"""QAOA for MaxCut / QAOA 求解 MaxCut

Reproduce Farhi et al. (2014) MaxCut optimization.
复现 Farhi et al. (2014) MaxCut 优化。

## Application / 应用场景
- Combinatorial optimization (组合优化)
- Graph partitioning (图划分)
- Benchmark (基准测试)

## Output / 输出
MaxCut value ≥ 1.8 on triangle.
三角图上 MaxCut ≥ 1.8。"""

from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, p=1, maxiter=100)
print(f"Max cut: {result.value}")
