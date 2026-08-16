"""Algorithm templates: Grover search / VQE / QAOA / QPE.

Each template depends only on numpy / scipy and is not tied to a specific
backend; sampling algorithms (Grover, QPE) can switch among the qiskit /
cirq / pennylane backends.
"""

from .grover import diffusion, grover, mark_state
from .hamiltonians import from_qiskit_nature
from .oracle import oracle
from .qaoa import qaoa_maxcut
from .qpe import qpe
from .quantum_counting import quantum_counting
from .shor import shor
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
]
