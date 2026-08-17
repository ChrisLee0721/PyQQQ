"""Noise injection tests for engine backends.

Tests that backends with density-matrix support correctly inject
depolarizing noise and produce expected leakage in deterministic circuits.
"""

from __future__ import annotations

import pytest

from quonic import NoiseModel, qgate, reset
from quonic.backends import get_backend
from quonic.gates import CX, H, X
from quonic.stack import current_circuit

BACKENDS = [
    "qulacs",
    "tensorcircuit",
    "cudaq",
    "mindquantum",
    "qpanda",
    "cqlib",
]

_MODULE_MAP = {
    "qpanda": "pyqpanda3",
}


def _import_backend(backend: str):
    if backend == "tensorcircuit":
        from quonic.backends.tensorcircuit import _patch_numpy_for_tensorcircuit

        _patch_numpy_for_tensorcircuit()
    mod = _MODULE_MAP.get(backend, backend)
    return pytest.importorskip(mod)


# ---------------------------------------------------------------------------
# 1. Depolarizing noise on a deterministic circuit (X gate)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("backend", BACKENDS)
def test_noise_x_gate(backend):
    """X|0> = |1> with noise should sometimes produce |0>."""
    _import_backend(backend)
    reset()
    qgate(X, 0)
    be = get_backend(backend)
    shots = 512  # reduced for slow backends (TensorCircuit DMCircuit)
    try:
        result = be.run(current_circuit(), shots=shots, noise=0.1)
    except NotImplementedError:
        pytest.skip(f"{backend} does not support noise")
    # With 10% depolarizing, ~10% of shots should flip back to |0>
    p0 = result.counts.get("0", 0) / shots
    assert p0 > 0.01  # some leakage
    assert p0 < 0.30  # not too much


# ---------------------------------------------------------------------------
# 2. Readout noise on a deterministic circuit
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("backend", BACKENDS)
def test_readout_noise(backend):
    """Readout noise should flip measured bits."""
    _import_backend(backend)
    reset()
    qgate(X, 0)  # |1>
    be = get_backend(backend)
    shots = 512
    nm = NoiseModel(readout=0.1)
    try:
        result = be.run(current_circuit(), shots=shots, noise=nm)
    except NotImplementedError:
        pytest.skip(f"{backend} does not support noise")
    # With 10% readout error, ~10% of shots should read |0>
    p0 = result.counts.get("0", 0) / shots
    assert p0 > 0.02
    assert p0 < 0.25


# ---------------------------------------------------------------------------
# 3. Single-qubit vs two-qubit noise levels
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("backend", BACKENDS)
def test_two_qubit_noise_stronger(backend):
    """Two-qubit noise should produce more leakage than single-qubit."""
    _import_backend(backend)
    shots = 512
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    be = get_backend(backend)
    try:
        result_low = be.run(current_circuit(), shots=shots, noise=NoiseModel(single=0.01, double=0.01))
        reset()
        qgate(H, 0)
        qgate(CX, 0, 1)
        result_high = be.run(current_circuit(), shots=shots, noise=NoiseModel(single=0.01, double=0.10))
    except NotImplementedError:
        pytest.skip(f"{backend} does not support noise")

    def leakage(r):
        return (r.counts.get("01", 0) + r.counts.get("10", 0)) / shots

    assert leakage(result_high) > leakage(result_low)
