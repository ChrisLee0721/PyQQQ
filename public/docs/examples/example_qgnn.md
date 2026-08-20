# Qgnn / Quantum GNN for graph-structured data.

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

Quantum Graph Neural Network / 量子图神经网络

Quantum GNN for graph-structured data.

---

## 快速上手

```python
from quonic.algorithms import qgnn_demo

result = qgnn_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qgnn circuit](/images/qgnn_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qgnn_demo

result = qgnn_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Graph classification (图分类)
- - Molecular property prediction (分子性质预测)
- - Social networks (社交网络)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qgnn/qgnn.py
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
"""Quantum Graph Neural Network / 量子图神经网络

Quantum GNN for graph-structured data.
量子 GNN 用于图结构数据。

## Application / 应用场景
- Graph classification (图分类)
- Molecular property prediction (分子性质预测)
- Social networks (社交网络)

## Output / 输出
Graph/node embeddings.
图/节点嵌入。"""

from quonic.algorithms import qgnn_demo

result = qgnn_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/qgnn/qgnn.py
```

---

## 下载

- [qgnn.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qgnn/qgnn.py)
