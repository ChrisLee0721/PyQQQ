"""Quantum matrix inversion demo.

HHL-based matrix inversion for linear systems.
Output: solution vector.
"""

from quonic.algorithms import quantum_matrix_inversion_demo

result = quantum_matrix_inversion_demo()
print(result.counts)
