# Superdense Coding / Send 2 classical bits using 1 qubit.

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

Superdense Coding / 超密编码

Send 2 classical bits using 1 qubit.

---

## 快速上手

```python
from quonic.algorithms import superdense_coding

for msg in ["00", "01", "10", "11"]:
    result = superdense_coding(message=msg, shots=100)
    # value is the decoded integer (0-3)
    decoded = f"{int(result.value):02b}"
    print(f"Sent: {msg}, Decoded: {decoded}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Superdense Coding circuit](/images/superdense_coding_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import superdense_coding

for msg in ["00", "01", "10", "11"]:
    result = superdense_coding(message=msg, shots=100)
    # value is the decoded integer (0-3)
    decoded = f"{int(result.value):02b}"
    print(f"Sent: {msg}, Decoded: {decoded}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum communication (量子通信)
- - Bandwidth doubling (带宽翻倍)
- - Teleportation (隐形传态)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/superdense_coding/superdense_coding.py
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
"""Superdense Coding / 超密编码

Send 2 classical bits using 1 qubit.
用 1 个量子比特发送 2 个经典比特。

## Application / 应用场景
- Quantum communication (量子通信)
- Bandwidth doubling (带宽翻倍)
- Teleportation (隐形传态)

## Output / 输出
Decoded 2-bit message.
解码的 2 比特消息。"""

from quonic.algorithms import superdense_coding

for msg in ["00", "01", "10", "11"]:
    result = superdense_coding(message=msg, shots=100)
    # value is the decoded integer (0-3)
    decoded = f"{int(result.value):02b}"
    print(f"Sent: {msg}, Decoded: {decoded}")

```

### 运行方式

```bash
python examples/superdense_coding/superdense_coding.py
```

---

## 下载

- [superdense_coding.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/superdense_coding/superdense_coding.py)
