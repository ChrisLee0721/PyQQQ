# QAOA Knapsack / QAOA 背包问题

> **Algorithms** / 算法

## Overview / 概述

Knapsack problem / 背包问题

QAOA for knapsack: maximize value within weight limit.

## Application / 应用场景

- Combinatorial optimization (组合优化)
- Resource allocation (资源分配)
- Logistics (物流)

## Code / 代码

```python
from quonic.algorithms import qaoa_knapsack

weights = [2, 3, 4]
values = [3, 4, 5]
capacity = 5
result = qaoa_knapsack(weights, values, capacity, p=1, maxiter=100)
print(f"Optimal value: {result.value}")
```

## Run / 运行

```bash
python examples/qaoa_knapsack/qaoa_knapsack.py
```

## Download / 下载

[qaoa_knapsack.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa_knapsack/qaoa_knapsack.py)
