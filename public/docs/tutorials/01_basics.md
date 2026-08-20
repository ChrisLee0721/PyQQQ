# Tutorial 01: Basics

Learn the fundamentals of QuoNic: building circuits, running them, and reading results.

## The Simplest Circuit

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)      # Hadamard on qubit 0
qgate(CX, 0, 1)  # CNOT: control=0, target=1
qshow()           # Run and display
```

This creates a Bell state. `qshow()` runs the circuit on the best available backend and prints the results.

## Understanding Qubits

In QuoNic, qubits are just numbers. `qgate(H, 0)` applies Hadamard to qubit 0. No circuit object to create, no qubit register to manage.

```python
qgate(X, 0)      # Pauli-X (bit flip) on qubit 0
qgate(H, 1)      # Hadamard on qubit 1
qgate(CX, 0, 1)  # CNOT: control=0, target=1
```

## Reading Results

`qshow()` returns a `Result` object with the measurement counts:

```python
result = qshow()
print(result.counts)  # {'00': 512, '11': 512} (for 1024 shots)
```

## Switching Backends

The same code runs on any backend:

```python
qshow(backend='qiskit')
qshow(backend='cirq')
qshow(backend='qulacs')
qshow(backend='native')
```

## GHZ State

```python
qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()  # |000> and |111> each ~50%
```

## What's Next

- [Tutorial 02: Algorithms](02_algorithms.md) — Grover, QFT, QPE
- [Tutorial 03: Noise Mitigation](03_noise_mitigation.md) — ZNE, readout calibration
