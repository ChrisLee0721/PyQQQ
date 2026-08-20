# Qtransformer / Quantum attention mechanism for sequence modeling.

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

Quantum Transformer / 量子 Transformer

Quantum attention mechanism for sequence modeling.

---

## 快速上手

```python
from quonic.algorithms import qtransformer_demo

result = qtransformer_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qtransformer circuit](/images/qtransformer_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qtransformer_demo

result = qtransformer_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - NLP (自然语言处理)
- - Sequence modeling (序列建模)
- - Quantum ML (量子机器学习)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qtransformer/qtransformer.py
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
"""Quantum Transformer / 量子 Transformer

Quantum attention mechanism for sequence modeling.
用于序列建模的量子注意力机制。

## Application / 应用场景
- NLP (自然语言处理)
- Sequence modeling (序列建模)
- Quantum ML (量子机器学习)

## Output / 输出
Attention weights.
注意力权重。"""

from quonic.algorithms import qtransformer_demo

result = qtransformer_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/qtransformer/qtransformer.py
```

---

## 下载

- [qtransformer.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qtransformer/qtransformer.py)
