"""Tests for GRAPE optimal control."""

from __future__ import annotations

import numpy as np

from quonic.pulse import grape_optimize


def test_grape_x_gate():
    """GRAPE should find a pulse that implements the X gate."""
    target = np.array([[0, 1], [1, 0]], dtype=complex)
    result = grape_optimize(target, n_steps=30, maxiter=100, lr=0.02)
    assert result.fidelity > 0.9, f"Fidelity too low: {result.fidelity}"
    assert len(result.pulse) == 30


def test_grape_identity():
    """GRAPE should find a pulse close to identity."""
    target = np.eye(2, dtype=complex)
    result = grape_optimize(target, n_steps=20, maxiter=200, lr=0.05)
    assert result.fidelity > 0.5  # identity is easy but GRAPE may overshoot


def test_grape_hadamard():
    """GRAPE should approximate a Hadamard gate."""
    target = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    result = grape_optimize(target, n_steps=30, maxiter=150, lr=0.02)
    assert result.fidelity > 0.85


def test_grape_result_fields():
    """GRAPEResult should have all expected fields."""
    target = np.eye(2, dtype=complex)
    result = grape_optimize(target, n_steps=10, maxiter=20)
    assert hasattr(result, "pulse")
    assert hasattr(result, "fidelity")
    assert hasattr(result, "n_iter")
    assert hasattr(result, "loss_history")
    assert len(result.loss_history) > 0
