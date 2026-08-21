# Intermediate Representation

QuoNic uses an intermediate representation (IR) for circuit manipulation.

## Features

- Circuit optimization
- Gate decomposition
- Backend-specific transformations

## Usage

```python
from quonic.ir import to_ir, from_ir

ir = to_ir(circuit)
optimized = ir.optimize()
circuit = from_ir(optimized)
```
