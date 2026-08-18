# QuoNic — Quantum Programming, as Simple as Writing Python

[![CI](https://github.com/ChrisLee0721/QuoNic/actions/workflows/ci.yml/badge.svg)](https://github.com/ChrisLee0721/QuoNic/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.5.0-purple.svg)](changelog.md)

**QuoNic makes quantum programming as simple as writing Python.**

No `QuantumCircuit` to learn, no `backend` to understand, no manual `measure`. If you can write Python, you can write quantum programs.

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

This is the Bell state — the most classic result in quantum computing. The same thing takes 10+ lines in raw Qiskit. QuoNic does it in 3.

## Features

- **12 backends**: Qiskit, Cirq, PennyLane, Qulacs, TensorCircuit, CUDA-Q, MindQuantum, QPanda3, CqLib, CuPy, native, Quantum Inspire
- **GPU acceleration**: `method="gpu"` with smart scheduling across backends
- **77 algorithm templates**: from Grover to VQE to QAOA to quantum error correction
- **Error mitigation**: ZNE (linear/exponential), readout calibration (per-qubit/correlated)
- **Quantum control flow**: `qif` (superposition), `cif` (classical), `cwhile` (repeat-until-success)
- **23 visualization types**: circuit diagrams, histograms, Bloch spheres, and more

## Installation

```bash
pip install quonic
```

Backends are optional — install only what you need:

```bash
pip install 'quonic[qiskit]'        # Qiskit + Aer
pip install 'quonic[qulacs]'        # Qulacs
pip install 'quonic[gpu]'           # CuPy GPU engine
pip install 'quonic[all-sim]'       # All simulators
```

## Documentation

- [Quick Start](quickstart.md) — 5-minute getting started guide
- [API Reference](api/ir.md) — Complete API documentation
- [Tutorials](tutorials/01_basics.md) — Step-by-step tutorials
- [Examples](examples.md) — Copy-and-run examples
- [Benchmarks](benchmarks.md) — Performance data

## Links

- [GitHub](https://github.com/ChrisLee0721/QuoNic)
- [PyPI](https://pypi.org/project/quonic/)
- [Changelog](changelog.md)
