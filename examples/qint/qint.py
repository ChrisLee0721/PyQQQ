"""Quantum integer / 量子整数

Quantum integer / 量子整数

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import QInt, qshow

x = QInt(3, value=5)  # |5> = |101>
x += 3                # quantum addition: 5 + 3 ≡ 0 (mod 8)
qshow()
