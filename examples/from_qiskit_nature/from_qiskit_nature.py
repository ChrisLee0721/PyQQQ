"""from_qiskit_nature: import a Pauli Hamiltonian from Qiskit.

Build H = Z⊗Z + X⊗I + I⊗X as a SparsePauliOp, convert it to the
[(coeff, pauli), ...] form that vqe() expects, then solve for the
ground energy (exact value -√5 ~ -2.236).

Requires qiskit and scipy: pip install 'quonic[algorithms]'.
"""

from qiskit.quantum_info import SparsePauliOp

from quonic.algorithms import from_qiskit_nature, vqe

op = SparsePauliOp.from_list([("ZZ", 1.0), ("XI", 1.0), ("IX", 1.0)])
terms = from_qiskit_nature(op)
print(terms)  # [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]

result = vqe(terms, 2, maxiter=200)
print(result.value)  # ~ -2.236
