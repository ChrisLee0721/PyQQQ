"""Controlled gates / 受控门

Controlled gates / 受控门

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import controlled, qgate, qshow
from quonic.gates import H, Ry

qgate(H, 0)
controlled(Ry(0.7), 0, 1)
qshow()
