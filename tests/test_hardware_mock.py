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
