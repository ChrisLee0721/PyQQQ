"""Controlled single-qubit gate: controlled(Ry(0.7), 0, 1).

A general controlled-U (here U = Ry(0.7)) is compiled to basic gates via
ZYZ decomposition, realizing |0><0|⊗I + |1><1|⊗Ry. controlled(X, 0, 1)
is a CNOT; this example shows a parametric rotation instead.
"""

from quonic import controlled, qgate, qshow
from quonic.gates import H, Ry

qgate(H, 0)
controlled(Ry(0.7), 0, 1)
qshow()
