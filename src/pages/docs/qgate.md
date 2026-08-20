---
title: qgate()
---

# qgate()

Apply a quantum gate to specified qubits.

## Signature

```python
qgate(gate, *qubits, **params)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `gate` | Gate or str | Gate object or name string |
| `*qubits` | int | Qubit indices |
| `**params` | float | Gate parameters (for parametric gates) |

## Examples

```python
from quonic import qgate
from quonic.gates import H, CX, Ry

qgate(H, 0)           # Hadamard on qubit 0
qgate(CX, 0, 1)       # CNOT: control=0, target=1
qgate(Ry, 0, 0.5)     # Ry(0.5) on qubit 0
qgate("h", 0)          # Gate by name
```
