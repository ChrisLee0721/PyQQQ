"""GHZ state: H(0) then CNOT(0,1), CNOT(1,2) gives (|000>+|111>)/√2.

Output: roughly 50% |000> and 50% |111>.
"""

from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()
