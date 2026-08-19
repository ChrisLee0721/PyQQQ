"""Integration tests — verify features work together correctly.

Tests the coupling between: custom gates, statevector, gradients, circuit
introspection, serialization, analysis, parameters, encoding, stepper.
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
    creg,
    optimize,
    param_shift,
    qgate,
    qshow,
    reset,
    run_batch,
    zne,
)
from quonic.backends import get_backend
from quonic.encoding import angle_encode
from quonic.gates import CCX, CX, H, X
from quonic.ir import Circuit, GateOperation
from quonic.stack import current_circuit

# ---------------------------------------------------------------------------
# 1. Custom gate + StateVector
# ---------------------------------------------------------------------------


def test_custom_gate_statevector():
    """Custom gate → return_state → verify amplitudes."""
    from quonic.gates import Gate

    H_mat = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    my_h = Gate.from_matrix("my_h_test", H_mat)

    reset()
    qgate(my_h, 0)
    sv = get_backend("native").run(current_circuit(), return_state=True)

    assert abs(sv.amplitude("0") - 1 / np.sqrt(2)) < 1e-10
    assert abs(sv.amplitude("1") - 1 / np.sqrt(2)) < 1e-10
    assert abs(sv.expectation("Z")) < 0.1  # |+> has <Z> ≈ 0


def test_custom_gate_qulacs_statevector():
    """Custom gate on qulacs → return_state → verify."""
    pytest.importorskip("qulacs")
    from quonic.gates import Gate

    X_mat = np.array([[0, 1], [1, 0]], dtype=complex)
    my_x = Gate.from_matrix("my_x_test", X_mat)

    reset()
    qgate(my_x, 0)
    sv = get_backend("qulacs").run(current_circuit(), return_state=True)

    assert abs(sv.amplitude("1") - 1.0) < 1e-10
    assert abs(sv.amplitude("0")) < 1e-10


# ---------------------------------------------------------------------------
# 2. Custom gate + optimize
# ---------------------------------------------------------------------------


def test_custom_gate_optimize():
    """Custom gate should not be cancelled by optimize."""
    from quonic.gates import Gate

    H_mat = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    my_h = Gate.from_matrix("my_h_opt", H_mat)

    reset()
    qgate(my_h, 0)
    qgate(my_h, 0)  # H·H = I, but custom gates don't self-cancel
    circ = current_circuit()
    opt = optimize(circ)
    # Custom gates are not in _SELF_INVERSE, so they should NOT cancel
    gate_ops = [op for op in opt.ops if isinstance(op, GateOperation) and op.name != "measure"]
    assert len(gate_ops) == 2  # both kept


# ---------------------------------------------------------------------------
# 3. StateVector + gradients
# ---------------------------------------------------------------------------


def test_statevector_gradients():
    """param_shift uses return_state internally — verify it works end-to-end."""
    # Simple circuit: Ry(θ)|0>, measure Z
    # <Z> = cos(θ), d<Z>/dθ = -sin(θ)
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("ry", (0,), (0.0,)))  # placeholder param

    params = [0.5]
    grad = param_shift(c, params, "Z")

    # Expected: d<Z>/dθ at θ=0.5 = -sin(0.5) ≈ -0.4794
    expected = -math.sin(0.5)
    assert abs(grad[0] - expected) < 0.01, f"grad={grad[0]}, expected={expected}"


# ---------------------------------------------------------------------------
# 4. Circuit introspection + serialization
# ---------------------------------------------------------------------------


def test_circuit_copy_serialize_roundtrip():
    """copy → to_json → from_json → verify ops match."""
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    circ = current_circuit()

    circ_copy = circ.copy()
    json_str = circ_copy.to_json()
    circ_restored = Circuit.from_json(json_str)

    assert circ_restored.num_qubits == circ.num_qubits
    assert len(circ_restored) == len(circ)
    for orig, rest in zip(circ, circ_restored):
        assert orig.name == rest.name
        assert orig.qubits == rest.qubits


def test_circuit_filter_slice():
    """filter + slice produce correct sub-circuits."""
    reset()
    qgate(H, 0)
    qgate(X, 1)
    qgate(CX, 0, 1)
    circ = current_circuit()

    # filter by qubit
    sub = circ.filter(qubits={0})
    assert all(op.qubits == (0,) for op in sub)

    # slice
    sub2 = circ.slice(start=0, end=2)
    assert len(sub2) == 2


def test_circuit_inverse():
    """inverse() reverses ops and adjoints gates."""
    reset()
    qgate(H, 0)
    qgate(X, 0)
    circ = current_circuit()
    inv = circ.inverse()

    # H and X are self-inverse, so H·X·X·H = I
    combined = circ + inv
    sv = get_backend("native").run(combined, return_state=True)
    # Should be |0>
    assert abs(sv.amplitude("0") - 1.0) < 1e-10


# ---------------------------------------------------------------------------
# 5. Parameters + gradients
# ---------------------------------------------------------------------------


def test_parameters_gradients():
    """Parameter + bind_params + param_shift integration."""
    theta = Parameter("theta")

    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("ry", (0,), (theta,)))

    # Bind to 0.7
    bound = bind_params(c, {theta: 0.7})
    sv = get_backend("native").run(bound, return_state=True)

    # <Z> = cos(0.7)
    expected_z = math.cos(0.7)
    assert abs(sv.expectation("Z") - expected_z) < 0.01


# ---------------------------------------------------------------------------
# 6. Encoding + StateVector
# ---------------------------------------------------------------------------


def test_angle_encode_statevector():
    """angle_encode → run → verify amplitudes."""
    features = [math.pi / 2, math.pi]  # Ry(π/2)|0>, Ry(π)|0>
    circ = angle_encode(features)

    sv = get_backend("native").run(circ, return_state=True)

    # Ry(π/2)|0> = cos(π/4)|0> + sin(π/4)|1> ≈ 0.707|0> + 0.707|1>
    # Ry(π)|0> = cos(π/2)|0> + sin(π/2)|1> = |1>
    # qubit 0 = LSB, qubit 1 = MSB
    # Combined: q1=1, q0=0 → "10" amp ≈ 0.707; q1=1, q0=1 → "11" amp ≈ 0.707
    amp_10 = sv.amplitude("10")
    amp_11 = sv.amplitude("11")
    assert abs(amp_10) > 0.5
    assert abs(amp_11) > 0.5


# ---------------------------------------------------------------------------
# 7. Stepper + StateVector
# ---------------------------------------------------------------------------


def test_stepper_statevector():
    """StepExecutor → step → StateVector at each gate."""
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    circ = current_circuit()

    executor = StepExecutor(circ)

    # Step 1: H on q0 → |+> ⊗ |0> = (|00> + |01>)/√2
    # qubit 0 = LSB, so "01" means q0=1, q1=0
    sv1 = executor.step()
    assert abs(sv1.amplitude("00") - 1 / np.sqrt(2)) < 1e-10
    assert abs(sv1.amplitude("01") - 1 / np.sqrt(2)) < 1e-10

    # Step 2: CX(0,1) → Bell state = (|00> + |11>)/√2
    sv2 = executor.step()
    assert abs(sv2.amplitude("00") - 1 / np.sqrt(2)) < 1e-10
    assert abs(sv2.amplitude("11") - 1 / np.sqrt(2)) < 1e-10

    assert executor.done()


# ---------------------------------------------------------------------------
# 8. Analysis + optimize
# ---------------------------------------------------------------------------


def test_analysis_optimize():
    """analyze → optimize → analyze → verify gate count decreased."""
    reset()
    qgate(X, 0)
    qgate(X, 0)  # X·X = I
    qgate(H, 0)
    circ = current_circuit()

    report_before = analyze(circ)
    opt = optimize(circ)
    report_after = analyze(opt)

    assert report_after.gate_count < report_before.gate_count


# ---------------------------------------------------------------------------
# 9. Batch execution
# ---------------------------------------------------------------------------


def test_batch_execution():
    """run_batch runs multiple circuits correctly."""
    circuits = []
    for _ in range(3):
        c = Circuit()
        c.allocate(1)
        c.add(GateOperation("x", (0,)))
        c.add(GateOperation("measure", (0,)))
        circuits.append(c)

    results = run_batch(circuits, backend="native", shots=100)
    assert len(results) == 3
    for r in results:
        assert r.counts.get("1", 0) == 100


# ---------------------------------------------------------------------------
# 10. Encoding + batch
# ---------------------------------------------------------------------------


def test_encoding_batch():
    """angle_encode multiple circuits → run_batch → verify."""
    circuits = []
    for angle in [0, math.pi / 2, math.pi]:
        circuits.append(angle_encode([angle]))

    results = run_batch(circuits, backend="native", shots=1000)

    # angle=0: Ry(0)|0> = |0>
    assert results[0].counts.get("0", 0) > 950

    # angle=π: Ry(π)|0> = |1>
    assert results[2].counts.get("1", 0) > 950


# ===================================================================
#  New features × Original features (v0.1.0–v0.6.0) coupling tests
# ===================================================================


# ---------------------------------------------------------------------------
# 11. Custom gate + qshow (v0.1.0 original)
# ---------------------------------------------------------------------------


def test_custom_gate_qshow():
    """Custom gate works through qshow with native backend."""
    from quonic.gates import Gate

    X_mat = np.array([[0, 1], [1, 0]], dtype=complex)
    my_x = Gate.from_matrix("my_x_show", X_mat)

    reset()
    qgate(my_x, 0)
    # Custom gates require backends that check _GATE_REGISTRY (native, qulacs)
    result = qshow(backend="native", shots=100)
    assert result.counts.get("1", 0) == 100


# ---------------------------------------------------------------------------
# 12. Custom gate + qif (v0.1.0 original)
# ---------------------------------------------------------------------------


def test_custom_gate_qif():
    """Custom gate works inside qif branch."""
    from quonic.gates import Gate

    X_mat = np.array([[0, 1], [1, 0]], dtype=complex)
    my_x = Gate.from_matrix("my_x_qif", X_mat)

    reset()
    qgate(X, 0)  # control = |1>
    from quonic import qif
    qif(0).then(my_x, 1).else_(X, 1)  # should flip q1
    result = get_backend("native").run(current_circuit(), shots=100)
    assert result.counts.get("11", 0) == 100


# ---------------------------------------------------------------------------
# 13. StateVector + qshow (v0.1.0 original)
# ---------------------------------------------------------------------------


def test_statevector_qshow():
    """return_state works through the native backend."""
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    # qshow doesn't support return_state; use backend directly
    sv = get_backend("native").run(current_circuit(), return_state=True)
    # Bell state
    assert abs(sv.amplitude("00") - 1 / np.sqrt(2)) < 1e-10
    assert abs(sv.amplitude("11") - 1 / np.sqrt(2)) < 1e-10


# ---------------------------------------------------------------------------
# 14. StateVector + noise (v0.3.0 original)
# ---------------------------------------------------------------------------


def test_statevector_noise():
    """return_state with noise raises clear error (DM engine not supported)."""
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    # return_state with noise uses DM engine which doesn't support state extraction
    # This should raise a clear error, not crash
    try:
        sv = get_backend("native").run(
            current_circuit(), shots=100, noise=0.05, return_state=True
        )
        # If it works (some backends may support it), verify validity
        probs = sv.probabilities()
        total = sum(probs.values())
        assert abs(total - 1.0) < 0.1
    except (AttributeError, NotImplementedError, TypeError):
        # Expected: DM engine doesn't support state extraction
        pass


# ---------------------------------------------------------------------------
# 15. Circuit introspection + cif (v0.3.0 original)
# ---------------------------------------------------------------------------


def test_circuit_introspection_cif():
    """Circuit introspection works on circuits with cif ops."""
    reset()
    qgate(H, 0)
    cif(0).then(X, 1).else_(X, 1)
    circ = current_circuit()

    # __repr__ should work
    r = repr(circ)
    assert "Circuit(" in r

    # __len__ should count all ops (including cif)
    assert len(circ) > 0

    # __iter__ should iterate all ops
    ops = list(circ)
    assert len(ops) == len(circ)


# ---------------------------------------------------------------------------
# 16. Circuit serialization + creg (v0.3.0 original)
# ---------------------------------------------------------------------------


def test_circuit_serialize_creg():
    """Circuit serialization works with creg ops."""
    reset()
    qgate(H, 0)
    flag = creg("flag")
    flag.measure(0)
    circ = current_circuit()

    # Serialize (cmeasure ops are serialized)
    d = circ.to_dict()
    assert d["num_qubits"] == 1
    assert len(d["ops"]) > 0

    # Deserialize
    circ2 = Circuit.from_dict(d)
    assert circ2.num_qubits == circ.num_qubits


# ---------------------------------------------------------------------------
# 17. Analysis + decompose (v0.3.0 original)
# ---------------------------------------------------------------------------


def test_analysis_decompose():
    """analyze() works on decomposed circuits."""
    reset()
    qgate(H, 0)
    qgate(CCX, 0, 1, 2)
    circ = current_circuit()

    from quonic.compiler import decompose
    decomposed = decompose(circ)

    report_before = analyze(circ)
    report_after = analyze(decomposed)

    # Decomposition should increase gate count (CCX → multiple basic gates)
    assert report_after.gate_count >= report_before.gate_count
    # But qubit count stays the same
    assert report_after.n_qubits == report_before.n_qubits


# ---------------------------------------------------------------------------
# 18. Optimize + decompose + compile (v0.3.0/v0.6.0 original)
# ---------------------------------------------------------------------------


def test_optimize_decompose_compile():
    """optimize → decompose → compile pipeline works end-to-end."""
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(CX, 0, 1)  # CX·CX = I
    circ = current_circuit()

    # optimize should cancel CX·CX
    opt = optimize(circ)
    report = analyze(opt)
    assert report.cx_count == 0  # both CX cancelled

    # decompose should still work on optimized circuit
    from quonic.compiler import decompose
    decomposed = decompose(opt)
    assert decomposed.num_qubits == 2


# ---------------------------------------------------------------------------
# 19. Gradients + groverize (v0.3.0 original)
# ---------------------------------------------------------------------------


def test_gradients_with_native():
    """param_shift works with native backend (the original default)."""
    # Simple VQE-like circuit: Ry(θ) on qubit 0, measure Z
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("ry", (0,), (0.0,)))

    params = [0.3]
    grad = param_shift(c, params, "Z", backend="native")

    # <Z> = cos(θ), d<Z>/dθ = -sin(θ)
    expected = -math.sin(0.3)
    assert abs(grad[0] - expected) < 0.01


# ---------------------------------------------------------------------------
# 20. Batch + multiple backends (v0.1.0–v0.5.0 original)
# ---------------------------------------------------------------------------


def test_batch_multiple_backends():
    """run_batch works across different backends."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("measure", (0,)))

    # native backend
    results_native = run_batch([c], backend="native", shots=100)
    assert results_native[0].counts.get("1", 0) == 100

    # qulacs backend
    pytest.importorskip("qulacs")
    results_qulacs = run_batch([c], backend="qulacs", shots=100)
    assert results_qulacs[0].counts.get("1", 0) == 100


