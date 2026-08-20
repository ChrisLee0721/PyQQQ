"""Quantum Phase Estimation / 量子相位估计

Quantum Phase Estimation / 量子相位估计

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

import math

from quonic.algorithms import qpe

result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)  # dominated by "...010" (rightmost 3 bits -> j = 2)
