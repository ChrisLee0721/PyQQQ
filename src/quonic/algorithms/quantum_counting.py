"""量子计数（quantum counting）模板。

用 Grover 迭代 + 量子相位估计（QPE）估计满足神谕的解的个数 M。

原理：Grover 算子 G 在 {|非解>, |解>} 子空间内旋转角度 2θ，其中
sin²θ = M / N（N = 2^n）。QPE 估计 G 的本征相位 θ/π，从而反解出 M。

示例：在 3 比特（N=8）中统计有多少个状态满足谓词

    from quonic.algorithms import oracle, quantum_counting

    @oracle(3)
    def f(x):
        return x & 1 == 0            # 偶数：共 4 个解

    result = quantum_counting(f, 3)
    print(result.value)              # 接近 4
"""

import math

from ..backends import get_backend
from ..ir import Circuit, GateOperation
from ..result import Result
from .qpe import _add_iqft


def _marked_states(oracle, n_qubits):
    if isinstance(oracle, str):
        if len(oracle) != n_qubits:
            raise ValueError(
                f"标记比特串 '{oracle}' 长度 {len(oracle)} 与量子比特数 {n_qubits} 不一致"
            )
        return [int(oracle, 2)]
    if hasattr(oracle, "marked"):  # @oracle 装饰器产物
        if oracle.n_qubits != n_qubits:
            raise ValueError(
                f"神谕的量子比特数 {oracle.n_qubits} 与 n_qubits={n_qubits} 不一致"
            )
        return list(oracle.marked)
    if callable(oracle):  # 裸谓词 f(x) -> bool
        states = [x for x in range(2 ** n_qubits) if oracle(x)]
        if not states:
            raise ValueError("神谕没有标记任何状态，无法计数")
        return states
    raise TypeError("oracle 必须是标记比特串、@oracle 装饰器产物或谓词函数")


def _add_controlled_oracle(circuit, control, search, marked):
    n = len(search)
    for x in marked:
        bits = format(x, f"0{n}b")
        for q in range(n):
            if bits[n - 1 - q] == "0":
                circuit.add(GateOperation("x", (search[q],)))
        circuit.add(GateOperation("mcz", tuple([control] + search)))
        for q in range(n):
            if bits[n - 1 - q] == "0":
                circuit.add(GateOperation("x", (search[q],)))


def _add_controlled_diffusion(circuit, control, search):
    for q in search:
        circuit.add(GateOperation("h", (q,)))
    for q in search:
        circuit.add(GateOperation("x", (q,)))
    circuit.add(GateOperation("mcz", tuple([control] + search)))
    for q in search:
        circuit.add(GateOperation("x", (q,)))
    for q in search:
        circuit.add(GateOperation("h", (q,)))


def _add_controlled_grover(circuit, control, search, marked):
    _add_controlled_oracle(circuit, control, search, marked)
    _add_controlled_diffusion(circuit, control, search)


def quantum_counting(oracle, n_qubits, t=None, backend="auto", shots=1024):
    """估计满足神谕的解的个数 M。

    参数：
        oracle: 标记比特串、@oracle 装饰器产物或谓词 f(x)->bool。
        n_qubits: 搜索空间量子比特数（N = 2**n_qubits）。
        t: 计数量子比特数，默认 n_qubits + 1（越大估计越精确）。
        backend / shots: 采样参数。

    返回：Result（kind="value"），result.value 为 M 的估计值。
    """
    marked = _marked_states(oracle, n_qubits)
    if t is None:
        t = n_qubits + 1

    search = list(range(t, t + n_qubits))
    circuit = Circuit()
    for q in range(t + n_qubits):
        circuit.add(GateOperation("h", (q,)))

    for j in range(t):
        for _ in range(2 ** (t - 1 - j)):
            _add_controlled_grover(circuit, j, search, marked)

    _add_iqft(circuit, t)

    result = get_backend(backend).run(circuit, shots=shots)
    best = max(result.counts, key=result.counts.get)
    j = int(best[-t:], 2)  # 最右侧 t 位是计数比特
    m = 2 ** n_qubits * math.sin(math.pi * abs(j / 2 ** t - 0.5)) ** 2
    return Result.from_value(m, j=j, t=t, counts=result.counts)
