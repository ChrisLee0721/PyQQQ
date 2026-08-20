"""Quantum Counting / 量子计数

Quantum Counting / 量子计数

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic.algorithms import oracle, quantum_counting


@oracle(3)
def even(x):
    return x & 1 == 0


result = quantum_counting(even, 3, shots=2048)
print(result.value)  # ~ 4
