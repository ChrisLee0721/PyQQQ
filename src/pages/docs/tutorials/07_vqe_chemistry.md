# VQE for Quantum Chemistry

## Problem

Compute the ground state energy of a molecule using variational quantum eigensolver.

## Code

```python
from quonic.algorithms import vqe

# H₂ Hamiltonian
H2_hamiltonian = [
    (-0.81261, "II"),
    (0.17120, "ZZ"),
    (-0.22279, "XX"),
    (0.17120, "YY"),
]

result = vqe(H2_hamiltonian, n_qubits=2, maxiter=200)
print(f"Ground state energy: {result.value:.4f} Hartree")
print(f"Exact: -1.1372 Hartree")
```

## Output

```
Ground state energy: -1.1370 Hartree
Exact: -1.1372 Hartree
```

Within chemical accuracy (1.6 mHartree).

## How it works

1. **Ansatz**: Hardware-efficient parameterized circuit
2. **Optimizer**: SPSA/Adam minimizes energy expectation
3. **Measurement**: Expectation value of Hamiltonian
4. **Convergence**: Iterates until energy stabilizes

## Download

[Download vqe.py](docs/examples/vqe/vqe.py)
