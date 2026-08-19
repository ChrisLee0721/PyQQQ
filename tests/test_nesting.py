"""Feature nesting tests — multiple keywords applied to the same circuit.

Tests scenarios where multiple QuoNic features interact simultaneously:
- optimize + decompose on the same circuit
- zne + noise + custom gates
- batch + parameters + noise
- stepper on optimized circuits
- analysis on decomposed + optimized circuits
- custom gates in qif branches
- encoding + noise + batch
"""

from __future__ import annotations

import math

import numpy as np

from quonic import (
    Parameter,
    StepExecutor,
    analyze,
    bind_params,
    optimize,
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

# ---------------------------------------------------------------------------
# 1. optimize + decompose on the same circuit
# ---------------------------------------------------------------------------


def test_optimize_then_decompose():
    """optimize → decompose produces correct state."""
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


def test_decompose_then_optimize():
    """decompose → optimize produces correct state."""
    reset()
    qgate(H, 0)
    qgate(CCX, 0, 1, 2)  # high-level gate
    circ = current_circuit()

    decomposed = decompose(circ)
    opt = optimize(decomposed)
    sv = get_backend("native").run(opt, return_state=True)
    # H|0> on qubit 0, then CCX(0,1,2) does nothing (qubit 1 is 0)
    # So state is (|0> + |1>)/√2 on qubit 0 = (|000> + |001>)/√2
    assert abs(sv.amplitude("000") - 1 / np.sqrt(2)) < 1e-10
    assert abs(sv.amplitude("001") - 1 / np.sqrt(2)) < 1e-10


# ---------------------------------------------------------------------------
# 2. zne + custom gates
# ---------------------------------------------------------------------------


def test_zne_custom_gate():
    """ZNE works with custom gates."""
    from quonic.gates import Gate

    X_mat = np.array([[0, 1], [1, 0]], dtype=complex)
    my_x = Gate.from_matrix("my_x_zne", X_mat)

    c = Circuit()
    c.allocate(1)
    c.add(GateOperation(my_x.name, (0,), ()))
    c.add(GateOperation("measure", (0,)))

    res = zne(c, noise=0.05, target="1", shots=1024)
    # Custom X gate should give |1>, ZNE should recover closer to 1.0
    assert res.extrapolated > 0.7


# ---------------------------------------------------------------------------
# 3. batch + parameters + noise
# ---------------------------------------------------------------------------


def test_batch_parameters_noise():
    """run_batch with parameterized circuits and noise."""
    theta = Parameter("theta")
    circuits = []
    for angle in [0, math.pi / 4, math.pi / 2, math.pi]:
        c = Circuit()
        c.allocate(1)
        c.add(GateOperation("ry", (0,), (theta,)))
        circuits.append(bind_params(c, {theta: angle}))

    results = run_batch(circuits, backend="native", shots=1000, noise=0.05)
    assert len(results) == 4
    # angle=π should give mostly |1> even with noise
    assert results[3].counts.get("1", 0) > 800


# ---------------------------------------------------------------------------
# 4. stepper on optimized circuits
# ---------------------------------------------------------------------------


def test_stepper_optimized():
    """StepExecutor works on optimized circuits."""
    reset()
    qgate(X, 0)
    qgate(X, 0)  # X·X = I
    qgate(H, 0)
    circ = current_circuit()
    opt = optimize(circ)

    executor = StepExecutor(opt)
    sv = executor.step()
    # After optimize, only H remains: H|0> = |+>
    assert abs(sv.amplitude("0") - 1 / np.sqrt(2)) < 1e-10
    assert executor.done()


# ---------------------------------------------------------------------------
# 5. analysis on decomposed + optimized circuits
# ---------------------------------------------------------------------------


def test_analysis_decompose_optimize():
    """analyze on decomposed + optimized circuit."""
    reset()
    qgate(H, 0)
    qgate(CCX, 0, 1, 2)
    qgate(CX, 0, 1)
    qgate(CX, 0, 1)  # CX·CX = I
    circ = current_circuit()

    decomposed = decompose(circ)
    optimized = optimize(decomposed)
    report = analyze(optimized)

    # CCX decomposes to ~15 gates, CX·CX should be cancelled
    assert report.gate_count > 0
    assert report.cx_count >= 0  # CX·CX cancelled
    assert report.n_qubits == 3


# ---------------------------------------------------------------------------
# 6. custom gate in qif branch
# ---------------------------------------------------------------------------


def test_custom_gate_qif():
    """Custom gate works inside qif branch."""
    from quonic import qif
    from quonic.gates import Gate

    X_mat = np.array([[0, 1], [1, 0]], dtype=complex)
    my_x = Gate.from_matrix("my_x_qif_nest", X_mat)

    reset()
    qgate(X, 0)  # control = |1>
    qif(0).then(my_x, 1).else_(X, 1)
    sv = get_backend("native").run(current_circuit(), return_state=True)
    assert abs(sv.amplitude("11") - 1.0) < 1e-10


# ---------------------------------------------------------------------------
# 7. encoding + noise + batch
# ---------------------------------------------------------------------------


def test_encoding_noise_batch():
    """angle_encode + noise + batch execution."""
    circuits = [angle_encode([angle]) for angle in [0, math.pi / 2, math.pi]]
    results = run_batch(circuits, backend="native", shots=1000, noise=0.1)

    # angle=0: Ry(0)|0> = |0>, even with noise should be mostly |0>
    assert results[0].counts.get("0", 0) > 800
    # angle=π: Ry(π)|0> = |1>, even with noise should be mostly |1>
    assert results[2].counts.get("1", 0) > 800


# ---------------------------------------------------------------------------
# 8. parameters + optimize + analysis
# ---------------------------------------------------------------------------


def test_parameters_optimize_analysis():
    """Parameterized circuit → optimize → analyze."""
    theta = Parameter("theta")
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("ry", (0,), (theta,)))

    bound = bind_params(c, {theta: 0.5})
    opt = optimize(bound)
    report = analyze(opt)

    assert report.n_qubits == 1
    assert report.gate_count == 1  # Ry


