"""decompose: expand a Toffoli (CCX) into basic gates.

CCX is a 3-qubit gate; decompose() rewrites it using only single-qubit
gates and CX (no ancilla needed for a single Toffoli).
"""

from quonic.compiler import decompose
from quonic.ir import Circuit, GateOperation

circuit = Circuit()
circuit.add(GateOperation("ccx", (0, 1, 2)))

expanded = decompose(circuit)
print("输入门: ccx x 1")
print(f"输出门: {expanded.gate_count()} 个基础门")
print([op.name for op in expanded.ops])
