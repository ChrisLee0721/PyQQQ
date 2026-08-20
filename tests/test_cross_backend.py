"""Cross-backend consistency tests.

Verify that the same circuit produces consistent results across all available backends.
"""

from __future__ import annotations

import pytest

from quonic.ir import Circuit, GateOperation


def _make_bell():
    """Create a Bell state circuit."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))
    return c


def _make_ghz3():
    """Create a GHZ-3 circuit."""
    c = Circuit()
    c.allocate(3)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))
    c.add(GateOperation("cx", (1, 2)))
    return c


def _make_x_gate():
    """Create a single X gate circuit."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("x", (0,)))
    return c


BACKENDS = ["native", "qiskit", "cirq", "pennylane", "qulacs"]


@pytest.mark.parametrize("backend", BACKENDS)
def test_bell_consistency(backend):
    """Bell state should give ~50/50 |00> and |11> on all backends."""
    pytest.importorskip(backend if backend != "native" else "numpy")
    from quonic.backends import get_backend

    c = _make_bell()
    be = get_backend(backend)
    result = be.run(c, shots=1000)
    counts = result.counts

    # Should only have |00> and |11>
    assert set(counts.keys()) <= {"00", "11"}
    # Each should be roughly 50%
    total = sum(counts.values())
    assert 0.3 < counts.get("00", 0) / total < 0.7
    assert 0.3 < counts.get("11", 0) / total < 0.7


@pytest.mark.parametrize("backend", BACKENDS)
def test_x_gate_consistency(backend):
    """X gate should give |1> on all backends."""
    pytest.importorskip(backend if backend != "native" else "numpy")
    from quonic.backends import get_backend

    c = _make_x_gate()
    be = get_backend(backend)
    result = be.run(c, shots=100)
    counts = result.counts

    assert set(counts.keys()) <= {"1"}
    assert counts.get("1", 0) == 100


@pytest.mark.parametrize("backend", BACKENDS)
def test_ghz3_consistency(backend):
    """GHZ-3 should give ~50/50 |000> and |111> on all backends."""
    pytest.importorskip(backend if backend != "native" else "numpy")
    from quonic.backends import get_backend

    c = _make_ghz3()
    be = get_backend(backend)
    result = be.run(c, shots=1000)
    counts = result.counts

    assert set(counts.keys()) <= {"000", "111"}
    total = sum(counts.values())
    assert 0.3 < counts.get("000", 0) / total < 0.7
    assert 0.3 < counts.get("111", 0) / total < 0.7
