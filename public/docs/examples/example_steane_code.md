# Steane Code / [[7,1,3]] CSS code, corrects arbitrary single-qubit errors.

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

Steane Code / Steane 码

[[7,1,3]] CSS code, corrects arbitrary single-qubit errors.

---

## 快速上手

```python
from quonic.algorithms import steane_code

result = steane_code(error_qubit=0, shots=100)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Steane Code circuit](/images/steane_code_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import steane_code

result = steane_code(error_qubit=0, shots=100)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum error correction (量子纠错)
- - Fault tolerance (容错)
- - Logical gates (逻辑门)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/steane_code/steane_code.py
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
"""Steane Code / Steane 码

[[7,1,3]] CSS code, corrects arbitrary single-qubit errors.
[[7,1,3]] CSS 码，纠正任意单比特错误。

## Application / 应用场景
- Quantum error correction (量子纠错)
- Fault tolerance (容错)
- Logical gates (逻辑门)

## Output / 输出
Corrected logical qubit.
纠正后的逻辑比特。"""

from quonic.algorithms import steane_code

result = steane_code(error_qubit=0, shots=100)
print(result.counts)

```

### 运行方式

```bash
python examples/steane_code/steane_code.py
```

---

## 下载

- [steane_code.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/steane_code/steane_code.py)
