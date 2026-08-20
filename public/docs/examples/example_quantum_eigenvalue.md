# Quantum Eigenvalue / Estimate eigenvalues of unitary operators.

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

Eigenvalue Estimation / 特征值估计

Estimate eigenvalues of unitary operators.

---

## 快速上手

```python
from quonic.algorithms import quantum_eigenvalue_demo

result = quantum_eigenvalue_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Quantum Eigenvalue circuit](/images/quantum_eigenvalue_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import quantum_eigenvalue_demo

result = quantum_eigenvalue_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum chemistry (量子化学)
- - Physics (物理学)
- - Linear algebra (线性代数)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/quantum_eigenvalue/quantum_eigenvalue.py
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
"""Eigenvalue Estimation / 特征值估计

Estimate eigenvalues of unitary operators.
估计酉算子的特征值。

## Application / 应用场景
- Quantum chemistry (量子化学)
- Physics (物理学)
- Linear algebra (线性代数)

## Output / 输出
Eigenvalue estimates.
特征值估计。"""

from quonic.algorithms import quantum_eigenvalue_demo

result = quantum_eigenvalue_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/quantum_eigenvalue/quantum_eigenvalue.py
```

---

## 下载

- [quantum_eigenvalue.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_eigenvalue/quantum_eigenvalue.py)
