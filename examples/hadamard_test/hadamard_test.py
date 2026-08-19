"""Hadamard test: estimate Re(<psi|U|psi>).

A primitive for many quantum algorithms (inner product estimation).
Output: probability of measuring |0> encodes the real part.
"""

from quonic import qgate
from quonic.algorithms import hadamard_test
from quonic.gates import X

# prepare_psi(circuit, qubit_index, n_qubits)
def prep_psi(circuit, q, n):
    qgate(X, q)  # |1>

# apply_u(circuit, qubit_index)
def apply_u(circuit, q):
    pass  # Identity

result = hadamard_test(1, prep_psi, apply_u, shots=10000)
print(result.counts)
