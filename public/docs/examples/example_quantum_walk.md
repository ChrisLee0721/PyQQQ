# Quantum Walk / Quantum analogue of random walk, spreads quadratically faster.

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

Quantum Walk / 量子行走

Quantum analogue of random walk, spreads quadratically faster.

---

## 快速上手

```python
from quonic.algorithms import quantum_walk

result = quantum_walk(n_positions=5, steps=10, shots=1024)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Quantum Walk circuit](/images/quantum_walk_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import quantum_walk

result = quantum_walk(n_positions=5, steps=10, shots=1024)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Search algorithms (搜索算法)
- - Graph algorithms (图算法)
- - Transport phenomena (输运现象)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/quantum_walk/quantum_walk.py
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
"""Quantum Walk / 量子行走

Quantum analogue of random walk, spreads quadratically faster.
随机行走的量子类比，二次方更快扩展。

## Application / 应用场景
- Search algorithms (搜索算法)
- Graph algorithms (图算法)
- Transport phenomena (输运现象)

## Output / 输出
Position distribution after n steps.
n 步后的位置分布。"""

from quonic.algorithms import quantum_walk

result = quantum_walk(n_positions=5, steps=10, shots=1024)
print(result.counts)

```

### 运行方式

```bash
python examples/quantum_walk/quantum_walk.py
```

---

## 下载

- [quantum_walk.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_walk/quantum_walk.py)
