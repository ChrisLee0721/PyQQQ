"""GHZ state / GHZ 态

GHZ state / GHZ 态"""

from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()
