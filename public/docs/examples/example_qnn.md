# Qnn / Variational quantum circuit as neural network.

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

Quantum Neural Network / 量子神经网络

Variational quantum circuit as neural network.

---

## 快速上手

```python
from quonic.algorithms import qnn_demo

result = qnn_demo(n_qubits=2, depth=2)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qnn circuit](/images/qnn_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qnn_demo

result = qnn_demo(n_qubits=2, depth=2)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Classification (分类)
- - Regression (回归)
- - Function approximation (函数逼近)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qnn/qnn.py
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
"""Quantum Neural Network / 量子神经网络

Variational quantum circuit as neural network.
变分量子电路作为神经网络。

## Application / 应用场景
- Classification (分类)
- Regression (回归)
- Function approximation (函数逼近)

## Output / 输出
Trained model predictions.
训练模型预测。"""

from quonic.algorithms import qnn_demo

result = qnn_demo(n_qubits=2, depth=2)
print(result.counts)

```

### 运行方式

```bash
python examples/qnn/qnn.py
```

---

## 下载

- [qnn.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qnn/qnn.py)
