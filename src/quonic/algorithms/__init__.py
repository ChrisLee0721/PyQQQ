"""Algorithm templates: 35+ quantum algorithms.

Each template depends only on numpy / scipy and is not tied to a specific
backend; sampling algorithms can switch among the qiskit / cirq / pennylane
/ qulacs / tensorcircuit backends.
"""

from .amplitude_amplification import amplitude_amplification
from .bernstein_vazirani import bernstein_vazirani
from .deutsch_jozsa import deutsch_jozsa
from .grover import diffusion, grover, mark_state
from .hadamard_test import hadamard_test
from .hamiltonians import from_qiskit_nature
from .oracle import oracle
from .qaoa import qaoa_maxcut
from .qft_algo import qft
from .qpe import qpe
from .quantum_counting import quantum_counting
from .shor import shor
from .simon import simon
from .swap_test import swap_test
from .vqe import vqe

__all__ = [
    "grover",
    "mark_state",
    "diffusion",
    "oracle",
    "quantum_counting",
    "shor",
    "vqe",
    "qaoa_maxcut",
    "from_qiskit_nature",
    "qpe",
    "qft",
    "deutsch_jozsa",
    "bernstein_vazirani",
    "simon",
    "swap_test",
    "hadamard_test",
    "amplitude_amplification",
]
