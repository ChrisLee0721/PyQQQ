# Elliptic Curve / Quantum approach to elliptic curve discrete log.

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

Elliptic curve quantum algorithm / 椭圆曲线量子算法

Quantum approach to elliptic curve discrete log.

---

## 快速上手

```python
from quonic.algorithms import elliptic_curve_demo

result = elliptic_curve_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Elliptic Curve circuit](/images/elliptic_curve_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import elliptic_curve_demo

result = elliptic_curve_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Post-quantum cryptography (后量子密码学)
- - Blockchain security (区块链安全)
- - Digital signatures (数字签名)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/elliptic_curve/elliptic_curve.py
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
"""Elliptic curve quantum algorithm / 椭圆曲线量子算法

Quantum approach to elliptic curve discrete log.
椭圆曲线离散对数的量子方法。

## Application / 应用场景
- Post-quantum cryptography (后量子密码学)
- Blockchain security (区块链安全)
- Digital signatures (数字签名)

## Output / 输出
Approximate solution to ECDLP.
ECDLP 的近似解。"""

from quonic.algorithms import elliptic_curve_demo

result = elliptic_curve_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/elliptic_curve/elliptic_curve.py
```

---

## 下载

- [elliptic_curve.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/elliptic_curve/elliptic_curve.py)
