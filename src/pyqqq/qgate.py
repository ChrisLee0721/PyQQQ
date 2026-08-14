"""qgate —— 向当前电路添加一个量子门。"""

from .gates import resolve
from .ir import GateOperation
from .stack import current_circuit


def qgate(gate, *qubits):
    g = resolve(gate)
    qubits = tuple(int(q) for q in qubits)
    if len(qubits) != g.num_qubits:
        raise ValueError(
            f"门 {g.name} 需要 {g.num_qubits} 个量子比特，但给了 {len(qubits)} 个：{qubits}"
        )
    op = GateOperation(name=g.name, qubits=qubits)
    current_circuit().add(op)
    return op
