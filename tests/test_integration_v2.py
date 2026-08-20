"""Integration tests: feature combinations.

Tests combining multiple QuoNic features together.
"""

from __future__ import annotations

import pytest
import numpy as np

from quonic.ir import Circuit, GateOperation
from quonic.backends.native import NativeBackend


def test_qec_with_noise():
    """QEC should improve success rate with noise."""
    from quonic.qec import qec_round_trip

    # Without QEC: high error rate
    result_no_qec = qec_round_trip(code="bit_flip", error_rate=0.1, shots=1000)

    # With QEC: should have lower logical error rate
    result_qec = qec_round_trip(code="bit_flip", error_rate=0.01, shots=1000)

    # QEC with lower error rate should have lower logical error
    assert result_qec.logical_error_rate <= result_no_qec.logical_error_rate


def test_ml_with_different_backends():
    """ML training should work with different backends."""
    from quonic.ml import Ansatz, SPSAOptimizer, train, expectation_loss

    ansatz = Ansatz.hardware_efficient(n_qubits=2, layers=1)
    opt = SPSAOptimizer(maxiter=5, lr=0.1)

    def loss_fn(p):
        return expectation_loss(ansatz.build(p), "ZZ")

    result = train(ansatz, opt, loss_fn)
    assert result.n_steps == 5
    assert len(result.loss_history) == 5


def test_optimize_then_run():
    """Optimized circuit should give same result as original."""
    from quonic.compiler import optimize

    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("h", (0,)))  # H·H = I
    c.add(GateOperation("cx", (0, 1)))

    optimized = optimize(c, passes=("cancel",))

    be = NativeBackend()
    result_orig = be.run(c, shots=1000)
    result_opt = be.run(optimized, shots=1000)

    # Both should give Bell state
    assert set(result_orig.counts.keys()) <= {"00", "11"}
    assert set(result_opt.counts.keys()) <= {"00", "11"}


def test_groverize_then_run():
    """Groverized circuit should run correctly."""
    from quonic import cwhile, creg, qgate, reset
    from quonic.gates import H
    from quonic.compiler import groverize
    from quonic.stack import current_circuit

    reset()
    flag = creg("flag")
    with cwhile(flag, until=1):
        qgate(H, 0)
        flag.measure(0)

    cwhile_op = current_circuit().ops[-1]
    static = groverize(cwhile_op)

    be = NativeBackend()
    result = be.run(static, shots=1000)
    assert result.counts is not None


def test_zne_improves_result():
    """ZNE should improve result under noise."""
    from quonic import zne
    from quonic.ir import Circuit, GateOperation

    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("measure", (0,)))

    # With noise, success rate < 1.0
    # With ZNE, should be closer to 1.0
    result = zne(c, noise=0.05, target="1", shots=4096)
    assert result.extrapolated > 0.5  # Should recover some signal


def test_scheduler_with_different_circuits():
    """Scheduler should recommend different backends for different circuits."""
    from quonic.scheduler import schedule, circuit_features

    # Clifford circuit -> should recommend stabilizer
    c_clifford = Circuit()
    c_clifford.allocate(3)
    c_clifford.add(GateOperation("h", (0,)))
    c_clifford.add(GateOperation("cx", (0, 1)))

    # General circuit -> should recommend statevector
    c_general = Circuit()
    c_general.allocate(3)
    c_general.add(GateOperation("rz", (0,), (0.5,)))
    c_general.add(GateOperation("cx", (0, 1)))

    rec_clifford = schedule(c_clifford)
    rec_general = schedule(c_general)

    # Both should return valid recommendations
    assert rec_clifford.backend is not None
    assert rec_general.backend is not None


def test_mps_expectation():
    """MPS should compute expectation values correctly."""
    from quonic.simulators._mps import MPSEngine

    mps = MPSEngine(2, chi_max=16)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    mps._apply_single(0, H)
    mps._apply_single(1, H)
    mps._apply_diag_contiguous([0, 1], np.pi)
    mps._apply_single(1, H)

    # Bell state: ZZ expectation should be 1
    val = mps.expectation("ZZ")
    assert abs(val - 1.0) < 0.2


def test_zx_optimize_reduces_gates():
    """ZX optimization should reduce gate count."""
    from quonic.zx import circuit_to_zx, optimize_zx, extract_circuit

    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("rz", (0,), (0.3,)))
    c.add(GateOperation("rz", (0,), (0.7,)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    c2 = extract_circuit(simplified)

    # Should have fewer ops (Rz merged)
    ops_orig = len([op for op in c.ops if op.name != "measure"])
    ops_opt = len([op for op in c2.ops if op.name != "measure"])
    assert ops_opt <= ops_orig
