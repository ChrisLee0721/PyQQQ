"""Mark state / 标记态

Mark state / 标记态

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic.algorithms import grover, mark_state

result = grover(mark_state("10"), 2, shots=1024)
print(result.counts)  # dominated by |10>
