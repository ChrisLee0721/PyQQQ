"""Edge case tests for QuoNic.

Tests boundary conditions: empty circuits, single qubit, max qubits, invalid inputs.
"""

from __future__ import annotations

import pytest
import numpy as np

from quonic.ir import Circuit, GateOperation
from quonic.backends.native import NativeBackend


def test_empty_circuit():
    """Empty circuit should return empty result."""
    c = Circuit()
    c.allocate(1)
    be = NativeBackend()
    result = be.run(c, shots=10)
    # Should return |0> with 100%
    assert result.counts.get("0", 0) == 10


def test_single_qubit():
    """Single qubit circuit should work."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("h", (0,)))
    be = NativeBackend()
    result = be.run(c, shots=1000)
    counts = result.counts
    assert set(counts.keys()) <= {"0", "1"}
    total = sum(counts.values())
    assert 0.3 < counts.get("0", 0) / total < 0.7


def test_many_qubits():
    """20-qubit circuit should work (at limit of statevector)."""
    c = Circuit()
    c.allocate(20)
    for q in range(20):
        c.add(GateOperation("h", (q,)))
    be = NativeBackend()
    result = be.run(c, shots=10)
    # Should have many outcomes
    assert len(result.counts) > 1


def test_all_same_gates():
    """All X gates should give all 1s."""
    c = Circuit()
    c.allocate(4)
    for q in range(4):
        c.add(GateOperation("x", (q,)))
    be = NativeBackend()
    result = be.run(c, shots=100)
    assert result.counts.get("1111", 0) == 100


def test_no_measure():
    """Circuit without explicit measure should still work."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))
    be = NativeBackend()
    result = be.run(c, shots=100)
    assert result.counts is not None


def test_repeated_gates():
    """H·H = I, so double H should give original state."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("h", (0,)))
    be = NativeBackend()
    result = be.run(c, shots=100)
    assert result.counts.get("0", 0) == 100


def test_deep_circuit():
    """Deep circuit (many gates) should work."""
    c = Circuit()
    c.allocate(2)
    for _ in range(100):
        c.add(GateOperation("h", (0,)))
        c.add(GateOperation("cx", (0, 1)))
    be = NativeBackend()
    result = be.run(c, shots=10)
    assert result.counts is not None


def test_wide_circuit():
    """Wide circuit (many qubits) with few gates."""
    c = Circuit()
    c.allocate(10)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 9)))
    be = NativeBackend()
    result = be.run(c, shots=1000)
    counts = result.counts
    # Should have |00...0> and |10...01>
    assert len(counts) >= 2
