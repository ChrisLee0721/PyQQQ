"""Shor's algorithm / Shor 算法

Shor's algorithm / Shor 算法

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic.algorithms import shor

result = shor(15, a=7, t=6, shots=256)
print(result.value)                    # 3 or 5
print(result.metadata["period"])       # 4 (the order of 7 mod 15)
