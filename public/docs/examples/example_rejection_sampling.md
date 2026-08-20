# Rejection Sampling / Quantum-enhanced rejection sampling.

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

Rejection Sampling / 拒绝采样

Quantum-enhanced rejection sampling.

---

## 快速上手

```python
from quonic.algorithms import rejection_sampling_demo

result = rejection_sampling_demo(n_samples=100)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Rejection Sampling circuit](/images/rejection_sampling_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import rejection_sampling_demo

result = rejection_sampling_demo(n_samples=100)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Sampling (采样)
- - Distribution generation (分布生成)
- - Monte Carlo (蒙特卡洛)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/rejection_sampling/rejection_sampling.py
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
"""Rejection Sampling / 拒绝采样

Quantum-enhanced rejection sampling.
量子增强的拒绝采样。

## Application / 应用场景
- Sampling (采样)
- Distribution generation (分布生成)
- Monte Carlo (蒙特卡洛)

## Output / 输出
Samples from target distribution.
目标分布的样本。"""

from quonic.algorithms import rejection_sampling_demo

result = rejection_sampling_demo(n_samples=100)
print(result.counts)

```

### 运行方式

```bash
python examples/rejection_sampling/rejection_sampling.py
```

---

## 下载

- [rejection_sampling.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/rejection_sampling/rejection_sampling.py)
