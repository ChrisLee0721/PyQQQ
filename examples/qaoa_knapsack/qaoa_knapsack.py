"""QAOA for the knapsack problem.

Finds the optimal subset of items maximizing value within weight capacity.
Output: approximate optimal value.
"""

from quonic.algorithms import qaoa_knapsack

weights = [2, 3, 4]
values = [3, 4, 5]
capacity = 5
result = qaoa_knapsack(weights, values, capacity, p=1, maxiter=100)
print(f"Optimal value: {result.value}")
