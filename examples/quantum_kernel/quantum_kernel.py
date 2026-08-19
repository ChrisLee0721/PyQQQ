"""Quantum kernel estimation.

Computes quantum kernel matrix for machine learning.
Output: kernel matrix entries.
"""

from quonic.algorithms import quantum_kernel

X = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
result = quantum_kernel(X, n_qubits=2, shots=10000)
print(result.counts)
