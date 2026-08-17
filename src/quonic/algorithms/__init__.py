"""Algorithm templates: 67 quantum algorithms.

Each template depends only on numpy / scipy and is not tied to a specific
backend; sampling algorithms can switch among the qiskit / cirq / pennylane
/ qulacs / tensorcircuit backends.
"""

from .amplitude_amplification import amplitude_amplification
from .bb84 import bb84
from .bernstein_vazirani import bernstein_vazirani
from .bit_flip_code import bit_flip_code
from .color_code import color_code_demo
from .deutsch_jozsa import deutsch_jozsa
from .discrete_log import discrete_log_demo
from .dqaoa import dqaoa_demo
from .e91 import e91
from .eigenvalue_solver import quantum_eigenvalue_demo
from .fermion_mapping import jordan_wigner_2site
from .ft_gates import ft_gate_demo
from .grover import diffusion, grover, mark_state
from .hadamard_test import hadamard_test
from .hamiltonians import from_qiskit_nature
from .hamiltonians_ext import from_openfermion, from_pauli_string, from_pennylane
from .hhl import hhl_demo
from .matrix_inversion import quantum_matrix_inversion_demo
from .molecule_vqe import molecule_vqe_demo
from .oracle import oracle
from .phase_flip_code import phase_flip_code
from .qaoa import qaoa_maxcut
from .qaoa_generic import qaoa
from .qaoa_knapsack import qaoa_knapsack
from .qaoa_mis import qaoa_mis
from .qaoa_tsp import qaoa_tsp
from .qbm import qbm_demo
from .qcnn import qcnn_demo
from .qft_algo import qft
from .qgan import qgan_demo
from .qgnn import qgnn_demo
from .qng import qng_demo
from .qpca import qpca_demo
from .qpe import qpe
from .qrl import qrl_demo
from .qtda import qtda_demo
from .qtransformer import qtransformer_demo
from .quantum_bayesian import quantum_bayesian_demo
from .quantum_clustering import quantum_clustering_demo
from .quantum_counting import quantum_counting
from .quantum_fitting import quantum_fitting_demo
from .quantum_kernel import quantum_kernel
from .quantum_monte_carlo import quantum_monte_carlo_demo
from .quantum_ode import quantum_ode_demo
from .quantum_pde import quantum_pde_demo
from .quantum_walk import quantum_walk
from .rejection_sampling import rejection_sampling_demo
from .shor import shor
from .shor_code import shor_code
from .simon import simon
from .stabilizer import stabilizer_demo
from .steane_code import steane_code
from .superdense_coding import superdense_coding
from .surface_code import surface_code_demo
from .swap_test import swap_test
from .syndrome import syndrome_demo
from .teleportation import teleportation
from .trotter import trotter
from .vqc import vqc
from .vqe import vqe
from .vqr import vqr

__all__ = [
    # Existing
    "grover", "mark_state", "diffusion", "oracle",
    "quantum_counting", "shor", "vqe", "qaoa", "qaoa_maxcut",
    "from_qiskit_nature", "qpe",
    # Phase 1: Foundational
    "qft", "deutsch_jozsa", "bernstein_vazirani", "simon",
    "swap_test", "hadamard_test", "amplitude_amplification",
    # Phase 2: Search & Optimization
    "qaoa_tsp", "qaoa_mis", "qaoa_knapsack", "quantum_walk",
    # Phase 3: Chemistry
    "from_pauli_string", "from_openfermion", "from_pennylane",
    "trotter", "jordan_wigner_2site", "molecule_vqe_demo",
    # Phase 4: Linear Algebra
    "hhl_demo", "quantum_matrix_inversion_demo", "quantum_eigenvalue_demo",
    "quantum_pde_demo", "quantum_ode_demo", "quantum_fitting_demo",
    # Phase 5: Communication
    "teleportation", "bb84", "e91", "superdense_coding", "discrete_log_demo",
    # Phase 6: Hybrid
    "vqc", "quantum_kernel", "qng_demo", "vqr",
    # Phase 7: Error Correction
    "bit_flip_code", "phase_flip_code", "shor_code", "steane_code",
    "stabilizer_demo", "syndrome_demo", "surface_code_demo", "color_code_demo",
    "ft_gate_demo",
    # Phase 8: Statistical
    "quantum_monte_carlo_demo", "rejection_sampling_demo", "quantum_bayesian_demo",
    # Phase 9: Minimal Demos
    "qcnn_demo", "qgnn_demo", "dqaoa_demo", "qtransformer_demo",
    "qrl_demo", "qtda_demo", "qpca_demo", "quantum_clustering_demo",
    "qgan_demo", "qbm_demo",
]
