# Qbm / Quantum version of Boltzmann machine for generative modeling.

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

Quantum Boltzmann Machine / 量子玻尔兹曼机

Quantum version of Boltzmann machine for generative modeling.

---

## 快速上手

```python
from quonic.algorithms import qbm_demo

result = qbm_demo(temperature=1.0)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qbm circuit](/images/qbm_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qbm_demo

result = qbm_demo(temperature=1.0)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Generative models (生成模型)
- - Sampling (采样)
- - Machine learning (机器学习)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qbm/qbm.py
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
"""Quantum Boltzmann Machine / 量子玻尔兹曼机

Quantum version of Boltzmann machine for generative modeling.
量子版玻尔兹曼机用于生成建模。

## Application / 应用场景
- Generative models (生成模型)
- Sampling (采样)
- Machine learning (机器学习)

## Output / 输出
Learned probability distribution.
学习到的概率分布。"""

from quonic.algorithms import qbm_demo

result = qbm_demo(temperature=1.0)
print(result.counts)

```

### 运行方式

```bash
python examples/qbm/qbm.py
```

---

## 下载

- [qbm.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qbm/qbm.py)
