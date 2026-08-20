# Schedule / Scheduling / 调度

> **Example** / 示例

---

## 目录

- [为什么需要？](#为什么需要)
- [快速上手](#快速上手)
- [原理详解](#原理详解)
- [代码详解](#代码详解)
- [进阶用法](#进阶用法)
- [适用场景](#适用场景)
- [常见问题](#常见问题)
- [学习路径](#学习路径)
- [完整示例代码](#完整示例代码)

---

## 为什么需要？

Scheduling / 调度

Scheduling / 调度

---

## 快速上手

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

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Schedule circuit](/images/schedule_circuit.svg)

See code comments for explanation.

---

## 代码详解

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

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum computing (量子计算)
- - Algorithm demonstration (算法演示)
- - Educational (教学)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/schedule/schedule.py
```

### Q2: What backend is used?

The example uses the default backend. You can specify a different one:

```python
qshow(backend='qiskit')
```

---

## 学习路径

### 前置知识

- Basic quantum computing concepts
- QuoNic API basics

### 继续学习

- Other examples in this documentation
- QuoNic API reference

---

## 完整示例代码

```python
"""Scheduling / 调度

Scheduling / 调度

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

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

### 运行方式

```bash
python examples/schedule/schedule.py
```

---

## 下载

- [schedule.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/schedule/schedule.py)
