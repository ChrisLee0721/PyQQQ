# Compiler

QuoNic's compiler transforms quantum circuits for hardware execution.

## Features

- Gate decomposition
- Circuit optimization
- Qubit routing
- Gate fusion

## Usage

```python
from quonic.compile import compile_circuit

compiled = compile_circuit(circuit, backend='qiskit')
```

## Optimization Levels

- Level 0: No optimization
- Level 1: Basic optimization (gate cancellation)
- Level 2: Full optimization (gate fusion, routing)
