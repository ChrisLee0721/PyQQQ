# Syndrome / Extract error syndromes without disturbing encoded state.

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

Syndrome Measurement / Syndrome 测量

Extract error syndromes without disturbing encoded state.

---

## 快速上手

```python
from quonic.algorithms import syndrome_demo

result = syndrome_demo(n_data=3, shots=100)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Syndrome circuit](/images/syndrome_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import syndrome_demo

result = syndrome_demo(n_data=3, shots=100)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Error detection (错误检测)
- - QEC decoding (QEC 解码)
- - Fault tolerance (容错)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/syndrome/syndrome.py
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
"""Syndrome Measurement / Syndrome 测量

Extract error syndromes without disturbing encoded state.
提取错误 syndrome 而不扰动态。

## Application / 应用场景
- Error detection (错误检测)
- QEC decoding (QEC 解码)
- Fault tolerance (容错)

## Output / 输出
Syndrome bits indicating error location.
指示错误位置的 syndrome 比特。"""

from quonic.algorithms import syndrome_demo

result = syndrome_demo(n_data=3, shots=100)
print(result.counts)

```

### 运行方式

```bash
python examples/syndrome/syndrome.py
```

---

## 下载

- [syndrome.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/syndrome/syndrome.py)
