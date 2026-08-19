"""Tests for the quantum machine learning module."""

from __future__ import annotations

import math

import numpy as np

from quonic.ml import (
    Ansatz,
    SPSAOptimizer,
    amplitude_encode,
    angle_encode,
    expectation_loss,
    fidelity_loss,
    train,
)

# ---------------------------------------------------------------------------
# 1. Ansatz
# ---------------------------------------------------------------------------


def test_hardware_efficient_ansatz():
    ansatz = Ansatz.hardware_efficient(n_qubits=2, layers=2)
    assert ansatz.n_params == 2 * 2  # n_qubits * layers
    circuit = ansatz.build([0.1, 0.2, 0.3, 0.4])
    assert circuit.num_qubits == 2
    assert len(circuit.ops) > 0


def test_qaoa_ansatz():
    ansatz = Ansatz.qaoa(n_qubits=3, p=1)
    assert ansatz.n_params == 6  # 2 * n_qubits * p
    circuit = ansatz.build([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    assert circuit.num_qubits == 3


# ---------------------------------------------------------------------------
# 2. Encoding
# ---------------------------------------------------------------------------


def test_angle_encode():
    circ = angle_encode([math.pi / 2, math.pi])
    assert circ.num_qubits == 2
    ops = [op for op in circ.ops if op.name != "measure"]
    assert all(op.name == "ry" for op in ops)


def test_amplitude_encode():
    circ = amplitude_encode([0.7, 0.3, 0.5, 0.5])
    assert circ.num_qubits == 2


# ---------------------------------------------------------------------------
# 3. Optimizer
# ---------------------------------------------------------------------------


def test_spsa_optimizer():
    opt = SPSAOptimizer(maxiter=5)
    params = opt.init(3)
    assert len(params) == 3
    grad = np.array([0.1, 0.2, 0.3])
    new_params = opt.step(params, grad)
    assert len(new_params) == 3
    assert opt.step_num == 1


# ---------------------------------------------------------------------------
# 4. Loss functions
# ---------------------------------------------------------------------------


def test_expectation_loss():
    from quonic.ir import Circuit, GateOperation
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("x", (0,)))  # |1>
    loss = expectation_loss(c, "Z")
    # <1|Z|1> = -1
    assert abs(loss - (-1.0)) < 0.01


def test_fidelity_loss():
    from quonic.ir import Circuit, GateOperation
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("x", (0,)))  # |1>
    target = np.array([0, 1], dtype=complex)
    loss = fidelity_loss(c, target)
    # perfect match → loss = 0
    assert abs(loss) < 0.01


# ---------------------------------------------------------------------------
# 5. Trainer
# ---------------------------------------------------------------------------


def test_train():
    ansatz = Ansatz.hardware_efficient(n_qubits=1, layers=1)
    opt = SPSAOptimizer(maxiter=5)
    result = train(ansatz, opt, lambda p: p[0] ** 2)
    assert result.n_steps == 5
    assert len(result.loss_history) == 5
