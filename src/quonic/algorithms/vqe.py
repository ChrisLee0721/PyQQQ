"""VQE（变分量子本征求解器）模板。

给定一个用泡利项表示的哈密顿量，用硬件高效拟设（hardware-efficient
ansatz）变分求解其基态能量。

示例：横向场 Ising 模型 H = Z⊗Z + X⊗I + I⊗X（2 量子比特）

    from quonic.algorithms import vqe

    hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
    result = vqe(hamiltonian, 2)
    print(result["energy"])   # 接近精确基态能量
"""

from ..result import Result
from ..simulator import StatevectorSimulator


def _ansatz_state(n, params):
    # 硬件高效拟设：Ry 层 -> CX 链 -> Ry 层，共 2n 个参数
    sim = StatevectorSimulator(n)
    for q in range(n):
        sim.apply("ry", (q,), (params[q],))
    for q in range(n - 1):
        sim.apply("cx", (q, q + 1))
    for q in range(n):
        sim.apply("ry", (q,), (params[n + q],))
    return sim


def vqe(hamiltonian, n_qubits, init_params=None, optimizer="COBYLA", maxiter=300,
        record_history=False):
    """变分求解哈密顿量的基态能量。

    参数：
        hamiltonian: 列表 [(系数, 泡利串), ...]，泡利串长度 = n_qubits。
        n_qubits: 量子比特数。
        init_params: 初始参数（长度 2 * n_qubits），默认全零。
        optimizer: scipy.optimize.minimize 的方法名。
        maxiter: 最大迭代次数。
        record_history: 为 True 时把每步能量记录进 metadata["history"]，
            供 plot_energy_convergence 画收敛曲线（默认关闭，避免额外模拟开销）。

    返回：Result（kind="value"），result.value 为最优能量，
    result.metadata["params"] 为最优参数。
    """
    try:
        from scipy.optimize import minimize
    except ImportError as e:
        raise ImportError(
            "使用 VQE 需要安装 scipy：\n"
            "    pip install 'quonic[algorithms]'\n"
            "或： pip install scipy"
        ) from e

    if init_params is None:
        init_params = [0.0] * (2 * n_qubits)

    def energy(params):
        sim = _ansatz_state(n_qubits, params)
        return sum(coeff * sim.expectation(pauli) for coeff, pauli in hamiltonian)

    history = []
    callback = None
    if record_history:
        def callback(xk):
            history.append(float(energy(xk)))

    result = minimize(
        energy,
        init_params,
        method=optimizer,
        options={"maxiter": maxiter},
        callback=callback,
    )
    metadata = {"params": [float(x) for x in result.x]}
    if record_history:
        metadata["history"] = history
    return Result.from_value(float(result.fun), **metadata)
