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
