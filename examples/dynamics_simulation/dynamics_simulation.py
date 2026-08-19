"""Quantum dynamics simulation: simulate time evolution of a quantum system.

Uses Trotterization to approximate e^{-iHt}.
Output: evolved state measurements.
"""

from quonic.algorithms import dynamics_simulation_demo

result = dynamics_simulation_demo(n_steps=10, shots=1024)
print(result.counts)
