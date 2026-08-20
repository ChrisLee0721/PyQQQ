"""Quantum if / 量子 if

Quantum if / 量子 if

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import qgate, qif, qshow
from quonic.gates import H, I, X

qgate(H, 0)
qif(0).then(X, 1).else_(I, 1)
qshow()
