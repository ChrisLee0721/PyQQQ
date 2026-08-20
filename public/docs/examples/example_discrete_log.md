# Discrete Log / Find x such that a^x = b mod p.

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

Discrete logarithm / 离散对数

Find x such that a^x = b mod p.

---

## 快速上手

```python
from quonic.algorithms import discrete_log_demo

result = discrete_log_demo(a=2, b=8, p=11)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Discrete Log circuit](/images/discrete_log_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import discrete_log_demo

result = discrete_log_demo(a=2, b=8, p=11)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Cryptography (密码学)
- - RSA breaking (RSA 破解)
- - Key exchange (密钥交换)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/discrete_log/discrete_log.py
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
"""Discrete logarithm / 离散对数

Find x such that a^x = b mod p.
找到 x 使得 a^x = b mod p。

## Application / 应用场景
- Cryptography (密码学)
- RSA breaking (RSA 破解)
- Key exchange (密钥交换)

## Output / 输出
The discrete logarithm x.
离散对数 x。"""

from quonic.algorithms import discrete_log_demo

result = discrete_log_demo(a=2, b=8, p=11)
print(result.counts)

```

### 运行方式

```bash
python examples/discrete_log/discrete_log.py
```

---

## 下载

- [discrete_log.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/discrete_log/discrete_log.py)
