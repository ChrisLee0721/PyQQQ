"""Gate decomposition / 门分解

Gate decomposition / 门分解"""

from quonic.compiler import decompose
from quonic.ir import Circuit, GateOperation

circuit = Circuit()
circuit.add(GateOperation("ccx", (0, 1, 2)))

expanded = decompose(circuit)
print("输入门: ccx x 1")
print(f"输出门: {expanded.gate_count()} 个基础门")
print([op.name for op in expanded.ops])
