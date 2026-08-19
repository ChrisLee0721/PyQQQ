"""Deutsch-Jozsa: determine if f is constant or balanced in one query.

Classical requires 2^(n-1)+1 queries; quantum needs 1.
Output: all zeros = constant, anything else = balanced.
"""

from quonic import qgate
from quonic.algorithms import deutsch_jozsa
from quonic.gates import CX

N = 3

def balanced_oracle(circuit, n):
    """Balanced oracle: flip last qubit if first qubit is |1>."""
    qgate(CX, 0, n)

result = deutsch_jozsa(N, balanced_oracle, shots=100)
print(f"Counts: {result.counts}")
