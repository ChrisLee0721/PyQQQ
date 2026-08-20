# Quantum Monte Carlo / Quantum speedup for Monte Carlo methods.

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

Quantum Monte Carlo / 量子蒙特卡洛

Quantum speedup for Monte Carlo methods.

---

## 快速上手

```python
from quonic.algorithms import quantum_monte_carlo_demo

result = quantum_monte_carlo_demo(n_qubits=2, shots=1024)
print(f"Estimated value: {result.value}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Quantum Monte Carlo circuit](/images/quantum_monte_carlo_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import quantum_monte_carlo_demo

result = quantum_monte_carlo_demo(n_qubits=2, shots=1024)
print(f"Estimated value: {result.value}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Integration (积分)
- - Risk analysis (风险分析)
- - Finance (金融)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/quantum_monte_carlo/quantum_monte_carlo.py
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
"""Quantum Monte Carlo / 量子蒙特卡洛

Quantum speedup for Monte Carlo methods.
蒙特卡洛方法的量子加速。

## Application / 应用场景
- Integration (积分)
- Risk analysis (风险分析)
- Finance (金融)

## Output / 输出
Estimated integral value.
估计积分值。"""

from quonic.algorithms import quantum_monte_carlo_demo

result = quantum_monte_carlo_demo(n_qubits=2, shots=1024)
print(f"Estimated value: {result.value}")

```

### 运行方式

```bash
python examples/quantum_monte_carlo/quantum_monte_carlo.py
```

---

## 下载

- [quantum_monte_carlo.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_monte_carlo/quantum_monte_carlo.py)
