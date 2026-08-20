# Qcnn / Quantum CNN for classification tasks.

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

Quantum Convolutional Neural Network / 量子卷积神经网络

Quantum CNN for classification tasks.

---

## 快速上手

```python
from quonic.algorithms import qcnn_demo

result = qcnn_demo(maxiter=50)
print(f"Accuracy: {result.value}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qcnn circuit](/images/qcnn_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qcnn_demo

result = qcnn_demo(maxiter=50)
print(f"Accuracy: {result.value}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Image classification (图像分类)
- - Pattern recognition (模式识别)
- - Quantum ML (量子机器学习)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qcnn/qcnn.py
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
"""Quantum Convolutional Neural Network / 量子卷积神经网络

Quantum CNN for classification tasks.
量子 CNN 用于分类任务。

## Application / 应用场景
- Image classification (图像分类)
- Pattern recognition (模式识别)
- Quantum ML (量子机器学习)

## Output / 输出
Classification accuracy.
分类准确率。"""

from quonic.algorithms import qcnn_demo

result = qcnn_demo(maxiter=50)
print(f"Accuracy: {result.value}")

```

### 运行方式

```bash
python examples/qcnn/qcnn.py
```

---

## 下载

- [qcnn.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qcnn/qcnn.py)
