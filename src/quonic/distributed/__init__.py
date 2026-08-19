"""Distributed quantum computing — multi-chip and quantum network support.

Example::

    from quonic.distributed import QuantumNetwork, EntanglementPair
    network = QuantumNetwork(n_nodes=3)
"""

from .entanglement import (
    EntanglementPair,
    create_bell_pair,
    distribute_entanglement,
    remote_cnot,
    teleport_state,
)
from .network import Node, QuantumNetwork

__all__ = [
    "QuantumNetwork",
    "Node",
    "EntanglementPair",
    "create_bell_pair",
    "distribute_entanglement",
    "remote_cnot",
    "teleport_state",
]
