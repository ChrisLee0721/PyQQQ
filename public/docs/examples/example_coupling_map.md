# Coupling Map / Coupling map / 耦合图

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

Coupling map / 耦合图

Coupling map / 耦合图

---

## 快速上手

```python
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
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Coupling Map circuit](/images/coupling_map_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
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
python examples/coupling_map/coupling_map.py
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
"""Coupling map / 耦合图

Coupling map / 耦合图

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

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

```

### 运行方式

```bash
python examples/coupling_map/coupling_map.py
```

---

## 下载

- [coupling_map.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/coupling_map/coupling_map.py)
