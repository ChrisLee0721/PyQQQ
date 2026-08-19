"""Quantum Monte Carlo integration demo.

Quantum speedup for Monte Carlo methods.
Output: estimated integral value.
"""

from quonic.algorithms import quantum_monte_carlo_demo

result = quantum_monte_carlo_demo(n_qubits=2, shots=1024)
print(f"Estimated value: {result.value}")
