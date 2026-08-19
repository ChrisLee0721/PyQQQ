"""Jordan-Wigner transform: 2-site Hubbard model simulation.

Maps fermionic Hamiltonian to qubit Hamiltonian.
Output: ground state energy estimate.
"""

from quonic.algorithms import jordan_wigner_2site

result = jordan_wigner_2site(t=1.0, U=2.0)
print(result.counts)
