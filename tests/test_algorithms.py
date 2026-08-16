"""算法模板测试：Grover / VQE / QAOA。"""

import numpy as np

from quonic.algorithms import (
    diffusion,
    from_qiskit_nature,
    grover,
    mark_state,
    oracle,
    qaoa_maxcut,
    qpe,
    quantum_counting,
    vqe,
)
from quonic.ir import GateOperation


def test_grover_marks_target():
    # 在 2 个量子比特中标记 |11>（CZ 相位翻转），迭代 1 次即可高概率命中
    def oracle(circuit):
        circuit.add(GateOperation("cz", (0, 1)))

    result = grover(oracle, 2, shots=1024)
    counts = result.counts
    total = sum(counts.values())
    assert counts.get("11", 0) / total > 0.9, f"{counts}"


def test_grover_bitstring():
    # 直接传比特串，等价于 mark_state("11")
    result = grover("11", 2, shots=1024)
    counts = result.counts
    total = sum(counts.values())
    assert counts.get("11", 0) / total > 0.9, f"{counts}"


def test_mark_state_with_zero_bit():
    # mark_state("10") 标记 |10>（qubit0=0, qubit1=1），需自动翻转 0 位
    result = grover(mark_state("10"), 2, shots=1024)
    counts = result.counts
    total = sum(counts.values())
    assert counts.get("10", 0) / total > 0.9, f"{counts}"


def test_grover_four_qubits():
    # n=4 走 mcz（多控制 Z）路径，迭代 floor(π/4·4)=3 次仍应高概率命中
    result = grover("1111", 4, shots=1024)
    counts = result.counts
    total = sum(counts.values())
    assert counts.get("1111", 0) / total > 0.9, f"{counts}"


def test_from_qiskit_nature():
    # 把 Qiskit 的 SparsePauliOp 转成 [(coeff, pauli)] 再喂 vqe，能量应与直接传一致
    from qiskit.quantum_info import SparsePauliOp

    op = SparsePauliOp.from_list([("ZZ", 1.0), ("XI", 1.0), ("IX", 1.0)])
    terms = from_qiskit_nature(op)
    result = vqe(terms, 2, init_params=[0.1] * 4, maxiter=500)
    exact = -np.sqrt(5.0)
    assert abs(result.value - exact) < 0.02, f"{result.value} vs {exact}"


def test_vqe_transverse_ising():
    # H = Z⊗Z + X⊗I + I⊗X，精确基态能量为 -sqrt(5) ≈ -2.236
    hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
    result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=500)
    exact = -np.sqrt(5.0)
    assert abs(result.value - exact) < 0.02, f"{result.value} vs {exact}"


def test_qaoa_maxcut_triangle():
    # 三角形图最大割 = 2（任取两个顶点分到一侧）
    edges = [(0, 1), (1, 2), (0, 2)]
    result = qaoa_maxcut(edges, 3, p=1, init_params=[0.3, 0.3], maxiter=500)
    assert result.value > 1.8, f"{result.value}"


def _qpe_phase_bits(result, n):
    # 结果比特串最右侧 n 位是相位估计（最左位是始终为 |1> 的本征态比特）
    best = max(result.counts, key=result.counts.get)
    return best[-n:]


def test_qpe_pi():
    # Rz(π)|1> 相位 π/2，φ/(2π)=1/4，2 位精度 -> j=1 -> "01"
    result = qpe(np.pi, 2, shots=1024)
    assert _qpe_phase_bits(result, 2) == "01"


def test_qpe_pi_half():
    # Rz(π/2)|1> 相位 π/4，φ/(2π)=1/8，3 位精度 -> j=1 -> "001"
    result = qpe(np.pi / 2, 3, shots=1024)
    assert _qpe_phase_bits(result, 3) == "001"


def test_qpe_pi_n3():
    # Rz(π)|1>，3 位精度 -> j=2 -> "010"
    result = qpe(np.pi, 3, shots=1024)
    assert _qpe_phase_bits(result, 3) == "010"


def test_oracle_decorator():
    # @oracle 把经典谓词编译成相位神谕，Grover 应命中唯一解 |101>
    @oracle(3)
    def f(x):
        return x == 5

    result = grover(f, 3, shots=1024)
    counts = result.counts
    total = sum(counts.values())
    assert counts.get("101", 0) / total > 0.9, f"{counts}"


def test_quantum_counting_half():
    # N=8 中偶数共 4 个，M/N=1/2 是量子计数的精确情形
    @oracle(3)
    def f(x):
        return x & 1 == 0

    result = quantum_counting(f, 3, shots=2048)
    assert abs(result.value - 4.0) < 0.5, f"{result.value}"


def test_quantum_counting_single():
    # N=8 中唯一解 |000>，估计值应在 1 附近（有限 t 精度下 0.3~2.5 之间）
    @oracle(3)
    def f(x):
        return x == 0

    result = quantum_counting(f, 3, shots=2048)
    assert 0.3 < result.value < 2.5, f"{result.value}"


def _matrix(ops, n):
    from quonic.simulators._statevector import StatevectorEngine

    cols = []
    for i in range(2 ** n):
        e = StatevectorEngine(n)
        e.state = np.zeros(2 ** n, dtype=complex)
        e.state[i] = 1.0
        for op in ops:
            e.apply(op.name, op.qubits, op.params)
        cols.append(e.state.copy())
    return np.column_stack(cols)


def test_diffusion_matches_operator():
    # diffusion(n) 本身（含 H·X·相位翻转·X·H）应等于 2|s><s| - I
    from quonic import reset
    from quonic.stack import current_circuit

    reset()
    diffusion(2)
    ops = current_circuit().ops
    reset()  # 清理全局电路，避免污染后续测试
    got = _matrix(ops, 2)

    s = np.ones(4, dtype=complex) / 2.0  # |s> = (|00>+|01>+|10>+|11>)/2
    # H·X·相位翻转·X·H = I - 2|s><s|（与 2|s><s| - I 只差全局相位 -1）
    expected = np.eye(4, dtype=complex) - 2.0 * np.outer(s, s)
    assert np.allclose(got, expected, atol=1e-9)
