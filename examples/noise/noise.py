"""Noise simulation / 噪声模拟

Noise simulation / 噪声模拟

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=0.05)
