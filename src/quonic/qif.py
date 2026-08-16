"""qif —— 量子叠加 if：把 if/else 两个分支编译成受控酉，再分解成基础门。

    from quonic import qgate, qif
    from quonic.gates import H, X, Z

    qgate(H, 0)
    qif(0).then(X, 1).else_(Z, 1)   # q0==1 时 X(q1)，否则 Z(q1)

物理语义（关键）：控制比特处于叠加态时**不测量**，两个分支相干叠加成
|0><0|⊗F + |1><1|⊗T（F=else 门，T=then 门），产生真纠缠；这与「先测量
再按结果二选一」的经典 if 根本不同——前者给贝尔态（纠缠），后者给经典
混合态（无纠缠）。

MVP 边界：只支持单比特分支门、then/else 作用在同一目标比特、无嵌套、
无测量。numpy 全部函数内 import，保证 `import quonic` 零开销。
"""

from .gates import resolve
from .ir import (
    ClassicalIfOperation,
    ClassicalWhileOperation,
    CMeasureOperation,
    GateOperation,
)
from .stack import current_circuit, pop, push


def _unitary(gate):
    """单比特门 → 2×2 酉矩阵（numpy 数组）。"""
    from .simulators._gates import single

    return single(gate.name, gate.params)


def _zyz(U):
    """单比特酉 U → (alpha, beta, gamma, delta)，
    满足 U = e^{i·alpha} Rz(beta) Ry(gamma) Rz(delta)。"""
    import numpy as np

    U = np.asarray(U, dtype=complex)
    det = np.linalg.det(U)
    alpha = float(np.angle(det) / 2.0)
    W = U * np.exp(-1j * alpha)  # det(W) = 1，进入 SU(2)
    a = W[0, 0]
    b = W[0, 1]
    gamma = 2.0 * np.arctan2(abs(b), abs(a))
    if np.isclose(abs(b), 0.0):
        beta = -2.0 * np.angle(a)
        delta = 0.0
    elif np.isclose(abs(a), 0.0):
        gamma = np.pi
        beta = -2.0 * np.angle(-b)
        delta = 0.0
    else:
        beta = -np.angle(a) - np.angle(-b)
        delta = -np.angle(a) + np.angle(-b)
    return alpha, float(beta), float(gamma), float(delta)


def _ctrl_unitary_decompose(V, c, t):
    """受控单比特酉 V → 基础门序列，实现 |0><0|⊗I + |1><1|⊗V。

    用 Nielsen-Chuang 图 4.6 构造：先 ZYZ 分解 V = e^{iα} Rz(β) Ry(γ) Rz(δ)，
    再令 A=Rz(β)Ry(γ/2)、B=Ry(-γ/2)Rz(-(δ+β)/2)、C=Rz((δ-β)/2)，则
    A·B·C = I 且 A·X·B·X·C = e^{-iα}V。对应电路（时间序）：
    P(α) · C · CX · B · CX · A（两个 CX 各对应一个 X，A/B/C 作用在 target）。
    """
    alpha, beta, gamma, delta = _zyz(V)
    g2 = gamma / 2.0

    def _rot(name, angle):
        return GateOperation(name, (t,), (angle,)) if abs(angle) > 1e-12 else None

    ops = []
    if abs(alpha) > 1e-12:
        ops.append(GateOperation("p", (c,), (alpha,)))
    for op in [
        _rot("rz", (delta - beta) / 2.0),   # C
        GateOperation("cx", (c, t)),
        _rot("rz", -(delta + beta) / 2.0),  # B 前段
        _rot("ry", -g2),                    # B 后段
        GateOperation("cx", (c, t)),
        _rot("ry", g2),                     # A 前段
        _rot("rz", beta),                   # A 后段
    ]:
        if op is not None:
            ops.append(op)
    return ops


