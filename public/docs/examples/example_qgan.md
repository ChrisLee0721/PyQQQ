# Qgan / Quantum generator + classical discriminator.

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

Quantum GAN / 量子 GAN

Quantum generator + classical discriminator.

---

## 快速上手

```python
from quonic.algorithms import qgan_demo

result = qgan_demo(n_steps=50)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qgan circuit](/images/qgan_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qgan_demo

result = qgan_demo(n_steps=50)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Data generation (数据生成)
- - Image synthesis (图像合成)
- - Quantum ML (量子机器学习)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qgan/qgan.py
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
"""Quantum GAN / 量子 GAN

Quantum generator + classical discriminator.
量子生成器 + 经典判别器。

## Application / 应用场景
- Data generation (数据生成)
- Image synthesis (图像合成)
- Quantum ML (量子机器学习)

## Output / 输出
Generated data distribution.
生成的数据分布。"""

from quonic.algorithms import qgan_demo

result = qgan_demo(n_steps=50)
print(result.counts)

```

### 运行方式

```bash
python examples/qgan/qgan.py
```

---

## 下载

- [qgan.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qgan/qgan.py)
