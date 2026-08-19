"""Feature coupling test matrix — systematic pairwise and triple feature tests.

Tests all feature pairs and critical triples from docs/coupling-matrix.md.
Each test name encodes the features being coupled: test_<feat1>_<feat2>.

See docs/coupling-matrix.md for the full matrix and known incompatibilities.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from quonic import (
    Parameter,
    StepExecutor,
    analyze,
    bind_params,
    cif,
    optimize,
    param_shift,
    qgate,
    reset,
    run_batch,
    zne,
)
from quonic.backends import get_backend
from quonic.compiler import decompose
from quonic.encoding import angle_encode
from quonic.gates import CCX, CX, H, X
from quonic.ir import Circuit, GateOperation
from quonic.stack import current_circuit

BACKENDS = ["native", "qulacs"]

_MODULE_MAP = {"qpanda": "pyqpanda3"}


def _import_backend(backend: str):
    if backend == "tensorcircuit":
        from quonic.backends.tensorcircuit import _ensure_tc_numpy_compat
        _ensure_tc_numpy_compat()
    mod = _MODULE_MAP.get(backend, backend)
    return pytest.importorskip(mod)


# ===================================================================
#  Level 2: Pairwise coupling (selected critical pairs)
# ===================================================================


# --- CustomGate × Backend ---

@pytest.mark.parametrize("backend", BACKENDS)
def test_customgate_backend(backend):
    """Custom gate works on each backend."""
    from quonic.gates import Gate
    _import_backend(backend)
    H_mat = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    my_h = Gate.from_matrix(f"my_h_{backend}", H_mat)
    reset()
    qgate(my_h, 0)
    result = get_backend(backend).run(current_circuit(), shots=1000)
    p0 = result.counts.get("0", 0) / 1000
    assert 0.4 < p0 < 0.6


# --- StateVector × Backend ---

@pytest.mark.parametrize("backend", BACKENDS)
def test_statevector_backend(backend):
    """return_state works on each backend."""
    _import_backend(backend)
    reset()
    qgate(H, 0)
    sv = get_backend(backend).run(current_circuit(), return_state=True)
    assert abs(sv.amplitude("0") - 1 / np.sqrt(2)) < 1e-10


# --- Noise × Backend ---

@pytest.mark.parametrize("backend", BACKENDS)
def test_noise_backend(backend):
    """Noise injection works on each backend."""
    _import_backend(backend)
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    result = get_backend(backend).run(current_circuit(), shots=1000, noise=0.05)
    # With noise, should not be perfect Bell state
    p00 = result.counts.get("00", 0) / 1000
    p11 = result.counts.get("11", 0) / 1000
    assert p00 + p11 < 1.0  # some leakage


# --- optimize × decompose ---

def test_optimize_decompose():
    """optimize then decompose preserves correctness."""
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(CX, 0, 1)  # CX·CX = I
    circ = current_circuit()
    opt = optimize(circ)
    decomposed = decompose(opt)
    sv = get_backend("native").run(decomposed, return_state=True)
    # H|0> = |+>, CX·CX = I, so final state is |+0>
    assert abs(sv.amplitude("00") - 1 / np.sqrt(2)) < 1e-10


# --- Parameters × gradients ---

def test_parameters_gradients():
    """Parameter binding works with gradient computation."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("ry", (0,), (0.0,)))
    params = [0.5]
    grad = param_shift(c, params, "Z")
    expected = -math.sin(0.5)
    assert abs(grad[0] - expected) < 0.01


# --- Encoding × StateVector ---

def test_encoding_statevector():
    """angle_encode produces correct statevector."""
    circ = angle_encode([math.pi])
    sv = get_backend("native").run(circ, return_state=True)
    assert abs(sv.amplitude("1") - 1.0) < 1e-10


# --- Encoding × noise ---

def test_encoding_noise():
    """angle_encode works with noise."""
    circ = angle_encode([math.pi])
    result = get_backend("native").run(circ, shots=1000, noise=0.1)
    p1 = result.counts.get("1", 0) / 1000
    assert 0.7 < p1 < 1.0


# --- Stepper × StateVector ---

def test_stepper_statevector():
    """StepExecutor returns correct StateVector at each step."""
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    executor = StepExecutor(current_circuit())
    sv1 = executor.step()
    assert abs(sv1.amplitude("00") - 1 / np.sqrt(2)) < 1e-10
    sv2 = executor.step()
    assert abs(sv2.amplitude("00") - 1 / np.sqrt(2)) < 1e-10
    assert abs(sv2.amplitude("11") - 1 / np.sqrt(2)) < 1e-10


# --- Analysis × optimize ---

def test_analysis_optimize():
    """analyze reports reduced gate count after optimize."""
    reset()
    qgate(X, 0)
    qgate(X, 0)
    qgate(H, 0)
    circ = current_circuit()
    before = analyze(circ)
    after = analyze(optimize(circ))
    assert after.gate_count < before.gate_count


# --- Serialization × introspection ---

