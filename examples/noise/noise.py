"""Depolarizing noise on a Bell state.

5% depolarizing after each gate leaks population into |01> and |10>.
"""

from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=0.05)
