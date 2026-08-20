"""Basic quantum gates demonstration / 基本量子门演示

Basic quantum gates demonstration / 基本量子门演示

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import qgate, qshow
from quonic.gates import CCX, CZ, MEASURE, X, Y, Z

qgate(X, 0)             # qubit 0 -> |1>
qgate(X, 1)             # qubit 1 -> |1>
qgate(CCX, 0, 1, 2)     # both controls are 1 -> qubit 2 flips to |1>
qgate(CZ, 0, 1)         # phase -1 when both are |1> (invisible)
qgate(Z, 0)             # phase flip on qubit 0 (invisible)
qgate(Y, 2)             # flip qubit 2 back to |0> (with a phase)
qgate(MEASURE, 0)       # explicit measurement; qshow() measures the rest

qshow()
