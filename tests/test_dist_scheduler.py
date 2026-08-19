"""Tests for distributed quantum task scheduler."""

from __future__ import annotations

from quonic.distributed import QuantumNetwork, schedule_task
from quonic.ir import Circuit, GateOperation


def test_schedule_local_circuit():
    """Circuit with local gates should have no entanglement pairs."""
    network = QuantumNetwork(n_nodes=2, topology="star")
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("x", (1,)))

    schedule = schedule_task(c, network, {0: "node_0", 1: "node_1"})
    assert schedule.entanglement_pairs == 0


def test_schedule_cross_node_circuit():
    """Circuit with cross-node gates should need entanglement."""
    network = QuantumNetwork(n_nodes=2, topology="star")
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("cx", (0, 1)))

    schedule = schedule_task(c, network, {0: "node_0", 1: "node_1"})
    assert schedule.entanglement_pairs >= 1


def test_schedule_auto_assign():
    """Auto-assignment should distribute qubits round-robin."""
    network = QuantumNetwork(n_nodes=2, topology="star")
    c = Circuit()
    c.allocate(4)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("h", (1,)))

    schedule = schedule_task(c, network)
    assert len(schedule.steps) > 0


def test_task_schedule_repr():
    """TaskSchedule should have a readable repr."""
    network = QuantumNetwork(n_nodes=2, topology="star")
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("h", (0,)))

    schedule = schedule_task(c, network)
    r = repr(schedule)
    assert "TaskSchedule" in r
