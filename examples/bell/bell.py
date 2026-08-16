"""Bell state: H(0) then CNOT(0,1) creates maximal entanglement (|00>+|11>)/√2.

Output: roughly 50% |00> and 50% |11>.
"""

from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
