"""Quantum PDE solver demo.

Quantum algorithm for solving partial differential equations.
Output: solution field.
"""

from quonic.algorithms import quantum_pde_demo

result = quantum_pde_demo(shots=1024)
print(result.counts)