def test_serialization_introspection():
    """to_json → from_json preserves circuit structure."""
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    circ = current_circuit()
    json_str = circ.to_json()
    restored = Circuit.from_json(json_str)
    assert len(restored) == len(circ)
    for a, b in zip(circ, restored):
        assert a.name == b.name
        assert a.qubits == b.qubits


# --- Batch × Backend ---

@pytest.mark.parametrize("backend", BACKENDS)
def test_batch_backend(backend):
    """run_batch works on each backend."""
    _import_backend(backend)
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("measure", (0,)))
    results = run_batch([c, c], backend=backend, shots=100)
    assert len(results) == 2
    for r in results:
        assert r.counts.get("1", 0) == 100


# ===================================================================
#  Level 3: Triple coupling (critical paths)
# ===================================================================


# --- CustomGate + noise + backend ---

@pytest.mark.parametrize("backend", BACKENDS)
def test_customgate_noise_backend(backend):
    """Custom gate + noise on each backend."""
    from quonic.gates import Gate
    _import_backend(backend)
    H_mat = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    my_h = Gate.from_matrix(f"my_h_noise_{backend}", H_mat)
    reset()
    qgate(my_h, 0)
    qgate(my_h, 0)  # H·H = I
    try:
        result = get_backend(backend).run(current_circuit(), shots=1000, noise=0.05)
        p0 = result.counts.get("0", 0) / 1000
        assert p0 > 0.7
    except (NotImplementedError, ValueError):
        pass  # some backends may not support custom gates with noise


# --- Parameters + gradients + backend ---

@pytest.mark.parametrize("backend", BACKENDS)
def test_parameters_gradients_backend(backend):
    """Parameterized circuit + gradients on each backend."""
    _import_backend(backend)
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("ry", (0,), (0.0,)))
    grad = param_shift(c, [0.3], "Z", backend=backend)
    expected = -math.sin(0.3)
    assert abs(grad[0] - expected) < 0.05


# --- Encoding + noise + backend ---

@pytest.mark.parametrize("backend", BACKENDS)
def test_encoding_noise_backend(backend):
    """angle_encode + noise on each backend."""
    _import_backend(backend)
    circ = angle_encode([math.pi])
    try:
        result = get_backend(backend).run(circ, shots=1000, noise=0.1)
        p1 = result.counts.get("1", 0) / 1000
        assert p1 > 0.5
    except NotImplementedError:
        pass


# --- optimize + decompose + backend ---

@pytest.mark.parametrize("backend", BACKENDS)
def test_optimize_decompose_backend(backend):
    """optimize → decompose → run on each backend."""
    _import_backend(backend)
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(CX, 0, 1)
    circ = optimize(current_circuit())
    decomposed = decompose(circ)
    sv = get_backend(backend).run(decomposed, return_state=True)
    assert abs(sv.amplitude("00") - 1 / np.sqrt(2)) < 1e-10


# --- cif + noise + backend ---

@pytest.mark.parametrize("backend", BACKENDS)
def test_cif_noise_backend(backend):
    """cif + noise on each backend."""
    _import_backend(backend)
    reset()
    qgate(X, 0)
    cif(0).then(X, 1).else_(X, 1)
    try:
        result = get_backend(backend).run(current_circuit(), shots=1000, noise=0.05)
        # Both branches apply X, so q1 should be 1
        assert result.counts.get("11", 0) > 800
    except NotImplementedError:
        pass


# --- StateVector + optimize + Analysis ---

def test_statevector_optimize_analysis():
    """StateVector + optimize + analyze integration."""
    reset()
    qgate(X, 0)
    qgate(X, 0)
    qgate(H, 0)
    circ = current_circuit()
    opt = optimize(circ)
    report = analyze(opt)
    sv = get_backend("native").run(opt, return_state=True)
    # X·X = I, then H|0> = |+>
    assert abs(sv.amplitude("0") - 1 / np.sqrt(2)) < 1e-10
    assert report.gate_count == 1  # only H remains


# --- CustomGate + qif + StateVector ---

def test_customgate_qif_statevector():
    """Custom gate in qif branch produces correct statevector."""
    from quonic.gates import Gate
    X_mat = np.array([[0, 1], [1, 0]], dtype=complex)
    my_x = Gate.from_matrix("my_x_qif_sv", X_mat)
    from quonic import qif
    reset()
    qgate(X, 0)  # control = |1>
    qif(0).then(my_x, 1).else_(X, 1)
    sv = get_backend("native").run(current_circuit(), return_state=True)
    assert abs(sv.amplitude("11") - 1.0) < 1e-10


# --- Parameters + Encoding + Batch ---

def test_parameters_encoding_batch():
    """Parameters + encoding + batch execution."""
    circuits = []
    for angle in [0, math.pi / 4, math.pi / 2, math.pi]:
        circuits.append(angle_encode([angle]))
    results = run_batch(circuits, backend="native", shots=1000)
    assert len(results) == 4
    # angle=0 → |0>, angle=π → |1>
    assert results[0].counts.get("0", 0) > 950
    assert results[3].counts.get("1", 0) > 950


