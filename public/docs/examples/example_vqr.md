# Vqr / Quantum model for regression tasks.

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

Variational Quantum Regressor / 变分量子回归器

Quantum model for regression tasks.

---

## 快速上手

```python
from quonic.algorithms import vqr

X = [[0.0], [0.5], [1.0], [1.5]]
y = [0.0, 0.479, 0.841, 0.997]
result = vqr(X, y, n_params=2, maxiter=100)
print(f"Final loss: {result.value}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Vqr circuit](/images/vqr_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import vqr

X = [[0.0], [0.5], [1.0], [1.5]]
y = [0.0, 0.479, 0.841, 0.997]
result = vqr(X, y, n_params=2, maxiter=100)
print(f"Final loss: {result.value}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Regression (回归)
- - Prediction (预测)
- - Function fitting (函数拟合)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/vqr/vqr.py
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
"""Variational Quantum Regressor / 变分量子回归器

Quantum model for regression tasks.
用于回归任务的量子模型。

## Application / 应用场景
- Regression (回归)
- Prediction (预测)
- Function fitting (函数拟合)

## Output / 输出
Predicted values.
预测值。"""

from quonic.algorithms import vqr

X = [[0.0], [0.5], [1.0], [1.5]]
y = [0.0, 0.479, 0.841, 0.997]
result = vqr(X, y, n_params=2, maxiter=100)
print(f"Final loss: {result.value}")

```

### 运行方式

```bash
python examples/vqr/vqr.py
```

---

## 下载

- [vqr.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/vqr/vqr.py)
