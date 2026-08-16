"""Classical if: cif(0).then(X,1).else_(Z,1) measures then branches.

Unlike qif (quantum superposition if), cif MEASURES the control qubit first,
producing a classical mixed state — no entanglement. With the control in
superposition, the final H⊗H rotation spreads counts across all four basis
states (~25% each), the signature of a mixture rather than a Bell state.
"""

from quonic import cif, qgate, qshow
from quonic.gates import H, X, Z

qgate(H, 0)
cif(0).then(X, 1).else_(Z, 1)
qgate(H, 0)
qgate(H, 1)
qshow()
