# Quantum Kernel / Compute quantum kernel matrix for ML.

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

Quantum Kernel Estimation / 量子核估计

Compute quantum kernel matrix for ML.

---

## 快速上手

```python
from quonic.algorithms import quantum_kernel

X = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
result = quantum_kernel(X, n_qubits=2, shots=10000)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Quantum Kernel circuit](/images/quantum_kernel_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import quantum_kernel

X = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
result = quantum_kernel(X, n_qubits=2, shots=10000)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Kernel methods (核方法)
- - SVM (支持向量机)
- - Quantum ML (量子机器学习)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/quantum_kernel/quantum_kernel.py
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
"""Quantum Kernel Estimation / 量子核估计

Compute quantum kernel matrix for ML.
计算用于机器学习的量子核矩阵。

## Application / 应用场景
- Kernel methods (核方法)
- SVM (支持向量机)
- Quantum ML (量子机器学习)

## Output / 输出
Kernel matrix entries.
核矩阵元素。"""

from quonic.algorithms import quantum_kernel

X = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
result = quantum_kernel(X, n_qubits=2, shots=10000)
print(result.counts)

```

### 运行方式

```bash
python examples/quantum_kernel/quantum_kernel.py
```

---

## 下载

- [quantum_kernel.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_kernel/quantum_kernel.py)
