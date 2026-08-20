# Hhl / Quantum algorithm for Ax = b, exponential speedup.

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

Linear system solver / 线性方程组求解器

Quantum algorithm for Ax = b, exponential speedup.

---

## 快速上手

```python
from quonic.algorithms import hhl_demo

result = hhl_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Hhl circuit](/images/hhl_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import hhl_demo

result = hhl_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Machine learning (机器学习)
- - Optimization (优化)
- - Differential equations (微分方程)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/hhl/hhl.py
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
"""Linear system solver / 线性方程组求解器

Quantum algorithm for Ax = b, exponential speedup.
量子算法求解 Ax = b，指数加速。

## Application / 应用场景
- Machine learning (机器学习)
- Optimization (优化)
- Differential equations (微分方程)

## Output / 输出
Quantum state proportional to x = A^{-1}b.
与 x = A^{-1}b 成正比的量子态。"""

from quonic.algorithms import hhl_demo

result = hhl_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/hhl/hhl.py
```

---

## 下载

- [hhl.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/hhl/hhl.py)
