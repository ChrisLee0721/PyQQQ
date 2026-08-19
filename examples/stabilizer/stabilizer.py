"""Stabilizer formalism demo.

Demonstrates Clifford group simulation via stabilizer tableau.
Output: stabilizer state measurements.
"""

from quonic.algorithms import stabilizer_demo

result = stabilizer_demo(n_qubits=3, shots=100)
print(result.counts)
