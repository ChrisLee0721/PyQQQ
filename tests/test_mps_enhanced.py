"""Tests for enhanced MPS simulator features."""

from __future__ import annotations

import numpy as np

from quonic.simulators._mps import MPSEngine


def test_mps_bell_state():
    """MPS should produce correct Bell state sampling."""
    mps = MPSEngine(2, chi_max=16)
    # H on qubit 0
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    mps._apply_single(0, H)
    # CX(0,1) via diagonal trick
    mps._apply_single(1, H)
    mps._apply_diag_contiguous([0, 1], np.pi)
    mps._apply_single(1, H)

    counts = mps.sample(1000)
    assert set(counts) <= {"00", "11"}
    assert abs(counts.get("00", 0) / 1000 - 0.5) < 0.15


def test_mps_expectation_z():
    """MPS expectation of Z on |0> should be +1."""
    mps = MPSEngine(1)
    val = mps.expectation("Z")
    assert abs(val - 1.0) < 1e-10


def test_mps_expectation_z_after_x():
    """MPS expectation of Z on |1> should be -1."""
    mps = MPSEngine(1)
    mps._apply_single(0, np.array([[0, 1], [1, 0]], dtype=complex))
    val = mps.expectation("Z")
    assert abs(val - (-1.0)) < 1e-10


def test_mps_expectation_zz_bell():
    """MPS expectation of ZZ on Bell state should be +1."""
    mps = MPSEngine(2, chi_max=16)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    mps._apply_single(0, H)
    mps._apply_single(1, H)
    mps._apply_diag_contiguous([0, 1], np.pi)
    mps._apply_single(1, H)
    val = mps.expectation("ZZ")
    assert abs(val - 1.0) < 0.1


def test_mps_to_statevector():
    """MPS statevector should match direct computation for small circuits."""
    mps = MPSEngine(2)
    sv = mps.to_statevector()
    expected = np.array([1, 0, 0, 0], dtype=complex)
    np.testing.assert_allclose(sv, expected, atol=1e-10)


def test_mps_bond_dimensions():
    """Initial MPS should have bond dimension 1."""
    mps = MPSEngine(3)
    assert mps.bond_dimensions() == [1, 1]


def test_mps_entropy_zero_state():
    """Entropy of |00> should be 0."""
    mps = MPSEngine(2)
    assert abs(mps.entropy(1)) < 1e-10


def test_mps_entropy_bell_state():
    """Entropy of Bell state at bipartition should be log(2)."""
    mps = MPSEngine(2, chi_max=16)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    mps._apply_single(0, H)
    mps._apply_single(1, H)
    mps._apply_diag_contiguous([0, 1], np.pi)
    mps._apply_single(1, H)
    S = mps.entropy(0)
    assert abs(S - np.log(2)) < 0.1
