"""Diffusion operator / 扩散算子

Diffusion operator / 扩散算子"""

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
