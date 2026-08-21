# Quick Start

Get started with QuoNic in 5 minutes: three core concepts, three examples.

## Three Core Concepts

| Concept | Purpose |
|---------|---------|
| **`qgate(gate, *qubits)`** | Add a gate to the circuit. Gate objects are imported from `quonic.gates` (recommended), strings also supported (e.g., `qgate("h", 0)`) |
| **`qshow()`** | Run the current circuit and display results. Qubits without explicit measurement are auto-measured; circuit is cleared after execution |
| **`reset()`** | Clear all qubits and start fresh |

## Example 1: Bell State

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)      # Hadamard on qubit 0
qgate(CX, 0, 1)  # CNOT: control=0, target=1
qshow()
```

Output:
```
backend: native | shots: 1024
Result:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################
```

## Example 2: Grover Search

```python
from quonic.algorithms import grover

result = grover("11", 2, shots=1024)
print(result.counts)
# Output: {'11': 1008, '00': 6, '01': 5, '10': 5}
```

## Example 3: Quantum Teleportation

```python
import math
from quonic import qgate, qshow
from quonic.gates import CX, CZ, H, Ry

qgate(Ry(math.pi / 3), 0)
qgate(H, 1)
qgate(CX, 1, 2)
qgate(CX, 0, 1)
qgate(H, 0)
qgate(CX, 1, 2)
qgate(CX, 0, 2)
qgate(CZ, 0, 2)
qshow()
```

## Installation

```bash
pip install quonic
```

## Next Steps

- [Basics Tutorial](tutorials/basics.md) - Learn the fundamentals
- [Algorithms](tutorials/algorithms.md) - Quantum algorithms
- [Examples](examples/example_bell.html) - All examples
