"""Basic gates: X, Y, Z, CZ, CCX (Toffoli), and explicit MEASURE.

X flips |0> to |1>; Y and Z add phases (invisible in this basis here);
CCX flips a target only when both controls are |1>; CZ is a controlled
phase. qshow() auto-measures any qubit without an explicit MEASURE.

Final state: |110> (qubit 0 = 0, qubits 1 and 2 = 1).
"""

from quonic import qgate, qshow
from quonic.gates import CCX, CZ, MEASURE, X, Y, Z

qgate(X, 0)             # qubit 0 -> |1>
qgate(X, 1)             # qubit 1 -> |1>
qgate(CCX, 0, 1, 2)     # both controls are 1 -> qubit 2 flips to |1>
qgate(CZ, 0, 1)         # phase -1 when both are |1> (invisible)
qgate(Z, 0)             # phase flip on qubit 0 (invisible)
qgate(Y, 2)             # flip qubit 2 back to |0> (with a phase)
qgate(MEASURE, 0)       # explicit measurement; qshow() measures the rest

qshow()
