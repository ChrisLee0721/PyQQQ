# Distributed Computing

QuoNic supports distributed quantum computing across multiple backends.

## Features

- Multi-backend execution
- Circuit splitting
- Result aggregation

## Usage

```python
from quonic.distributed import distribute

result = distribute(circuit, backends=['qiskit', 'cirq'])
```
