# Quantum Fitting / Quantum version of regression/curve fitting.

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

Quantum Curve Fitting / 量子曲线拟合

Quantum version of regression/curve fitting.

---

## 快速上手

```python
from quonic.algorithms import quantum_fitting_demo

result = quantum_fitting_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Quantum Fitting circuit](/images/quantum_fitting_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import quantum_fitting_demo

result = quantum_fitting_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Data fitting (数据拟合)
- - Prediction (预测)
- - Machine learning (机器学习)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/quantum_fitting/quantum_fitting.py
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
"""Quantum Curve Fitting / 量子曲线拟合

Quantum version of regression/curve fitting.
量子版回归/曲线拟合。

## Application / 应用场景
- Data fitting (数据拟合)
- Prediction (预测)
- Machine learning (机器学习)

## Output / 输出
Fitted parameters.
拟合参数。"""

from quonic.algorithms import quantum_fitting_demo

result = quantum_fitting_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/quantum_fitting/quantum_fitting.py
```

---

## 下载

- [quantum_fitting.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_fitting/quantum_fitting.py)
