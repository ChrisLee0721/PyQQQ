---
title: Quick Start
---

# Quick Start

## Install

```bash
pip install quonic
```

## Your First Circuit

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)      # Hadamard on qubit 0
qgate(CX, 0, 1)  # CNOT: entangle qubits
qshow()           # Run and display
```

Output:
```
backend: native | shots: 1024
Result:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################
```

## Switch Backend

```python
qshow(backend='qiskit')      # IBM Qiskit
qshow(backend='cirq')        # Google Cirq
qshow(backend='qulacs')      # Qulacs (fast C++)
```

## Add Noise

```python
qshow(noise=0.05)  # 5% depolarizing noise
```

## Run Algorithms

```python
from quonic.algorithms import grover, vqe, qft

# Grover search
result = grover("11", 2, shots=1024)

# VQE for chemistry
result = vqe(H2_hamiltonian, n_qubits=2)

# Quantum Fourier Transform
result = qft(n_qubits=4, shots=1024)
```
