"""MaxCut problem / 最大割问题

QAOA for MaxCut: partition graph to maximize edges between sets.
QAOA 求解最大割：划分图以最大化集合间边数。

## Application / 应用场景
- Graph partitioning (图划分)
- Network design (网络设计)
- Clustering (聚类)

## Output / 输出
Approximate max cut value.
近似最大割值。"""

from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, p=1, maxiter=100)
print(f"Max cut: {result.value}")
