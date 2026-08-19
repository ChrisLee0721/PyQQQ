"""Tests for Krotov pulse optimization."""

from __future__ import annotations

import numpy as np

from quonic.pulse import krotov_optimize


def test_krotov_identity():
    """Krotov should find identity."""
    target = np.eye(2, dtype=complex)
    result = krotov_optimize(target, n_steps=20, maxiter=100)
    assert result.fidelity > 0.3


def test_krotov_x_gate():
    """Krotov should approximate X gate."""
    target = np.array([[0, 1], [1, 0]], dtype=complex)
    result = krotov_optimize(target, n_steps=30, maxiter=200, lambda_a=0.5)
    assert result.fidelity > 0.001


def test_krotov_result_fields():
    """KrotovResult should have all expected fields."""
    target = np.eye(2, dtype=complex)
    result = krotov_optimize(target, n_steps=10, maxiter=20)
    assert hasattr(result, "pulse")
    assert hasattr(result, "fidelity")
    assert hasattr(result, "n_iter")
    assert hasattr(result, "loss_history")
