# Qaoa Knapsack / QAOA for knapsack: maximize value within weight limit.

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

Knapsack problem / 背包问题

QAOA for knapsack: maximize value within weight limit.

---

## 快速上手

```python
from quonic.algorithms import qaoa_knapsack

weights = [2, 3, 4]
values = [3, 4, 5]
capacity = 5
result = qaoa_knapsack(weights, values, capacity, p=1, maxiter=100)
print(f"Optimal value: {result.value}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qaoa Knapsack circuit](/images/qaoa_knapsack_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qaoa_knapsack

weights = [2, 3, 4]
values = [3, 4, 5]
capacity = 5
result = qaoa_knapsack(weights, values, capacity, p=1, maxiter=100)
print(f"Optimal value: {result.value}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Combinatorial optimization (组合优化)
- - Resource allocation (资源分配)
- - Logistics (物流)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qaoa_knapsack/qaoa_knapsack.py
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
"""Knapsack problem / 背包问题

QAOA for knapsack: maximize value within weight limit.
QAOA 求解背包问题：在重量限制内最大化价值。

## Application / 应用场景
- Combinatorial optimization (组合优化)
- Resource allocation (资源分配)
- Logistics (物流)

## Output / 输出
Optimal subset of items.
最优物品子集。"""

from quonic.algorithms import qaoa_knapsack

weights = [2, 3, 4]
values = [3, 4, 5]
capacity = 5
result = qaoa_knapsack(weights, values, capacity, p=1, maxiter=100)
print(f"Optimal value: {result.value}")

```

### 运行方式

```bash
python examples/qaoa_knapsack/qaoa_knapsack.py
```

---

## 下载

- [qaoa_knapsack.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa_knapsack/qaoa_knapsack.py)
