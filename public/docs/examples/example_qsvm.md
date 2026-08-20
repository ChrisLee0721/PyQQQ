# Qsvm / SVM with quantum kernel for classification.

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

Quantum Support Vector Machine / 量子支持向量机

SVM with quantum kernel for classification.

---

## 快速上手

```python
from quonic.algorithms import qsvm_demo

result = qsvm_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qsvm circuit](/images/qsvm_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qsvm_demo

result = qsvm_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Classification (分类)
- - Pattern recognition (模式识别)
- - Quantum ML (量子机器学习)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qsvm/qsvm.py
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
"""Quantum Support Vector Machine / 量子支持向量机

SVM with quantum kernel for classification.
使用量子核的 SVM 进行分类。

## Application / 应用场景
- Classification (分类)
- Pattern recognition (模式识别)
- Quantum ML (量子机器学习)

## Output / 输出
Classification accuracy.
分类准确率。"""

from quonic.algorithms import qsvm_demo

result = qsvm_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/qsvm/qsvm.py
```

---

## 下载

- [qsvm.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qsvm/qsvm.py)
