# Quantum Clustering / Quantum algorithm for unsupervised clustering.

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

Quantum Clustering / 量子聚类

Quantum algorithm for unsupervised clustering.

---

## 快速上手

```python
from quonic.algorithms import quantum_clustering_demo

result = quantum_clustering_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Quantum Clustering circuit](/images/quantum_clustering_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import quantum_clustering_demo

result = quantum_clustering_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Data analysis (数据分析)
- - Customer segmentation (客户细分)
- - Anomaly detection (异常检测)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/quantum_clustering/quantum_clustering.py
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
"""Quantum Clustering / 量子聚类

Quantum algorithm for unsupervised clustering.
无监督聚类的量子算法。

## Application / 应用场景
- Data analysis (数据分析)
- Customer segmentation (客户细分)
- Anomaly detection (异常检测)

## Output / 输出
Cluster assignments.
聚类分配。"""

from quonic.algorithms import quantum_clustering_demo

result = quantum_clustering_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/quantum_clustering/quantum_clustering.py
```

---

## 下载

- [quantum_clustering.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_clustering/quantum_clustering.py)
