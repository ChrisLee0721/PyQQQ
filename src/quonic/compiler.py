"""编译 seam：门分解 + 拓扑校验（不执行、不碰真实硬件）。

两件事：

1. **门分解**（`decompose`）—— 把高阶门展开成基础门集，是后端无关的
   「可移植核心」，QuoNic 自己拥有，用户不被某个后端的电路形状绑住。
2. **连通性校验**（`compile`）—— 对照 coupling_map 检查两/多比特门是否
   落在允许的边上，放不下抛 RoutingError。

SWAP 路由是留好的下一个扩展点，接在此之后即可，无需改动 IR 或调度器。
"""

import math
from collections import deque

from .ir import Circuit, ClassicalIfOperation, CMeasureOperation, GateOperation


class RoutingError(ValueError):
    """电路无法映射到目标耦合图。"""


# 分解后允许出现的基础门集（decompose 的输出保证落在其中）
BASIC_GATES = {"i", "h", "x", "y", "z", "rx", "ry", "rz", "p", "cx", "cz"}


def _p(q, theta):
    return GateOperation("p", (q,), (theta,))


def _decompose_cp(c, t, theta):
    """受控相位 cp(theta) = p·cx·p·cx·p（精确，无 ancilla）。"""
    half = theta / 2
    return [
        _p(c, half),
        GateOperation("cx", (c, t)),
        _p(t, -half),
        GateOperation("cx", (c, t)),
        _p(t, half),
    ]


def _decompose_ccx(a, b, c):
    """精确 Toffoli（Nielsen-Chuang 图 4.9），用 p(π/4) 当 T 门，6 个 cx。"""
    t = math.pi / 4
    return [
        GateOperation("h", (c,)),
        GateOperation("cx", (b, c)),
        _p(c, -t),
        GateOperation("cx", (a, c)),
        _p(c, t),
        GateOperation("cx", (b, c)),
        _p(c, -t),
        GateOperation("cx", (a, c)),
        _p(b, t),
        _p(c, t),
        GateOperation("h", (c,)),
        GateOperation("cx", (a, b)),
        _p(a, t),
        _p(b, -t),
        GateOperation("cx", (a, b)),
    ]


def _decompose_mcx(controls, target, new_ancillas):
    """多控制 X：k=1 -> cx；k=2 -> Toffoli；k>=3 -> AND 级联（k-2 个干净 ancilla）。"""
    k = len(controls)
    if k == 1:
        return [GateOperation("cx", (controls[0], target))]
    if k == 2:
        return _decompose_ccx(controls[0], controls[1], target)

    anc = new_ancillas(k - 2)
    ops = []
    # 前向：anc[0] = c1&c2，anc[j] = anc[j-1] & c_{j+2}
    ops += _decompose_ccx(controls[0], controls[1], anc[0])
    for j in range(1, k - 2):
        ops += _decompose_ccx(anc[j - 1], controls[j + 1], anc[j])
    # 施加：t ^= anc[k-3] & c_k
    ops += _decompose_ccx(anc[k - 3], controls[k - 1], target)
    # 反算（还原 ancilla 到 |0>）
    for j in range(k - 3, 0, -1):
        ops += _decompose_ccx(anc[j - 1], controls[j + 1], anc[j])
    ops += _decompose_ccx(controls[0], controls[1], anc[0])
    return ops


def _decompose_mcz(qubits, new_ancillas):
    """多控制 Z：末位当 target，mcz = H·mcx·H；单控制直接 cz。"""
    t = qubits[-1]
    controls = qubits[:-1]
    if len(controls) == 1:
        return [GateOperation("cz", (controls[0], t))]
    return (
        [GateOperation("h", (t,))]
        + _decompose_mcx(controls, t, new_ancillas)
        + [GateOperation("h", (t,))]
    )


def decompose(circuit):
    """把高阶门（cp / ccx / mcz）展开成基础门集，返回新的 Circuit。

    输出门集 ∈ {i, h, x, y, z, rx, ry, rz, p, cx, cz}（BASIC_GATES）。
    多控制 mcz（>2 控制）会引入干净 ancilla（起止均为 |0>），因此输出比特数
    可能多于输入。分解是精确的（无相对相位），可对拍 statevector 验证。

    不改动原电路对象。
    """
    out = Circuit()
    out.allocate(circuit.num_qubits)
    # 可复用的干净 ancilla：每个多控制门分解后 ancilla 都还原到 |0>，
    # 因此同一组 ancilla 可以被后续门循环使用，总 ancilla 数 = 各门所需的最大值。
    pool = []
    next_ancilla = [circuit.num_qubits]

    def new_ancillas(m):
        while len(pool) < m:
            pool.append(next_ancilla[0])
            next_ancilla[0] += 1
        return tuple(pool[:m])

    for op in circuit.ops:
        if op.name == "cp":
            for g in _decompose_cp(op.qubits[0], op.qubits[1], op.params[0]):
                out.add(g)
        elif op.name == "ccx":
            for g in _decompose_ccx(*op.qubits):
                out.add(g)
        elif op.name == "mcz":
            for g in _decompose_mcz(op.qubits, new_ancillas):
                out.add(g)
        else:
            out.add(op)
    return out