def _qif_decompose(F, T, c, t):
    """把 qif 编译成基础门序列：|0><0|⊗F + |1><1|⊗T = ctrl(T·F†) · (I⊗F)。

    先无条件施加 F（else 分支），再施加受控 V=T·F†：control=0 得 F，
    control=1 得 V·F = T·F†·F = T。"""
    import numpy as np

    if F == T:
        # 两分支相同 → 无条件 F；恒等门则整体为空
        return [] if F.name == "i" else [GateOperation(F.name, (t,), F.params)]

    Fm = np.asarray(_unitary(F), dtype=complex)
    Tm = np.asarray(_unitary(T), dtype=complex)
    # 先施加 F（无条件），再受控 V：control=0 得 F，control=1 得 V·F=T ⟹ V=T·F†
    V = Tm @ Fm.conj().T
    ops = _ctrl_unitary_decompose(V, c, t)
    # F 是恒等门时不落一个无用的 I 门（else_(I, ...) 的常见写法）
    if F.name == "i":
        return ops
    return [GateOperation(F.name, (t,), F.params)] + ops


def _check_branch(g, which, kind="qif"):
    if g.num_qubits != 1:
        raise ValueError(f"MVP 的 {kind} 分支只支持单比特门，{which} 收到 {g.name}")
    if g.name == "measure":
        raise ValueError(f"{kind} 分支需要酉门，不能是测量门 'measure'")


class _QIfBuilder:
    def __init__(self, control):
        self.control = int(control)
        self._then = None
        self._else = None

    def then(self, gate, target):
        g = resolve(gate)
        _check_branch(g, "then")
        self._then = (g, int(target))
        return self

    def else_(self, gate, target):
        g = resolve(gate)
        _check_branch(g, "else")
        self._else = (g, int(target))
        return self._compile()

    def _compile(self):
        if self._then is None:
            raise ValueError("qif 缺少 then 分支（先 .then(...) 再 .else_(...)）")
        if self._else is None:
            raise ValueError("qif 缺少 else 分支（请调用 .else_(...)）")
        T, tt = self._then
        F, ft = self._else
        if tt != ft:
            raise ValueError(
                f"MVP 的 qif 要求 then/else 分支作用在同一目标比特，收到 {tt} 与 {ft}"
            )
        if self.control == tt:
            raise ValueError("qif 的控制比特与目标比特不能相同")
        ops = _qif_decompose(F, T, self.control, tt)
        circ = current_circuit()
        for op in ops:
            circ.add(op)
        return ops


def qif(control):
    """量子叠加 if 入口，返回 builder，链式调用 .then(...).else_(...)。"""
    return _QIfBuilder(control)


def controlled(gate, control, target):
    """对 target 施加受控单比特门 gate，control 为控制比特。

    例：controlled(X, 0, 1) 等价于 CNOT(0,1)。用 ZYZ + 受控 U 分解实现，
    结果追加到当前电路。gate 可为门对象或门名字符串（如 "h" / Rx(0.5)）。
    """
    g = resolve(gate)
    if g.num_qubits != 1:
        raise ValueError(f"controlled 的目标门必须是单比特门，收到 {g.name}")
    if g.name == "measure":
        raise ValueError("controlled 需要酉门，不能是测量门 'measure'")
    control = int(control)
    target = int(target)
    if control == target:
        raise ValueError("controlled 的控制比特与目标比特不能相同")
    ops = _ctrl_unitary_decompose(_unitary(g), control, target)
    circ = current_circuit()
    for op in ops:
        circ.add(op)
    return ops


class CReg:
    """具名经典位：持有一次测量结果，供 cif / cwhile 读取。"""

    def __init__(self, name):
        if not isinstance(name, str) or not name:
            raise ValueError(f"creg 名必须是非空字符串，收到 {name!r}")
        self.name = name

    def measure(self, qubit):
        """测量 qubit，把结果存进本经典位。返回 self 便于链式。"""
        current_circuit().add(CMeasureOperation(int(qubit), self.name))
        return self

    def __repr__(self):
        return f"CReg({self.name!r})"


