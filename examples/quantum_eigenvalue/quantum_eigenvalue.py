"""Quantum eigenvalue estimation demo.

Estimates eigenvalues of a unitary operator.
Output: eigenvalue estimates.
"""

from quonic.algorithms import quantum_eigenvalue_demo

result = quantum_eigenvalue_demo()
print(result.counts)
