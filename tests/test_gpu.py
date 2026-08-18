"""GPU backend tests — covers CuPy engine, GPU dispatch, capability matrix, and scheduler.

Backends whose SDK is not installed are skipped via ``pytest.importorskip``.
"""

from __future__ import annotations

import math

import pytest

from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import CCX, CX, SWAP, H, Ry, X
from quonic.ir import ClassicalIfOperation, GateOperation
from quonic.scheduler import circuit_features, recommend_backend_gpu
from quonic.stack import current_circuit

BACKENDS = [
    "qulacs",
    "tensorcircuit",
    "cudaq",
    "mindquantum",
    "qpanda",
    "cqlib",
    "cupy",
]

_MODULE_MAP = {
    "qpanda": "pyqpanda3",
}


def _import_backend(backend: str):
    if backend == "tensorcircuit":
        from quonic.backends.tensorcircuit import _ensure_tc_numpy_compat

        _ensure_tc_numpy_compat()
    mod = _MODULE_MAP.get(backend, backend)
    return pytest.importorskip(mod)


def _run(backend: str, shots: int = 256, method: str = "statevector"):
    return get_backend(backend).run(current_circuit(), shots=shots, method=method)


# ---------------------------------------------------------------------------
# 1. CuPy engine — basic gate tests
# ---------------------------------------------------------------------------


def test_cupy_bell():
    _import_backend("cupy")
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    result = _run("cupy", shots=1024)
    p00 = result.counts.get("00", 0) / 1024
    p11 = result.counts.get("11", 0) / 1024
    assert p00 > 0.3 and p11 > 0.3
    assert p00 + p11 > 0.9


def test_cupy_ghz3():
    _import_backend("cupy")
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(CX, 1, 2)
    result = _run("cupy", shots=1024)
    p000 = result.counts.get("000", 0) / 1024
    p111 = result.counts.get("111", 0) / 1024
    assert p000 > 0.3 and p111 > 0.3
    assert p000 + p111 > 0.9


def test_cupy_ccx():
    _import_backend("cupy")
    reset()
    qgate(X, 0)
    qgate(X, 1)
    qgate(CCX, 0, 1, 2)
    result = _run("cupy", shots=100)
    assert result.counts.get("111", 0) == 100


def test_cupy_swap():
    _import_backend("cupy")
    reset()
    qgate(X, 0)
    qgate(SWAP, 0, 1)
    result = _run("cupy", shots=100)
    assert result.counts.get("01", 0) == 100


def test_cupy_ry_pi():
    _import_backend("cupy")
    reset()
    qgate(Ry(math.pi), 0)
    result = _run("cupy", shots=100)
    assert result.counts.get("1", 0) > 95


# ---------------------------------------------------------------------------
# 2. GPU dispatch — method="gpu" on various backends
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("backend", BACKENDS)
def test_gpu_bell(backend):
    _import_backend(backend)
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    try:
        result = _run(backend, shots=1024, method="gpu")
        p00 = result.counts.get("00", 0) / 1024
        p11 = result.counts.get("11", 0) / 1024
        assert p00 > 0.3 and p11 > 0.3
        assert p00 + p11 > 0.9
    except NotImplementedError:
        pytest.skip(f"{backend} does not support GPU")


@pytest.mark.parametrize("backend", BACKENDS)
def test_gpu_ccx(backend):
    _import_backend(backend)
    reset()
    qgate(X, 0)
    qgate(X, 1)
    qgate(CCX, 0, 1, 2)
    try:
        result = _run(backend, shots=100, method="gpu")
        assert result.counts.get("111", 0) == 100
    except NotImplementedError:
        pytest.skip(f"{backend} does not support GPU")


# ---------------------------------------------------------------------------
# 3. Capability matrix — GPU support declaration
# ---------------------------------------------------------------------------


def test_cupy_capabilities():
    _import_backend("cupy")
    be = get_backend("cupy")
    assert be._CAPABILITIES["gpu"] is True
    assert be._CAPABILITIES["noise"] is True
    assert be._CAPABILITIES["ctrl"] is True
    assert be._CAPABILITIES["mid_measure"] is True


def test_cirq_no_gpu():
    be = get_backend("cirq")
    assert be._CAPABILITIES["gpu"] is False


def test_native_no_gpu():
    be = get_backend("native")
    assert be._CAPABILITIES["gpu"] is False


@pytest.mark.parametrize("backend", ["cirq", "native"])
def test_gpu_rejected(backend):
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    with pytest.raises(NotImplementedError):
        _run(backend, shots=100, method="gpu")


# ---------------------------------------------------------------------------
# 4. Smart scheduling — recommend_backend_gpu
# ---------------------------------------------------------------------------


def test_scheduler_high_entanglement():
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(CCX, 0, 1, 2)
    feats = circuit_features(current_circuit())
    rec = recommend_backend_gpu(feats)
    assert rec.method == "gpu"
    assert rec.backend in ("qulacs", "tensorcircuit", "cupy")


def test_scheduler_low_entanglement():
    reset()
    for i in range(25):
        qgate(Ry(0.1), i)
    feats = circuit_features(current_circuit())
    rec = recommend_backend_gpu(feats)
    assert rec.method == "gpu"
    assert rec.backend == "tensorcircuit"


def test_scheduler_ctrl():
    reset()
    qgate(H, 0)
    # Manually add a cif op
    circ = current_circuit()
    circ.add(
        ClassicalIfOperation(
            0,
            GateOperation("x", (1,)),
            GateOperation("i", (1,)),
        )
    )
    feats = circuit_features(circ)
    rec = recommend_backend_gpu(feats)
    assert rec.method == "gpu"
    assert rec.backend in ("qulacs", "cupy")


def test_scheduler_small_circuit():
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    feats = circuit_features(current_circuit())
    rec = recommend_backend_gpu(feats)
    assert rec.method == "gpu"
    assert rec.backend in ("qulacs", "cupy")


# ---------------------------------------------------------------------------
# 5. CuPy engine — error handling
# ---------------------------------------------------------------------------


def test_cupy_cif_raises():
    """CuPy engine should handle classical control flow."""
    _import_backend("cupy")
    reset()
    qgate(H, 0)
    circ = current_circuit()
    circ.add(
        ClassicalIfOperation(
            0,
            GateOperation("x", (1,)),
            GateOperation("i", (1,)),
        )
    )
    # CuPy supports ctrl via _run_gpu_dynamic
    result = _run("cupy", shots=1024)
    # Should produce classical mixture
    counts = result.counts
    assert len(counts) > 1


def test_cupy_noise_raises():
    """CuPy engine should raise for noise (not yet supported)."""
    _import_backend("cupy")
    reset()
    qgate(H, 0)
    # Noise is not supported in GPU mode
    with pytest.raises(NotImplementedError):
        get_backend("cupy").run(current_circuit(), shots=100, noise=0.05)