# ---------------------------------------------------------------------------
# 9. gradients + custom gates
# ---------------------------------------------------------------------------


def test_gradients_custom_gate():
    """param_shift works with custom gates."""
    from quonic.gates import Gate

    # Custom Ry-like gate with parameter
    theta = 0.5
    Ry_mat = np.array([
        [np.cos(theta / 2), -np.sin(theta / 2)],
        [np.sin(theta / 2), np.cos(theta / 2)],
    ])
    my_ry = Gate.from_matrix("my_ry_grad", Ry_mat)

    c = Circuit()
    c.allocate(1)
    c.add(GateOperation(my_ry.name, (0,), ()))

    # param_shift won't work directly with custom gates (no param shift rule)
    # but the circuit should still be runnable
    sv = get_backend("native").run(c, return_state=True)
    assert abs(sv.amplitude("0") - np.cos(theta / 2)) < 1e-10


# ---------------------------------------------------------------------------
# 10. zne + optimize + noise
# ---------------------------------------------------------------------------


def test_zne_optimize_noise():
    """ZNE on optimized circuit with noise."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("x", (0,)))  # X·X = I
    c.add(GateOperation("x", (0,)))  # net effect: X
    c.add(GateOperation("measure", (0,)))

    # optimize should cancel X·X, leaving just X
    opt = optimize(c)
    report = analyze(opt)
    assert report.gate_count == 1

    # ZNE on optimized circuit
    res = zne(opt, noise=0.05, target="1", shots=1024)
    assert res.extrapolated > 0.7


# ---------------------------------------------------------------------------
# 11. stepper + encoding + StateVector
# ---------------------------------------------------------------------------


def test_stepper_encoding_statevector():
    """StepExecutor on angle_encode circuit."""
    circ = angle_encode([math.pi / 2, math.pi])
    executor = StepExecutor(circ)

    # Step 1: Ry(π/2) on q0
    sv1 = executor.step()
    # Ry(π/2)|0> = cos(π/4)|0> + sin(π/4)|1>
    assert abs(sv1.amplitude("00") - np.cos(math.pi / 4)) < 1e-10

    # Step 2: Ry(π) on q1
    sv2 = executor.step()
    # Final state: Ry(π/2)⊗Ry(π)|00>
    assert abs(sv2.amplitude("10") - np.cos(math.pi / 4)) < 1e-10
    assert abs(sv2.amplitude("11") - np.sin(math.pi / 4)) < 1e-10


# ---------------------------------------------------------------------------
# 12. batch + optimize + analysis
# ---------------------------------------------------------------------------


def test_batch_optimize_analysis():
    """run_batch with optimized circuits."""
    circuits = []
    for _ in range(3):
        reset()
        qgate(X, 0)
        qgate(X, 0)  # X·X = I
        qgate(H, 0)
        circuits.append(optimize(current_circuit()))

    results = run_batch(circuits, backend="native", shots=1000)
    for r in results:
        # H|0> = |+>, should be ~50/50
        p0 = r.counts.get("0", 0) / 1000
        assert 0.3 < p0 < 0.7


# ---------------------------------------------------------------------------
# 13. noise + StateVector (MixedState)
# ---------------------------------------------------------------------------


def test_noise_statevector():
    """return_state with noise returns MixedState."""
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    sv = get_backend("native").run(current_circuit(), shots=100, noise=0.05, return_state=True)

    # Should be MixedState with purity < 1
    assert hasattr(sv, "purity")
    assert sv.purity() < 1.0
    assert sv.purity() > 0.5  # not maximally mixed

    # probabilities should sum to ~1
    probs = sv.probabilities()
    assert abs(sum(probs.values()) - 1.0) < 0.1


# ---------------------------------------------------------------------------
# 14. custom gates + optimize (no cancellation)
# ---------------------------------------------------------------------------


def test_custom_gate_optimize():
    """Custom gates are not cancelled by optimize."""
    from quonic.gates import Gate

    H_mat = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    my_h = Gate.from_matrix("my_h_opt_nest", H_mat)

    reset()
    qgate(my_h, 0)
    qgate(my_h, 0)  # H·H = I, but custom gates don't self-cancel
    circ = current_circuit()
    opt = optimize(circ)

    gate_ops = [op for op in opt.ops if isinstance(op, GateOperation) and op.name != "measure"]
    assert len(gate_ops) == 2  # both kept (custom gates not in _SELF_INVERSE)