def creg(name):
    """声明一个具名经典位。

    用法：flag = creg("flag")；flag.measure(0) 把 qubit 0 的测量结果存进去；
    再交给 cif(flag) / cwhile(flag) 分支或循环。
    """
    return CReg(name)


class _CIfBuilder:
    def __init__(self, control):
        self.control = control  # int（qubit）或 CReg（经典位）
        self._then = None
        self._else = None

    def then(self, gate, target):
        g = resolve(gate)
        _check_branch(g, "then", "cif")
        self._then = (g, int(target))
        return self

    def else_(self, gate, target):
        g = resolve(gate)
        _check_branch(g, "else", "cif")
        self._else = (g, int(target))
        return self._compile()

    def _compile(self):
        if self._then is None:
            raise ValueError("cif 缺少 then 分支（先 .then(...) 再 .else_(...)）")
        if self._else is None:
            raise ValueError("cif 缺少 else 分支（请调用 .else_(...)）")
        T, tt = self._then
        F, ft = self._else
        if tt != ft:
            raise ValueError(
                f"MVP 的 cif 要求 then/else 分支作用在同一目标比特，收到 {tt} 与 {ft}"
            )
        if isinstance(self.control, CReg):
            ctrl = self.control.name
        else:
            ctrl = int(self.control)
            if ctrl == tt:
                raise ValueError("cif 的控制比特与目标比特不能相同")
        op = ClassicalIfOperation(
            ctrl,
            GateOperation(T.name, (tt,), T.params),
            GateOperation(F.name, (ft,), F.params),
        )
        current_circuit().add(op)
        return op


def cif(control):
    """经典 if：按控制源二选一施加分支门。

    与 qif（量子叠加 if）不同，cif 产生经典混合态而非相干纠缠。
    control 可为：
      - 量子比特下标：**先测量**该比特再分支（测到 |1> 施加 then，|0> 施加 else）
      - CReg（creg() 声明的经典位）：直接读取已存好的测量结果

    例：
        qgate(H, 0)
        cif(0).then(X, 1).else_(Z, 1)      # 先测 q0，再二选一

        flag = creg("flag"); flag.measure(0)
        cif(flag).then(X, 1).else_(I, 1)   # 按 flag 已存结果分支
    """
    return _CIfBuilder(control)


class _CWhileBuilder:
    def __init__(self, cond, until, max_iters):
        if not isinstance(cond, CReg):
            raise TypeError(f"cwhile 的条件必须是 creg() 声明的经典位，收到 {cond!r}")
        self.creg = cond
        self.until = int(until)
        if self.until not in (0, 1):
            raise ValueError(f"cwhile 的 until 只能是 0 或 1，收到 {self.until}")
        self.max_iters = int(max_iters)
        if self.max_iters < 1:
            raise ValueError(f"cwhile 的 max_iters 必须 >= 1，收到 {self.max_iters}")

    def __enter__(self):
        push()  # 捕获循环体到新电路作用域
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        body = pop()
        if exc_type is not None:
            return False  # 循环体内异常：已弹栈，向上传播
        op = ClassicalWhileOperation(self.creg.name, self.until, tuple(body.ops))
        current_circuit().add(op)
        return False


def cwhile(cond, until=0, max_iters=10000):
    """经典反馈循环（repeat-until-success）：重复执行循环体，直到 creg 测量结果
    等于 until。循环体以 creg.measure(...) 结尾更新条件。

    用法（上下文管理器）：
        flag = creg("flag")
        with cwhile(flag, until=0):
            qgate(H, 0)
            flag.measure(0)   # 每次尝试都重新测量 flag

    注意：仅 native 后端支持 cwhile（逐 shot 动态执行）；其余后端抛
    NotImplementedError。循环体必须测量条件 creg，否则会一直循环到
    max_iters 上限。
    """
    return _CWhileBuilder(cond, until, max_iters)
