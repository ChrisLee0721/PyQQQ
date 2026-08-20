# Hamiltonian Simulation / Simulate e^{-iHt} for given Hamiltonian.

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

Hamiltonian simulation / 哈密顿量模拟

Simulate e^{-iHt} for given Hamiltonian.

---

## 快速上手

```python
from quonic.algorithms import hamiltonian_simulation_demo

result = hamiltonian_simulation_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Hamiltonian Simulation circuit](/images/hamiltonian_simulation_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import hamiltonian_simulation_demo

result = hamiltonian_simulation_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum chemistry (量子化学)
- - Material science (材料科学)
- - Quantum simulation (量子模拟)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/hamiltonian_simulation/hamiltonian_simulation.py
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
"""Hamiltonian simulation / 哈密顿量模拟

Simulate e^{-iHt} for given Hamiltonian.
模拟给定哈密顿量的 e^{-iHt}。

## Application / 应用场景
- Quantum chemistry (量子化学)
- Material science (材料科学)
- Quantum simulation (量子模拟)

## Output / 输出
Evolved state under Hamiltonian evolution.
哈密顿量演化下的演化态。"""

from quonic.algorithms import hamiltonian_simulation_demo

result = hamiltonian_simulation_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/hamiltonian_simulation/hamiltonian_simulation.py
```

---

## 下载

- [hamiltonian_simulation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/hamiltonian_simulation/hamiltonian_simulation.py)
