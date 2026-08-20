"""Diffusion operator / 扩散算子

Diffusion operator / 扩散算子

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import qgate, qshow
from quonic.algorithms import diffusion, mark_state
from quonic.gates import H
from quonic.stack import current_circuit

n = 2
for q in range(n):
    qgate(H, q)
mark_state("11")(current_circuit())  # 相位标记 |11>
diffusion(n)                          # 一次振幅放大
qshow()
