"""Hamiltonian simulation via Trotterization.

Simulates e^{-iHt} for a given Hamiltonian H.
Output: evolved state measurements.
"""

from quonic.algorithms import hamiltonian_simulation_demo

result = hamiltonian_simulation_demo()
print(result.counts)
