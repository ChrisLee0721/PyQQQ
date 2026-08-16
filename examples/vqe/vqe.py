"""VQE: variational ground-state energy.

H = Z⊗Z + X⊗I + I⊗X has exact ground energy -√5 ≈ -2.236.
Requires scipy: pip install 'quonic[algorithms]'.
"""

from quonic.algorithms import vqe

hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)  # ≈ -2.236
