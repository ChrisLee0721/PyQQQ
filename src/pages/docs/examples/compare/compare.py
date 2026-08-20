"""Compare backends / 比较后端

Compare backends / 比较后端

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import QInt, qlt, qshow

x = QInt(3)
x.h()            # uniform superposition |0>..|7>
flag = qlt(x, 4) # flag = 1 iff x < 4

qshow()
