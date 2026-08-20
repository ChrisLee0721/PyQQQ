# Stabilizer / Clifford group simulation via stabilizer tableau.

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

Stabilizer Formalism / 稳定子形式

Clifford group simulation via stabilizer tableau.

---

## 快速上手

```python
from quonic.algorithms import stabilizer_demo

result = stabilizer_demo(n_qubits=3, shots=100)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Stabilizer circuit](/images/stabilizer_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import stabilizer_demo

result = stabilizer_demo(n_qubits=3, shots=100)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Error correction (纠错)
- - Clifford simulation (Clifford 模拟)
- - Quantum circuits (量子电路)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/stabilizer/stabilizer.py
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
"""Stabilizer Formalism / 稳定子形式

Clifford group simulation via stabilizer tableau.
通过稳定子表模拟 Clifford 群。

## Application / 应用场景
- Error correction (纠错)
- Clifford simulation (Clifford 模拟)
- Quantum circuits (量子电路)

## Output / 输出
Stabilizer state measurements.
稳定子态测量。"""

from quonic.algorithms import stabilizer_demo

result = stabilizer_demo(n_qubits=3, shots=100)
print(result.counts)

```

### 运行方式

```bash
python examples/stabilizer/stabilizer.py
```

---

## 下载

- [stabilizer.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/stabilizer/stabilizer.py)
