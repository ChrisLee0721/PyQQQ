"""量子傅里叶变换（QFT）及其逆变换。

qubits 参数是一个量子比特索引列表，第一个元素视为最低位。
采用无 swap 约定（与 QPE 一致）。
"""

import math

from .ir import GateOperation


def _add_cp(circuit, c, t, phi):
    # 受控相位 CP(phi)=diag(1,1,1,e^{i phi})，后端直接支持原生 cp 门
    circuit.add(GateOperation("cp", (c, t), (phi,)))


def add_qft(circuit, qubits):
    """正向 QFT（无 swap，qubits[0] 为最低位）。"""
    n = len(qubits)
    for j in range(n - 1, -1, -1):
        circuit.add(GateOperation("h", (qubits[j],)))
        for k in range(j - 1, -1, -1):
            _add_cp(circuit, qubits[k], qubits[j], math.pi / 2 ** (j - k))


def add_iqft(circuit, qubits):
    """逆 QFT（无 swap），是 add_qft 的逆。"""
    n = len(qubits)
    for j in range(n):
        for k in range(j):
            _add_cp(circuit, qubits[k], qubits[j], -math.pi / 2 ** (j - k))
        circuit.add(GateOperation("h", (qubits[j],)))
