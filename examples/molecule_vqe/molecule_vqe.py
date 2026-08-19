"""Molecular VQE: compute ground state energy of a molecule.

Uses variational quantum eigensolver with chemistry-inspired ansatz.
Output: ground state energy.
"""

from quonic.algorithms import molecule_vqe_demo

result = molecule_vqe_demo(maxiter=200)
print(f"Ground state energy: {result.value}")
