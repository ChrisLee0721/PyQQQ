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
