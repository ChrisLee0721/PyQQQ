# Quantum Ode / Quantum algorithm for ordinary differential equations.

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

ODE Solver / ODE 求解器

Quantum algorithm for ordinary differential equations.

---

## 快速上手

```python
from quonic.algorithms import quantum_ode_demo

result = quantum_ode_demo(shots=1024)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Quantum Ode circuit](/images/quantum_ode_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import quantum_ode_demo

result = quantum_ode_demo(shots=1024)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Physics simulation (物理模拟)
- - Engineering (工程)
- - Dynamics (动力学)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/quantum_ode/quantum_ode.py
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
"""ODE Solver / ODE 求解器

Quantum algorithm for ordinary differential equations.
常微分方程的量子算法。

## Application / 应用场景
- Physics simulation (物理模拟)
- Engineering (工程)
- Dynamics (动力学)

## Output / 输出
Solution trajectory.
解轨迹。"""

from quonic.algorithms import quantum_ode_demo

result = quantum_ode_demo(shots=1024)
print(result.counts)

```

### 运行方式

```bash
python examples/quantum_ode/quantum_ode.py
```

---

## 下载

- [quantum_ode.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_ode/quantum_ode.py)
