"""SWAP test: estimate overlap between two quantum states.

Output: P(|0>) = (1 + |<a|b>|^2) / 2, so high P means similar states.
"""

from quonic import qgate
from quonic.algorithms import swap_test
from quonic.gates import X


# prepare(circuit, qubit_index, n_qubits)
def prep_a(circuit, q, n):
    pass  # |0>

def prep_b(circuit, q, n):
    qgate(X, q)  # |1> — orthogonal to |0>

result = swap_test(1, prep_a, prep_b, shots=10000)
print(result.counts)
