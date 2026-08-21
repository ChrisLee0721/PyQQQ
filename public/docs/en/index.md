# QuoNic — Quantum Programming, as Simple as Writing Python

[![CI](https://github.com/ChrisLee0721/QuoNic/actions/workflows/ci.yml/badge.svg)](https://github.com/ChrisLee0721/QuoNic/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

## Three Lines of Code, One Bell State

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0); qgate(CX, 0, 1); qshow()
```

## Why QuoNic?

| Feature | QuoNic | Qiskit | Cirq |
|---------|--------|--------|------|
| Lines of code | 3 | 15 | 12 |
| Learning time | 5 min | 30 min | 20 min |
| Backends | 12+ | 5 | 3 |
| GPU acceleration | ✅ | ❌ | ✅ |

## 12+ Quantum Backends

```python
qshow(backend='native')    # Local simulator
qshow(backend='qiskit')    # IBM Qiskit
qshow(backend='cirq')      # Google Cirq
qshow(backend='gpu')       # GPU accelerated
qshow(backend='cudaq')     # NVIDIA CUDA-Q
```

## 77 Algorithm Templates

- Basics: Bell state, GHZ state, quantum teleportation
- Algorithms: Grover, Shor, VQE, QAOA
- Error correction: bit flip code, Shor code, surface code
- Machine learning: QNN, QSVM, QGAN

## Quick Start

```bash
pip install quonic
python -c "from quonic import qgate, qshow; qgate('h', 0); qshow()"
```

## Next Steps

- [Quick Start](quickstart.md) - Get started in 5 minutes
- [Basics Tutorial](tutorials/basics.md) - Learn the fundamentals
- [Examples](examples/example_bell.html) - All examples
