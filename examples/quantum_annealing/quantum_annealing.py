"""Quantum annealing with hybrid classical-quantum solver.

Simulates quantum annealing for optimization problems.
Output: approximate ground state.
"""

from quonic.algorithms import quantum_annealing_hybrid_demo

result = quantum_annealing_hybrid_demo(n_spins=4, n_steps=100)
print(result.counts)
