"""Quantum walk on a line.

The quantum analogue of a random walk — spreads quadratically faster.
Output: position distribution after n steps.
"""

from quonic.algorithms import quantum_walk

result = quantum_walk(n_positions=5, steps=10, shots=1024)
print(result.counts)
