"""Coupling map / 耦合图

Coupling map / 耦合图"""

from quonic import CouplingMap, RoutingError
from quonic.compiler import compile, route_swaps
from quonic.ir import Circuit, GateOperation

line = CouplingMap.from_line(3)  # edges: 0-1, 1-2

circuit = Circuit()
circuit.add(GateOperation("cx", (0, 2)))  # not adjacent on the line

try:
    compile(circuit, coupling_map=line)
except RoutingError as e:
    print(f"编译失败: {type(e).__name__}")  # RoutingError (expected)

routed = route_swaps(circuit, line)
print("路由后门序列:")
for op in routed.ops:
    print(f"  {op.name}{op.qubits}")  # swap(0,1) then cx(1,2)
