# Tutorial 02: Algorithms

Explore QuoNic's 77 algorithm templates.

## Grover's Search

```python
from quonic import qgate, qshow
from quonic.gates import H, X
from quonic.algorithms.grover import grover_search

# Search for |11> in a 2-qubit space
circuit = grover_search(n=2, target="11")
qshow(circuit)
```

## Quantum Fourier Transform

```python
from quonic.algorithms.qft_algo import qft

circuit = qft(n=3)
qshow(circuit)
```

## VQE (Variational Quantum Eigensolver)

```python
from quonic.algorithms.vqe import vqe

# Find the ground state energy of a Hamiltonian
result = vqe(hamiltonian="ZZ", n_qubits=2, max_iter=100)
print(f"Ground state energy: {result['energy']:.4f}")
```

## QAOA (Quantum Approximate Optimization Algorithm)

```python
from quonic.algorithms.qaoa import qaoa

# Solve a MaxCut problem
result = qaoa(graph=graph, p=2)
print(f"MaxCut value: {result['cut_value']}")
```

## More Algorithms

QuoNic has 77 algorithm templates across 10 categories:

- **Foundational** (9): QFT, Deutsch-Jozsa, Bernstein-Vazirani, Simon, QPE
- **Search & Optimization** (9): Grover, QAOA (generic/TSP/MIS/knapsack), quantum counting
- **Quantum Chemistry** (8): VQE, Trotter, Hamiltonian simulation
- **Linear Algebra** (6): HHL, matrix inversion, eigenvalue solver
- **Communication & Crypto** (6): Teleportation, BB84, Shor
- **Hybrid ML** (7): VQC, quantum kernel, QNN, QSVM
- **Error Correction** (9): Bit/phase flip, Shor code, Steane, surface code
- **Statistical** (3): Quantum Monte Carlo, Bayesian inference
- **Algebraic** (3): Hidden subgroup, lattice, elliptic curve
- **Frontier** (10): QCNN, QGNN, QTransformer, QRL, QGAN

See the [Algorithm Report](../algorithm-report.md) for the full list.