def _violates(op, coupling_map):
    """两/多比特门是否有任意一对量子比特不相连。"""
    qs = op.qubits
    if len(qs) < 2:
        return False
    for i in range(len(qs)):
        for j in range(i + 1, len(qs)):
            if not coupling_map.has_edge(qs[i], qs[j]):
                return True
    return False


def compile(circuit, coupling_map=None):
    """把电路编译到目标拓扑，返回新的 Circuit（不改动原对象）。

    参数：
        circuit: 源电路。
        coupling_map: CouplingMap；None 表示全连接（无连通性约束）。

    目前仅做连通性校验；门分解请用 decompose()，路由是留好的扩展点。
    校验失败抛 RoutingError，成功则返回一份（当前与原电路等价的）副本。
    """
    out = Circuit()
    out.allocate(circuit.num_qubits)

    if coupling_map is None:
        for op in circuit.ops:
            out.add(op)
        return out

    problems = [
        op for op in circuit.ops
        if op.name not in ("measure", "cmeasure", "cif", "cwhile")
        and _violates(op, coupling_map)
    ]
    if problems:
        detail = ", ".join(f"{op.name}{op.qubits}" for op in problems[:5])
        if len(problems) > 5:
            detail += f" 等 {len(problems)} 个门"
        raise RoutingError(
            f"电路无法映射到耦合图（{coupling_map}）："
            f"以下门的量子比特对不相连 —— {detail}"
        )

    for op in circuit.ops:
        out.add(op)
    return out


# ---------------------------------------------------------------------------
# SWAP 路由
# ---------------------------------------------------------------------------

def _adjacency(coupling_map):
    adj = {q: set() for q in range(coupling_map.n)}
    for u, v in coupling_map.edges():
        adj[u].add(v)
        adj[v].add(u)
    return adj


def _shortest_path(adj, src, dst):
    """耦合图上的 BFS 最短路，返回节点序列 [src, ..., dst]；不连通返回 None。"""
    if src == dst:
        return [src]
    prev = {src: None}
    q = deque([src])
    while q:
        u = q.popleft()
        if u == dst:
            break
        for v in adj.get(u, ()):
            if v not in prev:
                prev[v] = u
                q.append(v)
    if dst not in prev:
        return None
    path = []
    cur = dst
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return path[::-1]


def route_swaps(circuit, coupling_map):
    """贪心 SWAP 路由：把两比特门映射到耦合图，插入 SWAP 使两端相邻。

    返回新的 Circuit，门量子比特下标已换成「物理比特」位置，并在两端不相邻的
    两比特门处插入 "swap" 门（相邻物理比特）。单比特门/测量门下标随映射更新；
    三比特及以上门按原样透传（调用方应先 decompose() 展开）。不改动原电路。
    """
    adj = _adjacency(coupling_map)
    n_phys = max(circuit.num_qubits, coupling_map.n)
    layout = list(range(n_phys))  # layout[q] = 逻辑 q 当前所在的物理位置
    out = Circuit()
    out.allocate(n_phys)

    def emit(name, qubits, params=()):
        out.add(GateOperation(name, tuple(qubits), params))

    for op in circuit.ops:
        if op.name == "measure":
            emit("measure", (layout[op.qubits[0]],))
            continue
        if op.name == "cif":
            # 经典控制流无邻接约束，只把控制/目标比特下标随布局重映射
            ctrl = layout[op.control] if isinstance(op.control, int) else op.control
            out.add(
                ClassicalIfOperation(
                    ctrl,
                    GateOperation(
                        op.then_op.name,
                        (layout[op.then_op.qubits[0]],),
                        op.then_op.params,
                    ),
                    GateOperation(
                        op.else_op.name,
                        (layout[op.else_op.qubits[0]],),
                        op.else_op.params,
                    ),
                )
            )
            continue
        if op.name == "cmeasure":
            # 具名经典位测量：只重映射量子比特下标，保留 creg 名
            out.add(CMeasureOperation(layout[op.qubit], op.creg))
            continue
        if op.name == "cwhile":
            raise NotImplementedError(
                "SWAP 路由暂不支持 cwhile（经典反馈循环）；"
                "请改用 native 后端直接运行，或在路由前展开循环"
            )
        if len(op.qubits) == 1:
            emit(op.name, (layout[op.qubits[0]],), op.params)
            continue
        if len(op.qubits) != 2:
            emit(op.name, tuple(layout[q] for q in op.qubits), op.params)
            continue

        c, t = op.qubits
        while True:
            pc, pt = layout[c], layout[t]
            if pt in adj.get(pc, ()):
                emit(op.name, (pc, pt), op.params)
                break
            path = _shortest_path(adj, pc, pt)
            if path is None or len(path) < 2:
                raise RoutingError(
                    f"耦合图不连通，无法路由 {op.name}{op.qubits}"
                )
            u, v = path[0], path[1]
            emit("swap", (u, v))
            lu, lv = layout.index(u), layout.index(v)
            layout[lu], layout[lv] = layout[lv], layout[lu]

    return out
