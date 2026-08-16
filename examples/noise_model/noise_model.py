"""NoiseModel: separate single- and two-qubit depolarizing rates.

On a Bell state, 1% single-qubit and 5% two-qubit depolarizing noise
leaks a little population into |01> and |10> (zero without noise).
"""

from quonic import NoiseModel, qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=NoiseModel(single=0.01, double=0.05))
