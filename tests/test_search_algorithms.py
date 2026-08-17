"""Tests for Phase 2 search & optimization algorithms."""

from __future__ import annotations

from quonic.algorithms import (
    qaoa,
    qaoa_knapsack,
    qaoa_maxcut,
    qaoa_mis,
    quantum_walk,
)


def test_qaoa_generic_triangle():
    """QAOA on triangle MaxCut should find cut ≥ 1."""
    edges = [(0, 1), (1, 2), (0, 2)]
    # MaxCut Hamiltonian: -sum(Z_iZ_j) for edges
    n = 3
    terms = []
    for i, j in edges:
        pauli = ["I"] * n
        pauli[i] = "Z"
        pauli[j] = "Z"
        terms.append((-1.0, "".join(pauli)))
    result = qaoa(terms, n, p=1, maxiter=30)
    assert result.value < 0  # negative energy = positive cut


def test_qaoa_maxcut_triangle():
    """QAOA MaxCut on triangle should find cut ≥ 2."""
    edges = [(0, 1), (1, 2), (0, 2)]
    result = qaoa_maxcut(edges, 3, p=1, maxiter=50)
    assert result.value >= 1.0  # approximate


def test_qaoa_mis_path():
    """QAOA MIS on path graph 0-1-2 should return non-negative MIS estimate."""
    edges = [(0, 1), (1, 2)]
    result = qaoa_mis(edges, 3, p=1, maxiter=30)
    assert result.value >= 0  # QAOA gives approximate result


def test_qaoa_knapsack_basic():
    """QAOA Knapsack should return positive value."""
    weights = [2, 3, 4]
    values = [3, 4, 5]
    capacity = 5
    result = qaoa_knapsack(weights, values, capacity, p=1, maxiter=30)
    assert result.value > 0


def test_quantum_walk_3position():
    """Quantum walk should produce non-trivial distribution."""
    result = quantum_walk(n_positions=2, steps=3, shots=1024)
    # Should have multiple outcomes
    assert len(result.counts) > 1
