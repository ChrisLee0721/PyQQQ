# Amplitude Estimation / Quantum algorithm to estimate the amplitude of a marked state.

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

Estimate success probability / 估计成功概率

Quantum algorithm to estimate the amplitude of a marked state.

---

## 快速上手

```python
from quonic.algorithms import amplitude_estimation_demo

result = amplitude_estimation_demo(n_qubits=2, n_precision=3, shots=1024)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Amplitude Estimation circuit](/images/amplitude_estimation_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import amplitude_estimation_demo

result = amplitude_estimation_demo(n_qubits=2, n_precision=3, shots=1024)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Monte Carlo integration (蒙特卡洛积分)
- - Risk analysis (风险分析)
- - Option pricing (期权定价)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/amplitude_estimation/amplitude_estimation.py
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
"""Estimate success probability / 估计成功概率

Quantum algorithm to estimate the amplitude of a marked state.
量子算法估计标记态的振幅。

## Application / 应用场景
- Monte Carlo integration (蒙特卡洛积分)
- Risk analysis (风险分析)
- Option pricing (期权定价)

## Output / 输出
Estimated amplitude with quadratic speedup over classical.
估计振幅，相比经典有二次加速。"""

from quonic.algorithms import amplitude_estimation_demo

result = amplitude_estimation_demo(n_qubits=2, n_precision=3, shots=1024)
print(result.counts)

```

### 运行方式

```bash
python examples/amplitude_estimation/amplitude_estimation.py
```

---

## 下载

- [amplitude_estimation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/amplitude_estimation/amplitude_estimation.py)