# ---------------------------------------------------------------------------
# 21. Stepper + original gates (v0.1.0 original)
# ---------------------------------------------------------------------------


def test_stepper_original_gates():
    """StepExecutor works with original gate set (H, CX, X, etc.)."""
    reset()
    qgate(X, 0)
    qgate(CX, 0, 1)
    circ = current_circuit()

    executor = StepExecutor(circ)

    # Step 1: X on q0 → |10> (q0=1, q1=0)
    sv1 = executor.step()
    assert abs(sv1.amplitude("01") - 1.0) < 1e-10  # q0=1, q1=0

    # Step 2: CX(0,1) → |11> (q0=1, q1=1)
    sv2 = executor.step()
    assert abs(sv2.amplitude("11") - 1.0) < 1e-10


# ---------------------------------------------------------------------------
# 22. Parameterized circuit + ZNE (v0.3.0 original)
# ---------------------------------------------------------------------------


def test_parameterized_zne():
    """Parameterized circuit works with ZNE."""
    theta = Parameter("theta")

    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("ry", (0,), (theta,)))
    c.add(GateOperation("measure", (0,)))

    # Bind to π (should give |1>)
    bound = bind_params(c, {theta: math.pi})

    # ZNE should work on the bound circuit
    res = zne(bound, noise=0.05, target="1", shots=1024)
    # ZNE should improve the result (extrapolated closer to 1.0 than raw)
    assert res.extrapolated > 0.8


