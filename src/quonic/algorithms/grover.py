"""Grover 搜索算法模板。

搜索某个计算基态，最简单的方式是直接传比特串（mark_state 自动生成神谕）：

    from quonic.algorithms import grover
    result = grover("11", 2, shots=1024)   # 在 2 比特中搜索 |11>

也可以提供自定义神谕（一个把目标态相位翻转的回调）：

    from quonic.algorithms import grover, mark_state
    result = grover(mark_state("11"), 2, shots=1024)
"""

import math

from ..backends import get_backend
from ..ir import Circuit, GateOperation


def _add_diffusion(circuit, n):
    for q in range(n):
        circuit.add(GateOperation("h", (q,)))
    for q in range(n):
        circuit.add(GateOperation("x", (q,)))
    _add_phase_flip_all_ones(circuit, n)
    for q in range(n):
        circuit.add(GateOperation("x", (q,)))
    for q in range(n):
        circuit.add(GateOperation("h", (q,)))


def _add_phase_flip_all_ones(circuit, n):
    # 对 |11...1> 施加 -1 相位（多控制 Z）
    if n == 1:
        circuit.add(GateOperation("z", (0,)))
    else:
        circuit.add(GateOperation("mcz", tuple(range(n))))


def mark_state(bitstring):
    """返回一个神谕回调，标记计算基态 |bitstring>。

    比特串最右位是 qubit 0（与 qshow 的比特串约定一致）。
    例：mark_state("11") 标记 |11>；mark_state("10") 标记 |10>（qubit0=0, qubit1=1）。
    """
    bitstring = str(bitstring)
    if not bitstring or any(ch not in "01" for ch in bitstring):
        raise ValueError(f"mark_state 需要只含 0/1 的比特串，收到 {bitstring!r}")
    n = len(bitstring)

    def oracle(circuit):
        # 把目标态中的 0 位翻成 1，做全 1 相位翻转，再翻回来
        for q in range(n):
            if bitstring[n - 1 - q] == "0":
                circuit.add(GateOperation("x", (q,)))
        _add_phase_flip_all_ones(circuit, n)
        for q in range(n):
            if bitstring[n - 1 - q] == "0":
                circuit.add(GateOperation("x", (q,)))

    return oracle


def grover(oracle, n_qubits, iterations=None, backend="auto", shots=1024):
    """运行 Grover 搜索。

    参数：
        oracle: 神谕，可以是回调函数 oracle(circuit)，也可以直接传比特串
            （如 "11"，等价于 mark_state("11")）。
        n_qubits: 量子比特数。
        iterations: 迭代次数，默认 floor(π/4 · √(2^n))。
        backend: 采样后端（qiskit / cirq / pennylane）。
        shots: 采样次数。

    返回：Result（kind="counts"），result.counts 为采样直方图。
    """
    if isinstance(oracle, str):
        if len(oracle) != n_qubits:
            raise ValueError(
                f"标记的比特串 '{oracle}' 长度 {len(oracle)} 与量子比特数 {n_qubits} 不一致"
            )
        oracle = mark_state(oracle)

    circuit = Circuit()
    for q in range(n_qubits):
        circuit.add(GateOperation("h", (q,)))

    if iterations is None:
        iterations = int(math.pi / 4 * math.sqrt(2 ** n_qubits))

    for _ in range(iterations):
        oracle(circuit)
        _add_diffusion(circuit, n_qubits)

    return get_backend(backend).run(circuit, shots=shots)


def diffusion(n_qubits):
    """把 Grover 扩散算子（2|s><s| - I）追加到当前电路。

    对 qubit 0..n_qubits-1 施加 H、X、多控制 Z、X、H 的序列，是振幅放大
    （Grover 迭代）的核心一步，可与 qgate / mark_state 组合构建自定义搜索：
        qgate(H, 0); qgate(H, 1); mark_state("11")(current_circuit()); diffusion(2)
    """
    from ..stack import current_circuit

    circ = current_circuit()
    _add_diffusion(circ, n_qubits)
    return circ
