"""量子相位估计（QPE）模板。

估计单比特门 U = Rz(θ) 作用在 |1> 上的本征相位。

Rz(θ)|1> = e^{iθ/2}|1>，所以本征相位 φ = θ/2。
QPE 用 n 个相位比特估计 j，满足 j/2^n ≈ φ/(2π) = θ/(4π)。

示例：
    import math
    from quonic.algorithms import qpe

    result = qpe(math.pi, n_precision=3, shots=1024)
    # Rz(π)|1> 相位 π/2，φ/(2π)=1/4，j≈2 -> 相位比特 "010"
"""


from ..backends import get_backend
from ..ir import Circuit, GateOperation
from ..qft import add_iqft


def _add_crz(circuit, c, t, theta):
    # 受控 Rz(theta)（控制 c，目标 t）
    circuit.add(GateOperation("cx", (c, t)))
    circuit.add(GateOperation("rz", (t,), (-theta / 2,)))
    circuit.add(GateOperation("cx", (c, t)))
    circuit.add(GateOperation("rz", (t,), (theta / 2,)))


def _add_iqft(circuit, n):
    # 逆量子傅里叶变换（qubit 0 = 最低位），委托给 qft 模块
    add_iqft(circuit, list(range(n)))


def qpe(theta, n_precision, shots=1024, backend="auto"):
    """估计 Rz(theta) 作用在 |1> 上的本征相位。

    参数：
        theta: 单比特旋转角（弧度）。
        n_precision: 相位估计的比特数。
        shots / backend: 采样参数。

    返回：Result（kind="counts"）。比特串最右侧 n_precision 位是相位估计，
    其整数值 j 满足 j/2^n ≈ theta/(4π)（n = n_precision）。
    """
    n = n_precision
    state_qubit = n
    circuit = Circuit()
    circuit.add(GateOperation("x", (state_qubit,)))
    for j in range(n):
        circuit.add(GateOperation("h", (j,)))
    for j in range(n):
        _add_crz(circuit, j, state_qubit, theta * (2 ** (n - 1 - j)))
    _add_iqft(circuit, n)
    return get_backend(backend).run(circuit, shots=shots)
