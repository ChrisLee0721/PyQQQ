"""Classical while loop / 经典 while 循环

Classical while loop / 经典 while 循环

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import creg, cwhile, qgate, qshow
from quonic.gates import H

flag = creg("flag")
with cwhile(flag, until=0):
    qgate(H, 0)
    flag.measure(0)

qshow(backend="native")  # cwhile 逐 shot 动态执行，仅 native 后端支持
