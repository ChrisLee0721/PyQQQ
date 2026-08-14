"""后端无关的中间表示（IR）。

qgate() 先把用户操作记录成与后端无关的 GateOperation / Circuit，
qshow() 再交给具体后端（Qiskit / Cirq / ...）翻译执行。
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class GateOperation:
    name: str
    qubits: Tuple[int, ...]


class Circuit:
    def __init__(self):
        self.ops: List[GateOperation] = []
        self.num_qubits: int = 0

    def add(self, op: GateOperation) -> None:
        self.ops.append(op)
        for q in op.qubits:
            if q + 1 > self.num_qubits:
                self.num_qubits = q + 1

    def measured_qubits(self):
        return {op.qubits[0] for op in self.ops if op.name == "measure"}

    def unmeasured_qubits(self):
        measured = self.measured_qubits()
        return [q for q in range(self.num_qubits) if q not in measured]

    def is_empty(self):
        return not self.ops
