"""Controlled gates / 受控门

Controlled gates / 受控门"""

from quonic import controlled, qgate, qshow
from quonic.gates import H, Ry

qgate(H, 0)
controlled(Ry(0.7), 0, 1)
qshow()
