# Quantum Matrix Inversion / HHL-based matrix inversion for linear systems.

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

Matrix Inversion / 矩阵求逆

HHL-based matrix inversion for linear systems.

---

## 快速上手

```python
from quonic.algorithms import quantum_matrix_inversion_demo

result = quantum_matrix_inversion_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Quantum Matrix Inversion circuit](/images/quantum_matrix_inversion_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import quantum_matrix_inversion_demo

result = quantum_matrix_inversion_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Linear systems (线性系统)
- - Machine learning (机器学习)
- - Optimization (优化)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/quantum_matrix_inversion/quantum_matrix_inversion.py
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
"""Matrix Inversion / 矩阵求逆

HHL-based matrix inversion for linear systems.
基于 HHL 的线性系统矩阵求逆。

## Application / 应用场景
- Linear systems (线性系统)
- Machine learning (机器学习)
- Optimization (优化)

## Output / 输出
Solution vector.
解向量。"""

from quonic.algorithms import quantum_matrix_inversion_demo

result = quantum_matrix_inversion_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/quantum_matrix_inversion/quantum_matrix_inversion.py
```

---

## 下载

- [quantum_matrix_inversion.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_matrix_inversion/quantum_matrix_inversion.py)
