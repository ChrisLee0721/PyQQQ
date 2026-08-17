"""Classical control flow tests for engine backends.

Tests that backends with mid-circuit measurement support correctly handle
cif, cmeasure, and cwhile operations.
"""

from __future__ import annotations

import pytest

from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import CX, H, I, X
from quonic.ir import ClassicalIfOperation, GateOperation
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
# 1. cif: measure qubit 0, if |1> then X on qubit 1
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("backend", BACKENDS)
def test_cif_then_branch(backend):
    """cif with control=qubit: measure qubit, branch accordingly."""
    _import_backend(backend)
    reset()
    qgate(X, 0)  # q0 = |1>
    circ = current_circuit()
    # cif(0): measure qubit 0, if result==1 then X(1) else I(1)
    circ.add(
        ClassicalIfOperation(
            0,
            GateOperation("x", (1,)),
            GateOperation("i", (1,)),
        )
    )
    be = get_backend(backend)
    try:
        result = be.run(circ, shots=256)
    except NotImplementedError:
        pytest.skip(f"{backend} does not support mid-circuit measurement")
    # q0=|1>, so cif should execute X(1), result should be |11>
    assert result.counts.get("11", 0) > 200


# ---------------------------------------------------------------------------
# 2. cif: else branch
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("backend", BACKENDS)
def test_cif_else_branch(backend):
    """cif else branch: qubit 0 is |0>, should execute else_op."""
    _import_backend(backend)
    reset()
    # q0 = |0> (default)
    circ = current_circuit()
    circ.add(
        ClassicalIfOperation(
            0,
            GateOperation("x", (1,)),
            GateOperation("i", (1,)),
        )
    )
    be = get_backend(backend)
    try:
        result = be.run(circ, shots=256)
    except NotImplementedError:
        pytest.skip(f"{backend} does not support mid-circuit measurement")
    # q0=|0>, so cif should execute I(1), result should be |00>
    assert result.counts.get("00", 0) > 200


# ---------------------------------------------------------------------------
# 3. Noise + classical control flow
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("backend", BACKENDS)
def test_noisy_cif(backend):
    """Noise + cif: should still produce valid results.

    Note: TensorCircuit's DM engine doesn't support incremental state reading
    for dynamic circuits, so this test is expected to fail/skip for that backend.
    """
    _import_backend(backend)
    # TensorCircuit's DMCircuit doesn't support mid-circuit state extraction
    if backend == "tensorcircuit":
        pytest.skip("TensorCircuit DM does not support mid-circuit state extraction")
    reset()
    qgate(X, 0)  # q0 = |1>
    circ = current_circuit()
    circ.add(
        ClassicalIfOperation(
            0,
            GateOperation("x", (1,)),
            GateOperation("i", (1,)),
        )
    )
    be = get_backend(backend)
    try:
        result = be.run(circ, shots=1024, noise=0.05)
    except NotImplementedError:
        pytest.skip(f"{backend} does not support noise + mid-circuit measurement")
    # Most shots should be |11>, some noise leakage expected
    p11 = result.counts.get("11", 0) / 1024
    assert p11 > 0.5  # majority should be |11>
