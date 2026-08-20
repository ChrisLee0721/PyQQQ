# Smart Scheduling / 智能调度

> **Backends** / 后端

## Overview / 概述

Scheduling / 调度

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
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
```

## Run / 运行

```bash
python examples/schedule/schedule.py
```

## Download / 下载

[schedule.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/schedule/schedule.py)
