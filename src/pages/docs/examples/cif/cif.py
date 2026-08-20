"""Classical if statement / 经典 if 语句

Classical if statement / 经典 if 语句

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import cif, qgate, qshow
from quonic.gates import H, X, Z

qgate(H, 0)
cif(0).then(X, 1).else_(Z, 1)
qgate(H, 0)
qgate(H, 1)
qshow()
