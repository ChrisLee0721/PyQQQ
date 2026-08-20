# Ft Gate / Gates implemented with error detection/correction.

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

Fault-tolerant gates / 容错门

Gates implemented with error detection/correction.

---

## 快速上手

```python
from quonic.algorithms import ft_gate_demo

result = ft_gate_demo(shots=100)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Ft Gate circuit](/images/ft_gate_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import ft_gate_demo

result = ft_gate_demo(shots=100)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Fault-tolerant computing (容错计算)
- - Quantum error correction (量子纠错)
- - Logical gates (逻辑门)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/ft_gate/ft_gate.py
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
"""Fault-tolerant gates / 容错门

Gates implemented with error detection/correction.
带有错误检测/纠正的门实现。

## Application / 应用场景
- Fault-tolerant computing (容错计算)
- Quantum error correction (量子纠错)
- Logical gates (逻辑门)

## Output / 输出
Logically encoded state with error protection.
具有错误保护的逻辑编码态。"""

from quonic.algorithms import ft_gate_demo

result = ft_gate_demo(shots=100)
print(result.counts)

```

### 运行方式

```bash
python examples/ft_gate/ft_gate.py
```

---

## 下载

- [ft_gate.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/ft_gate/ft_gate.py)
