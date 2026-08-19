"""Quantum Machine Learning — variational circuits, data encoding, and optimizers.

Example::

    from quonic.ml import Ansatz, angle_encode, SPSAOptimizer
    from quonic.ml import expectation_loss, train

    ansatz = Ansatz.hardware_efficient(n_qubits=4, layers=3)
    encoded = angle_encode(features)
    opt = SPSAOptimizer(maxiter=100)
    result = train(ansatz, encoded, opt, observable="ZZZZ")
"""

from .ansatz import Ansatz
from .encoding import amplitude_encode, angle_encode, iqp_encode
from .loss import cross_entropy_loss, expectation_loss, fidelity_loss
from .optimizer import AdamOptimizer, QNGOptimizer, SPSAOptimizer
from .trainer import train

__all__ = [
    "Ansatz",
    "angle_encode",
    "amplitude_encode",
    "iqp_encode",
    "expectation_loss",
    "fidelity_loss",
    "cross_entropy_loss",
    "SPSAOptimizer",
    "AdamOptimizer",
    "QNGOptimizer",
    "train",
]
