"""Quantum if: qif(0).then(X,1).else_(I,1) is a controlled-X (CNOT).

The control qubit is NOT measured; the two branches superpose coherently,
producing true entanglement (not a measure-then-branch mixed state).
Output: same as the Bell state, roughly 50% |00> and 50% |11>.
"""

from quonic import qgate, qif, qshow
from quonic.gates import H, I, X

qgate(H, 0)
qif(0).then(X, 1).else_(I, 1)
qshow()
