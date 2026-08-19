"""Distributed quantum computing — multi-chip and quantum network support.

Example::

    from quonic.distributed import QuantumNetwork, EntanglementPair
    network = QuantumNetwork(n_nodes=3)
"""

from .entanglement import EntanglementPair, remote_cnot
from .network import Node, QuantumNetwork

__all__ = [
    "QuantumNetwork",
    "Node",
    "EntanglementPair",
    "remote_cnot",
]
