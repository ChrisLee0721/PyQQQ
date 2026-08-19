"""Tests for the distributed quantum computing module."""

from __future__ import annotations

from quonic.distributed import EntanglementPair, Node, QuantumNetwork, remote_cnot
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


def test_remote_cnot():
    pair = EntanglementPair(node_a=0, node_b=1)
    c = remote_cnot(pair, control_qubit=0, target_qubit=1)
    assert isinstance(c, Circuit)
    assert len(c.ops) > 0
