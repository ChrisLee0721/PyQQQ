# Qaoa Mis / QAOA for MIS: find largest set of non-adjacent vertices.

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

Maximum Independent Set / 最大独立集

QAOA for MIS: find largest set of non-adjacent vertices.

---

## 快速上手

```python
from quonic.algorithms import qaoa_mis

edges = [(0, 1), (1, 2)]
result = qaoa_mis(edges, 3, p=1, maxiter=100)
print(f"MIS size: {result.value}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qaoa Mis circuit](/images/qaoa_mis_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qaoa_mis

edges = [(0, 1), (1, 2)]
result = qaoa_mis(edges, 3, p=1, maxiter=100)
print(f"MIS size: {result.value}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Graph theory (图论)
- - Scheduling (调度)
- - Resource allocation (资源分配)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qaoa_mis/qaoa_mis.py
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
"""Maximum Independent Set / 最大独立集

QAOA for MIS: find largest set of non-adjacent vertices.
QAOA 求解最大独立集：找到最大的非相邻顶点集。

## Application / 应用场景
- Graph theory (图论)
- Scheduling (调度)
- Resource allocation (资源分配)

## Output / 输出
Approximate MIS size.
近似最大独立集大小。"""

from quonic.algorithms import qaoa_mis

edges = [(0, 1), (1, 2)]
result = qaoa_mis(edges, 3, p=1, maxiter=100)
print(f"MIS size: {result.value}")

```

### 运行方式

```bash
python examples/qaoa_mis/qaoa_mis.py
```

---

## 下载

- [qaoa_mis.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa_mis/qaoa_mis.py)