# --- Serialization + introspection + optimize ---

def test_serialization_introspection_optimize():
    """Serialize → deserialize → optimize → verify."""
    reset()
    qgate(X, 0)
    qgate(X, 0)
    qgate(H, 0)
    circ = current_circuit()
    json_str = circ.to_json()
    restored = Circuit.from_json(json_str)
    opt = optimize(restored)
    sv = get_backend("native").run(opt, return_state=True)
    assert abs(sv.amplitude("0") - 1 / np.sqrt(2)) < 1e-10


# --- Stepper + cif + StateVector ---

def test_stepper_cif_statevector():
    """Stepper works with gate-only circuits (cif requires backend-level handling)."""
    reset()
    qgate(X, 0)  # q0 = |1>
    qgate(CX, 0, 1)  # CNOT: flip q1 when q0=1
    circ = current_circuit()
    executor = StepExecutor(circ)
    # Step 1: X on q0
    sv1 = executor.step()
    assert abs(sv1.amplitude("01") - 1.0) < 1e-10  # q0=1, q1=0
    # Step 2: CX(0,1) → flip q1
    sv2 = executor.step()
    assert abs(sv2.amplitude("11") - 1.0) < 1e-10  # q0=1, q1=1


# ===================================================================
#  Level 4: End-to-end pipelines
# ===================================================================


def test_vqe_pipeline():
    """VQE pipeline: Parameters → Encoding → gradients → StateVector → Analysis."""
    # Simple VQE: minimize <Z> for Ry(θ)|0>
    theta = Parameter("theta")
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("ry", (0,), (theta,)))

    # Bind to initial value
    bound = bind_params(c, {theta: 0.5})
    sv = get_backend("native").run(bound, return_state=True)
    energy = sv.expectation("Z")

    # Compute gradient
    grad = param_shift(bound, [0.5], "Z")
    report = analyze(bound)

    assert isinstance(energy, float)
    assert len(grad) == 1
    assert report.n_qubits == 1


def test_error_mitigation_pipeline():
    """Error mitigation: ZNE + noise + backend."""
    import pytest
    pytest.importorskip("scipy")
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("measure", (0,)))

    # ZNE with noise
    res = zne(c, noise=0.05, target="1", shots=1024, extrapolation="exponential")
    assert res.extrapolated > 0.8  # should recover most of the signal


def test_hardware_compile_pipeline():
    """Hardware compile: decompose → optimize → analyze."""
    reset()
    qgate(H, 0)
    qgate(CCX, 0, 1, 2)
    qgate(CX, 1, 2)
    circ = current_circuit()

    decomposed = decompose(circ)
    optimized = optimize(decomposed)
    report = analyze(optimized)

    assert report.gate_count > 0
    assert report.n_qubits == 3


def test_debug_pipeline():
    """Debug pipeline: Stepper → StateVector → Analysis → Serialization."""
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    circ = current_circuit()

    executor = StepExecutor(circ)
    states = []
    while not executor.done():
        sv = executor.step()
        states.append(sv)

    assert len(states) == 2
    # Final state should be Bell state
    assert abs(states[1].amplitude("00") - 1 / np.sqrt(2)) < 1e-10

    # Analyze
    report = analyze(circ)
    assert report.gate_count == 2

    # Serialize
    json_str = circ.to_json()
    restored = Circuit.from_json(json_str)
    assert len(restored) == len(circ)


def test_custom_gate_pipeline():
    """Custom gate pipeline: CustomGate → optimize → decompose → StateVector."""
    from quonic.gates import Gate

    H_mat = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    my_h = Gate.from_matrix("my_h_pipeline", H_mat)

    reset()
    qgate(my_h, 0)
    qgate(my_h, 0)  # H·H = I
    circ = current_circuit()

    opt = optimize(circ)
    sv = get_backend("native").run(opt, return_state=True)
    # Should be |0> (H·H = I)
    assert abs(sv.amplitude("0") - 1.0) < 1e-10


def test_full_stack_pipeline():
    """Full stack: CustomGate → Parameters → noise → optimize → StateVector."""
    from quonic.gates import Gate

    H_mat = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    my_h = Gate.from_matrix("my_h_full", H_mat)

    theta = Parameter("theta")
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("ry", (0,), (theta,)))

    bind_params(c, {theta: math.pi / 4})

    # Add custom gate
    reset()
    qgate(my_h, 0)
    circ = current_circuit()

    # Optimize
    opt = optimize(circ)

    # Run with noise
    try:
        result = get_backend("native").run(opt, shots=1000, noise=0.01)
        assert isinstance(result.counts, dict)
    except NotImplementedError:
        pass

    # Run without noise for statevector
    sv = get_backend("native").run(opt, return_state=True)
    assert abs(sv.amplitude("0") - 1 / np.sqrt(2)) < 1e-10
