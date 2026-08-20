# Qng / Uses quantum Fisher information for better optimization.

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

Quantum Natural Gradient / 量子自然梯度

Uses quantum Fisher information for better optimization.

---

## 快速上手

```python
from quonic.algorithms import qng_demo

result = qng_demo(n_params=2, maxiter=50)
print(f"Final loss: {result.value}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qng circuit](/images/qng_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qng_demo

result = qng_demo(n_params=2, maxiter=50)
print(f"Final loss: {result.value}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Variational algorithms (变分算法)
- - VQE optimization (VQE 优化)
- - Quantum ML (量子机器学习)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qng/qng.py
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
"""Quantum Natural Gradient / 量子自然梯度

Uses quantum Fisher information for better optimization.
使用量子 Fisher 信息进行更好的优化。

## Application / 应用场景
- Variational algorithms (变分算法)
- VQE optimization (VQE 优化)
- Quantum ML (量子机器学习)

## Output / 输出
Optimized parameters with faster convergence.
更快收敛的优化参数。"""

from quonic.algorithms import qng_demo

result = qng_demo(n_params=2, maxiter=50)
print(f"Final loss: {result.value}")

```

### 运行方式

```bash
python examples/qng/qng.py
```

---

## 下载

- [qng.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qng/qng.py)
