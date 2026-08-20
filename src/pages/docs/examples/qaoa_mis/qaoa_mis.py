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
