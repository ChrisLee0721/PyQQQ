"""Tests for MPS canonical form."""

from __future__ import annotations

import numpy as np

from quonic.simulators._mps import MPSEngine


def test_canonicalize_left():
    """After canonicalize(1), M[0] should be left-canonical."""
    mps = MPSEngine(3, chi_max=16)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    mps._apply_single(0, H)
    mps._apply_diag_contiguous([0, 1], np.pi)
    mps._apply_single(1, H)

    mps.canonicalize(ortho_center=1)
    assert mps.is_left_canonical(0)


def test_canonicalize_right():
    """After canonicalize(n-1), M[n-1] should be right-canonical."""
    mps = MPSEngine(3, chi_max=16)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    mps._apply_single(0, H)
    mps._apply_diag_contiguous([0, 1], np.pi)

    mps.canonicalize(ortho_center=2)
    assert mps.is_right_canonical(2)


def test_canonicalize_preserves_state():
    """Canonicalization should not change the physical state."""
    mps = MPSEngine(2, chi_max=16)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    # Create Bell state: H(0), H(1), CZ, H(1) = CX(0,1)
    mps._apply_single(0, H)
    mps._apply_single(1, H)
    mps._apply_diag_contiguous([0, 1], np.pi)
    mps._apply_single(1, H)

    sv_before = mps.to_statevector()
    mps.canonicalize()
    sv_after = mps.to_statevector()

    np.testing.assert_allclose(sv_before, sv_after, atol=1e-10)


def test_canonicalize_improves_stability():
    """Canonical form should give correct expectation values."""
    mps = MPSEngine(2, chi_max=16)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    mps._apply_single(0, H)
    mps._apply_single(1, H)
    mps._apply_diag_contiguous([0, 1], np.pi)
    mps._apply_single(1, H)

    mps.canonicalize()
    val = mps.expectation("ZZ")
    assert abs(val - 1.0) < 0.1


def test_norm():
    """Norm of normalized state should be 1."""
    mps = MPSEngine(2, chi_max=16)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    mps._apply_single(0, H)
    mps._apply_single(1, H)
    mps._apply_diag_contiguous([0, 1], np.pi)
    mps._apply_single(1, H)

    assert abs(mps.norm() - 1.0) < 1e-10


def test_is_left_canonical_initial():
    """Initial |0> state should be left-canonical."""
    mps = MPSEngine(2)
    assert mps.is_left_canonical(0)
