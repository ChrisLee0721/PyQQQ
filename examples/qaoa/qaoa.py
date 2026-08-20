"""QAOA algorithm / QAOA 算法

QAOA algorithm / QAOA 算法

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)
print(result.value)  # ≈ 2.0
