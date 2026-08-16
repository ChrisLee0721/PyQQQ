"""QAOA（量子近似优化算法）模板，求解 MaxCut 问题。

给定无向图（边列表），用 p=1 层 QAOA 变分求最大割。

示例：三角形图（3 个顶点、3 条边）

    from quonic.algorithms import qaoa

    edges = [(0, 1), (1, 2), (0, 2)]
    result = qaoa.qaoa_maxcut(edges, 3)
    print(result["cut"])   # 三角形最大割 = 2
"""

from ..result import Result
from ..simulator import StatevectorSimulator


def _pauli_z(i, j, n):
    s = ["I"] * n
    s[i] = "Z"
    s[j] = "Z"
    return "".join(s)


def _qaoa_state(n, edges, p, params):
    gammas = params[:p]
    betas = params[p:]
    sim = StatevectorSimulator(n)
    for q in range(n):
        sim.apply("h", (q,))
    for layer in range(p):
        # 代价层：exp(-i γ Z_i Z_j) = CX · Rz(2γ) · CX
        for i, j in edges:
            sim.apply("cx", (i, j))
            sim.apply("rz", (j,), (2 * gammas[layer],))
            sim.apply("cx", (i, j))
        # 混合层：Rx(2β)
        for q in range(n):
            sim.apply("rx", (q,), (2 * betas[layer],))
    return sim


def qaoa_maxcut(edges, n_qubits, p=1, init_params=None, optimizer="COBYLA", maxiter=300,
                record_history=False):
    """变分求解给定图的 MaxCut。

    参数：
        edges: 边列表 [(i, j), ...]。
        n_qubits: 顶点数。
        p: QAOA 层数（默认 1）。
        init_params: 初始参数（长度 2p），默认全 0.1。
        optimizer / maxiter: 传给 scipy.optimize.minimize。
        record_history: 为 True 时把每步能量记录进 metadata["history"]，
            供 plot_energy_convergence 画收敛曲线（默认关闭）。

    返回：Result（kind="value"），result.value 为近似最大割，
    metadata 含 "params"（最优参数）、"energy"（Σ<ZiZj>）与可选 "history"。
    """
    try:
        from scipy.optimize import minimize
    except ImportError as e:
        raise ImportError(
            "使用 QAOA 需要安装 scipy：\n"
            "    pip install 'quonic[algorithms]'\n"
            "或： pip install scipy"
        ) from e

    if init_params is None:
        init_params = [0.1] * (2 * p)

    def cost(params):
        sim = _qaoa_state(n_qubits, edges, p, params)
        return sum(sim.expectation(_pauli_z(i, j, n_qubits)) for i, j in edges)

    history = []
    callback = None
    if record_history:
        def callback(xk):
            history.append(float(cost(xk)))

    result = minimize(
        cost,
        init_params,
        method=optimizer,
        options={"maxiter": maxiter},
        callback=callback,
    )
    energy = float(result.fun)
    cut = (len(edges) - energy) / 2.0
    metadata = {"params": [float(x) for x in result.x], "energy": energy}
    if record_history:
        metadata["history"] = history
    return Result.from_value(cut, **metadata)
