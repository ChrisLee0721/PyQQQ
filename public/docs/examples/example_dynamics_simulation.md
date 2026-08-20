# Dynamics Simulation / Simulate time evolution of quantum systems.

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

Quantum dynamics simulation / 量子动力学模拟

Simulate time evolution of quantum systems.

---

## 快速上手

```python
from quonic.algorithms import dynamics_simulation_demo

result = dynamics_simulation_demo(n_steps=10, shots=1024)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Dynamics Simulation circuit](/images/dynamics_simulation_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import dynamics_simulation_demo

result = dynamics_simulation_demo(n_steps=10, shots=1024)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum chemistry (量子化学)
- - Material science (材料科学)
- - Condensed matter (凝聚态)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/dynamics_simulation/dynamics_simulation.py
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
"""Quantum dynamics simulation / 量子动力学模拟

Simulate time evolution of quantum systems.
模拟量子系统的时间演化。

## Application / 应用场景
- Quantum chemistry (量子化学)
- Material science (材料科学)
- Condensed matter (凝聚态)

## Output / 输出
Evolved state after time t.
时间 t 后的演化态。"""

from quonic.algorithms import dynamics_simulation_demo

result = dynamics_simulation_demo(n_steps=10, shots=1024)
print(result.counts)

```

### 运行方式

```bash
python examples/dynamics_simulation/dynamics_simulation.py
```

---

## 下载

- [dynamics_simulation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/dynamics_simulation/dynamics_simulation.py)
