"""Grover search: find |11> among 2 qubits.

Passing a bitstring auto-generates the oracle; one iteration hits with high probability.
Output: almost all |11>.
"""

from quonic.algorithms import grover

result = grover("11", 2, shots=1024)
print(result.counts)
