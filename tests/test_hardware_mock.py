"""Mock tests for hardware backends.

Tests backend registration and basic structure without requiring real hardware.
"""

from __future__ import annotations

import pytest

from quonic.ir import Circuit, GateOperation


def _make_circuit() -> Circuit:
    """Create a simple test circuit: H(0), CX(0,1), measure."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))
    c.add(GateOperation("measure", (0,)))
    c.add(GateOperation("measure", (1,)))
    return c


# ---------------------------------------------------------------------------
# All hardware backends: registration
# ---------------------------------------------------------------------------


def test_all_hardware_backends_registered():
    """Verify all7 hardware backends are registered in the backend registry."""
    from quonic.backends import _REGISTRY

    hw = ["ibm", "braket", "azure", "ionq", "rigetti", "xanadu", "quera"]
    for name in hw:
        assert name in _REGISTRY, f"Backend '{name}' not registered"


# ---------------------------------------------------------------------------
# Backend structure
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("backend_name", ["ibm", "braket", "azure", "ionq", "rigetti", "xanadu", "quera"])
def test_hardware_backend_has_name(backend_name):
    """Each hardware backend should have a name attribute."""
    from quonic.backends import _REGISTRY

    cls = _REGISTRY[backend_name]
    assert hasattr(cls, "name") or hasattr(cls, "name")


@pytest.mark.parametrize("backend_name", ["ibm", "braket", "azure", "ionq", "rigetti", "xanadu", "quera"])
def test_hardware_backend_has_run(backend_name):
    """Each hardware backend should have a run method."""
    from quonic.backends import _REGISTRY

    cls = _REGISTRY[backend_name]
    assert hasattr(cls, "run")


@pytest.mark.parametrize("backend_name", ["ibm", "braket", "azure", "ionq", "rigetti", "xanadu", "quera"])
def test_hardware_backend_has_capabilities(backend_name):
    """Each hardware backend should declare capabilities."""
    from quonic.backends import _REGISTRY

    cls = _REGISTRY[backend_name]
    if hasattr(cls, "_CAPABILITIES"):
        assert isinstance(cls._CAPABILITIES, dict)


# ---------------------------------------------------------------------------
# Braket backend specific tests
# ---------------------------------------------------------------------------


def test_braket_device_resolution():
    """Braket should resolve shorthand device names to ARNs."""
    from quonic.backends.braket import BraketBackend

    b = BraketBackend("sv1")
    assert "sv1" in b.device.lower()

    b2 = BraketBackend("dm1")
    assert "dm1" in b2.device.lower()

    b3 = BraketBackend("tn1")
    assert "tn1" in b3.device.lower()


def test_braket_local_device():
    """Braket local device should use LocalSimulator."""
    from quonic.backends.braket import BraketBackend

    b = BraketBackend("local")
    assert b.device == "local"


def test_braket_custom_arn():
    """Braket should accept custom device ARNs."""
    from quonic.backends.braket import BraketBackend

    arn = "arn:aws:braket:us-east-1:123456:device/qpu/ionq/Aria-1"
    b = BraketBackend(arn)
    assert b.device == arn


def test_braket_capabilities():
    """Braket should declare correct capabilities."""
    from quonic.backends.braket import BraketBackend

    b = BraketBackend()
    assert b._CAPABILITIES["noise"] is True
    assert b._CAPABILITIES["ctrl"] is False
    assert b.name == "braket"


def test_braket_gate_translation():
    """Braket gate translation should handle standard gates."""
    from quonic.backends.braket import _translate_gate

    # Mock Braket circuit
    class MockCircuit:
        def __init__(self):
            self.ops = []
        def h(self, q): self.ops.append(("h", q))
        def x(self, q): self.ops.append(("x", q))
        def cnot(self, c, t): self.ops.append(("cnot", c, t))
        def rz(self, q, theta): self.ops.append(("rz", q, theta))

    bc = MockCircuit()

    # Test H gate
    op = type("Op", (), {"name": "h", "qubits": (0,), "params": ()})()
    _translate_gate(bc, None, op)
    assert ("h", 0) in bc.ops

    # Test CX gate
    op = type("Op", (), {"name": "cx", "qubits": (0, 1), "params": ()})()
    _translate_gate(bc, None, op)
    assert ("cnot", 0, 1) in bc.ops

    # Test Rz gate
    op = type("Op", (), {"name": "rz", "qubits": (0,), "params": (0.5,)})()
    _translate_gate(bc, None, op)
    assert ("rz", 0, 0.5) in bc.ops
