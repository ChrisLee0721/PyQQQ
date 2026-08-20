"""Scheduling / 调度

Scheduling / 调度"""

from quonic.ir import Circuit, GateOperation
from quonic.scheduler import circuit_features, schedule

circuit = Circuit()
circuit.add(GateOperation("h", (0,)))
for i in range(3):
    circuit.add(GateOperation("cx", (i, i + 1)))

feats = circuit_features(circuit)
print(f"n={feats['n']} depth={feats['depth']} gates={feats['gate_count']}")
print(f"is_clifford={feats['is_clifford']} treewidth_ub={feats['treewidth_ub']}")

rec = schedule(circuit)
print(f"推荐: backend={rec.backend}, method={rec.method}")
