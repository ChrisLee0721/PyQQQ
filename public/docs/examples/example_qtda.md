# Qtda / Quantum algorithm for persistent homology.

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

Quantum Topological Data Analysis / 量子拓扑数据分析

Quantum algorithm for persistent homology.

---

## 快速上手

```python
from quonic.algorithms import qtda_demo

result = qtda_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qtda circuit](/images/qtda_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qtda_demo

result = qtda_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Data analysis (数据分析)
- - Shape recognition (形状识别)
- - Topology (拓扑学)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qtda/qtda.py
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
"""Quantum Topological Data Analysis / 量子拓扑数据分析

Quantum algorithm for persistent homology.
持续同调的量子算法。

## Application / 应用场景
- Data analysis (数据分析)
- Shape recognition (形状识别)
- Topology (拓扑学)

## Output / 输出
Topological features.
拓扑特征。"""

from quonic.algorithms import qtda_demo

result = qtda_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/qtda/qtda.py
```

---

## 下载

- [qtda.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qtda/qtda.py)
