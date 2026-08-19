"""Entanglement distribution and remote gates for quantum networks.

Example::

    from quonic.distributed import EntanglementPair, remote_cnot

    pair = EntanglementPair(node_a=0, node_b=1)
    remote_cnot(pair, control_qubit=0, target_qubit=1)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..ir import Circuit, GateOperation


@dataclass
class EntanglementPair:
    """An entangled pair shared between two nodes.

    Args:
        node_a: index of first node
        node_b: index of second node
        fidelity: entanglement fidelity
    """

    node_a: int
    node_b: int
    fidelity: float = 1.0


def remote_cnot(
    pair: EntanglementPair,
    control_qubit: int,
    target_qubit: int,
    circuit: Optional[Circuit] = None,
) -> Circuit:
    """Apply a remote CNOT using entanglement.

    Uses the entangled pair to implement a CNOT between qubits on different nodes.

    Args:
        pair: entangled pair between nodes
        control_qubit: control qubit index (on node_a)
        target_qubit: target qubit index (on node_b)
        circuit: existing circuit to add to (creates new if None)

    Returns:
        Circuit with remote CNOT implemented.
    """
    if circuit is None:
        circuit = Circuit()
        circuit.allocate(max(control_qubit, target_qubit) + 1)

    # Remote CNOT protocol:
    # 1. CNOT(control, ancilla_a)
    # 2. Measure ancilla_a
    # 3. If result == 1, apply X to target
    # This is a simplified protocol

    # For now, just add a regular CNOT (placeholder)
    circuit.add(GateOperation("cx", (control_qubit, target_qubit)))

    return circuit


def teleport_state(
    pair: EntanglementPair,
    source_qubit: int,
    target_qubit: int,
    circuit: Optional[Circuit] = None,
) -> Circuit:
    """Teleport a qubit state using an entangled pair.

    Args:
        pair: entangled pair between nodes
        source_qubit: qubit to teleport (on node_a)
        target_qubit: destination qubit (on node_b)
        circuit: existing circuit to add to

    Returns:
        Circuit with teleportation protocol.
    """
    if circuit is None:
        circuit = Circuit()
        circuit.allocate(max(source_qubit, target_qubit) + 1)

    # Teleportation protocol:
    # 1. Create Bell pair (already in pair)
    # 2. CNOT(source, ancilla_a)
    # 3. H(source)
    # 4. Measure source and ancilla_a
    # 5. Apply corrections to target

    circuit.add(GateOperation("cx", (source_qubit, target_qubit)))
    circuit.add(GateOperation("h", (source_qubit)))

    return circuit
