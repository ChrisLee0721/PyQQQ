"""Tests for the distributed quantum computing module."""

from __future__ import annotations

from quonic.distributed import (
    EntanglementPair,
    Node,
    QuantumNetwork,
    create_bell_pair,
    distribute_entanglement,
    remote_cnot,
    teleport_state,
)
from quonic.ir import Circuit

# ---------------------------------------------------------------------------
# 1. Quantum network
# ---------------------------------------------------------------------------


def test_quantum_network_star():
    network = QuantumNetwork(n_nodes=3, topology="star")
    assert len(network.nodes) == 3
    assert network.get_neighbors("node_0") == ["node_1", "node_2"]
    assert network.get_neighbors("node_1") == ["node_0"]


def test_quantum_network_ring():
    network = QuantumNetwork(n_nodes=3, topology="ring")
    assert network.get_neighbors("node_0") == ["node_1"]
    assert network.get_neighbors("node_1") == ["node_2"]
    assert network.get_neighbors("node_2") == ["node_0"]


def test_quantum_network_linear():
    network = QuantumNetwork(n_nodes=3, topology="linear")
    assert network.get_neighbors("node_0") == ["node_1"]
    assert network.get_neighbors("node_1") == ["node_0", "node_2"]
    assert network.get_neighbors("node_2") == ["node_1"]


# ---------------------------------------------------------------------------
# 2. Node
# ---------------------------------------------------------------------------


def test_node_creation():
    node = Node("alice", 4)
    assert node.name == "alice"
    assert node.n_qubits == 4
    assert node.backend == "native"


# ---------------------------------------------------------------------------
# 3. Entanglement
# ---------------------------------------------------------------------------


def test_entanglement_pair():
    pair = EntanglementPair(node_a=0, node_b=1)
    assert pair.node_a == 0
    assert pair.node_b == 1
    assert pair.fidelity == 1.0


def test_create_bell_pair():
    """Bell pair creation should add H and CX gates."""
    c = Circuit()
    c.allocate(2)
    create_bell_pair(c, 0, 1)
    ops = [op for op in c.ops if op.name != "measure"]
    assert len(ops) == 2
    assert ops[0].name == "h"
    assert ops[1].name == "cx"


def test_distribute_entanglement():
    """distribute_entanglement should return a valid pair."""
    c = Circuit()
    c.allocate(4)
    pair = distribute_entanglement(c, 0, 3, fidelity=0.95)
    assert pair.ancilla_a == 0
    assert pair.ancilla_b == 3
    assert pair.fidelity == 0.95


def test_remote_cnot():
    """Remote CNOT should produce a circuit with corrections."""
    pair = EntanglementPair(node_a=0, node_b=1, ancilla_a=2, ancilla_b=3)
    c = remote_cnot(pair, control_qubit=0, target_qubit=1)
    assert c.num_qubits >= 4
    ops = [op for op in c.ops if op.name != "measure"]
    assert len(ops) >= 2


def test_teleport_state():
    """Teleportation should produce a circuit with H and corrections."""
    pair = EntanglementPair(node_a=0, node_b=1, ancilla_a=2, ancilla_b=3)
    c = teleport_state(pair, source_qubit=0, target_qubit=1)
    assert c.num_qubits >= 4
    ops = [op for op in c.ops if op.name != "measure"]
    assert any(op.name == "h" for op in ops)
    assert any(op.name == "cx" for op in ops)
