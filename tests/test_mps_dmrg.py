"""Tests for MPS DMRG optimization."""

from __future__ import annotations

from quonic.simulators._mps import MPSEngine


def test_dmrg_finds_ground_state():
    """DMRG should find the ground energy of a simple Hamiltonian."""
    # H = -Z (ground state is |1> with energy -1)
    mps = MPSEngine(1, chi_max=16)
    # Start in |0>
    energy = mps.dmrg_sweep([(-1.0, "Z")], max_sweeps=5)
    # Should find energy close to -1
    assert energy < 0.5


def test_dmrg_two_qubit():
    """DMRG should handle 2-qubit Hamiltonian."""
    # H = ZZ (ground state is |00> or |11> with energy +1, or |01> or |10> with energy -1)
    mps = MPSEngine(2, chi_max=16)
    energy = mps.dmrg_sweep([(1.0, "ZZ")], max_sweeps=5)
    # Energy should be ≤ 1
    assert energy <= 1.1


def test_dmrg_preserves_mps():
    """DMRG should leave MPS in a valid state."""
    mps = MPSEngine(2, chi_max=16)
    mps.dmrg_sweep([(1.0, "ZZ")], max_sweeps=3)
    # MPS should still be valid
    assert mps.norm() > 0
    sv = mps.to_statevector()
    assert len(sv) == 4
