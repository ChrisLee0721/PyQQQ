# Lattice Svp / Quantum approach to lattice-based cryptography.

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

Shortest Vector Problem / 最短向量问题

Quantum approach to lattice-based cryptography.

---

## 快速上手

```python
from quonic.algorithms import lattice_svp_demo

result = lattice_svp_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Lattice Svp circuit](/images/lattice_svp_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import lattice_svp_demo

result = lattice_svp_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Post-quantum cryptography (后量子密码学)
- - Lattice-based crypto (格密码)
- - Security analysis (安全分析)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/lattice_svp/lattice_svp.py
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
"""Shortest Vector Problem / 最短向量问题

Quantum approach to lattice-based cryptography.
格密码的量子方法。

## Application / 应用场景
- Post-quantum cryptography (后量子密码学)
- Lattice-based crypto (格密码)
- Security analysis (安全分析)

## Output / 输出
Approximate shortest vector.
近似最短向量。"""

from quonic.algorithms import lattice_svp_demo

result = lattice_svp_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/lattice_svp/lattice_svp.py
```

---

## 下载

- [lattice_svp.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/lattice_svp/lattice_svp.py)
