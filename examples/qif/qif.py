"""Quantum if / 量子 if

Quantum if / 量子 if"""

from quonic import qgate, qif, qshow
from quonic.gates import H, I, X

qgate(H, 0)
qif(0).then(X, 1).else_(I, 1)
qshow()
