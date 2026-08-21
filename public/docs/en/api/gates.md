# Quantum Gates

QuoNic provides a comprehensive set of quantum gates.

## Single-Qubit Gates

| Gate | Description |
|------|-------------|
| `X` | Pauli-X (NOT) |
| `Y` | Pauli-Y |
| `Z` | Pauli-Z |
| `H` | Hadamard |
| `S` | Phase gate |
| `T` | T gate |

## Multi-Qubit Gates

| Gate | Description |
|------|-------------|
| `CX` | CNOT |
| `CZ` | Controlled-Z |
| `CCX` | Toffoli |
| `SWAP` | SWAP |

## Rotation Gates

| Gate | Description |
|------|-------------|
| `Rx(θ)` | X rotation |
| `Ry(θ)` | Y rotation |
| `Rz(θ)` | Z rotation |

## Usage

```python
from quonic import qgate
from quonic.gates import H, CX, Rx

qgate(H, 0)
qgate(CX, 0, 1)
qgate(Rx(3.14), 2)
```
