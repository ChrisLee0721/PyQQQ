"""Quantum ODE solver demo.

Quantum algorithm for solving ordinary differential equations.
Output: solution trajectory.
"""

from quonic.algorithms import quantum_ode_demo

result = quantum_ode_demo(shots=1024)
print(result.counts)
