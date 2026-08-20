# Qaoa Tsp / QAOA for TSP: find shortest route visiting all cities.

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

Traveling Salesman Problem / 旅行商问题

QAOA for TSP: find shortest route visiting all cities.

---

## 快速上手

```python
from quonic.algorithms import qaoa_tsp

distances = {
    (0, 1): 1.0, (1, 0): 1.0,
    (1, 2): 2.0, (2, 1): 2.0,
    (0, 2): 1.5, (2, 0): 1.5,
}
result = qaoa_tsp(distances, 3, p=1, maxiter=100)
print(f"Tour cost: {result.value}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qaoa Tsp circuit](/images/qaoa_tsp_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qaoa_tsp

distances = {
    (0, 1): 1.0, (1, 0): 1.0,
    (1, 2): 2.0, (2, 1): 2.0,
    (0, 2): 1.5, (2, 0): 1.5,
}
result = qaoa_tsp(distances, 3, p=1, maxiter=100)
print(f"Tour cost: {result.value}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Logistics (物流)
- - Route planning (路线规划)
- - Circuit design (电路设计)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qaoa_tsp/qaoa_tsp.py
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
"""Traveling Salesman Problem / 旅行商问题

QAOA for TSP: find shortest route visiting all cities.
QAOA 求解 TSP：找到访问所有城市的最短路线。

## Application / 应用场景
- Logistics (物流)
- Route planning (路线规划)
- Circuit design (电路设计)

## Output / 输出
Approximate tour cost.
近似旅行成本。"""

from quonic.algorithms import qaoa_tsp

distances = {
    (0, 1): 1.0, (1, 0): 1.0,
    (1, 2): 2.0, (2, 1): 2.0,
    (0, 2): 1.5, (2, 0): 1.5,
}
result = qaoa_tsp(distances, 3, p=1, maxiter=100)
print(f"Tour cost: {result.value}")

```

### 运行方式

```bash
python examples/qaoa_tsp/qaoa_tsp.py
```

---

## 下载

- [qaoa_tsp.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa_tsp/qaoa_tsp.py)
