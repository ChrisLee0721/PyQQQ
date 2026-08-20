# From Qiskit Nature / Convert from Qiskit Nature / 从 Qiskit Nature 转换

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

Convert from Qiskit Nature / 从 Qiskit Nature 转换

Convert from Qiskit Nature / 从 Qiskit Nature 转换

---

## 快速上手

```python
from qiskit.quantum_info import SparsePauliOp

from quonic.algorithms import from_qiskit_nature, vqe

op = SparsePauliOp.from_list([("ZZ", 1.0), ("XI", 1.0), ("IX", 1.0)])
terms = from_qiskit_nature(op)
print(terms)  # [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]

result = vqe(terms, 2, maxiter=200)
print(result.value)  # ~ -2.236
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![From Qiskit Nature circuit](/images/from_qiskit_nature_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from qiskit.quantum_info import SparsePauliOp

from quonic.algorithms import from_qiskit_nature, vqe

op = SparsePauliOp.from_list([("ZZ", 1.0), ("XI", 1.0), ("IX", 1.0)])
terms = from_qiskit_nature(op)
print(terms)  # [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]

result = vqe(terms, 2, maxiter=200)
print(result.value)  # ~ -2.236
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum computing (量子计算)
- - Algorithm demonstration (算法演示)
- - Educational (教学)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/from_qiskit_nature/from_qiskit_nature.py
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
"""Convert from Qiskit Nature / 从 Qiskit Nature 转换

Convert from Qiskit Nature / 从 Qiskit Nature 转换

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from qiskit.quantum_info import SparsePauliOp

from quonic.algorithms import from_qiskit_nature, vqe

op = SparsePauliOp.from_list([("ZZ", 1.0), ("XI", 1.0), ("IX", 1.0)])
terms = from_qiskit_nature(op)
print(terms)  # [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]

result = vqe(terms, 2, maxiter=200)
print(result.value)  # ~ -2.236

```

### 运行方式

```bash
python examples/from_qiskit_nature/from_qiskit_nature.py
```

---

## 下载

- [from_qiskit_nature.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/from_qiskit_nature/from_qiskit_nature.py)
