"""Tests for MPS custom gate support and noise."""

from __future__ import annotations

import numpy as np

from quonic.gates import Gate
from quonic.simulators._mps import MPSEngine


def test_mps_custom_gate():
    """MPS should support custom gates via _GATE_REGISTRY."""
    # Register a custom T gate
    t_mat = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
    Gate.from_matrix("test_t_mps", t_mat)

    mps = MPSEngine(1, chi_max=16)
    mps.apply("test_t_mps", [0])

    sv = mps.to_statevector()
    expected = np.array([1, 0], dtype=complex)
    np.testing.assert_allclose(sv, expected, atol=1e-10)


def test_mps_custom_gate_rotation():
    """Custom Ry gate should rotate the state."""
    theta = np.pi / 3
    ry_mat = np.array(
        [[np.cos(theta / 2), -np.sin(theta / 2)],
         [np.sin(theta / 2), np.cos(theta / 2)]],
        dtype=complex,
    )
    Gate.from_matrix("test_ry_mps", ry_mat)

    mps = MPSEngine(1, chi_max=16)
    mps.apply("test_ry_mps", [0])

    sv = mps.to_statevector()
    expected = np.array([np.cos(theta / 2), np.sin(theta / 2)], dtype=complex)
    np.testing.assert_allclose(sv, expected, atol=1e-10)


def test_mps_noise_depolarizing():
    """Depolarizing noise should corrupt the state with some probability."""
    mps = MPSEngine(1, chi_max=16)
    # Apply X to get |1>
    mps._apply_single(0, np.array([[0, 1], [1, 0]], dtype=complex))

    # Apply very high noise — should definitely corrupt
    np.random.seed(42)
    for _ in range(100):
        mps_copy = MPSEngine(1, chi_max=16)
        mps_copy._apply_single(0, np.array([[0, 1], [1, 0]], dtype=complex))
        mps_copy.apply_noise([0], p=0.99)
        sv = mps_copy.to_statevector()
        # With high noise, state should sometimes not be |1>
        if abs(sv[0]) > 0.1:
            break
    else:
        # All 100 trials stayed as |1> — noise isn't working
        assert False, "Noise never corrupted the state"


def test_mps_noise_zero_probability():
    """Zero noise probability should not change the state."""
    mps = MPSEngine(1, chi_max=16)
    mps._apply_single(0, np.array([[0, 1], [1, 0]], dtype=complex))
    sv_before = mps.to_statevector()

    mps.apply_noise([0], p=0.0)
    sv_after = mps.to_statevector()

    np.testing.assert_allclose(sv_before, sv_after, atol=1e-10)