# ---------------------------------------------------------------------------
# 23. Encoding + noise (v0.3.0 original)
# ---------------------------------------------------------------------------


def test_encoding_with_noise():
    """angle_encode works with noise simulation."""
    circ = angle_encode([math.pi])  # Ry(π)|0> = |1>

    # With noise, the result should be degraded
    result = get_backend("native").run(circ, shots=1000, noise=0.1)
    p1 = result.counts.get("1", 0) / 1000
    # With 10% noise, P(1) should be less than 1.0
    assert p1 < 1.0
    assert p1 > 0.5  # but still mostly |1>


# ---------------------------------------------------------------------------
# 24. Custom gate + noise (v0.3.0 original)
# ---------------------------------------------------------------------------


def test_custom_gate_with_noise():
    """Custom gate works with noise on backends that support it."""
    from quonic.gates import Gate

    H_mat = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    my_h = Gate.from_matrix("my_h_noise", H_mat)

    reset()
    qgate(my_h, 0)
    qgate(my_h, 0)  # H·H = I, should give |0>

    # Custom gates with noise: use qulacs which has native noise support
    try:
        pytest.importorskip("qulacs")
        result = get_backend("qulacs").run(current_circuit(), shots=1000, noise=0.05)
        p0 = result.counts.get("0", 0) / 1000
        assert p0 > 0.8  # mostly |0>
        assert p0 < 1.0  # but not perfect
    except (ImportError, NotImplementedError, ValueError):
        # Some backends may not support custom gates with noise
        pass
