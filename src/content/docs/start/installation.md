---
title: Installation
description: Install QuoNic and optional dependencies
---

# Installation

## Basic Install

```bash
pip install quonic
```

## With Specific Backends

```bash
pip install 'quonic[qiskit]'        # IBM Qiskit
pip install 'quonic[cirq]'          # Google Cirq
pip install 'quonic[pennylane]'     # PennyLane
pip install 'quonic[qulacs]'        # Qulacs
```

## All Backends

```bash
pip install 'quonic[all-sim]'       # All simulators
pip install 'quonic[all-hw]'        # All hardware backends
pip install 'quonic[all]'           # Everything
```

## GPU Support

```bash
pip install 'quonic[gpu]'           # CuPy (NVIDIA CUDA)
```

## Visualization

```bash
pip install 'quonic[viz]'           # matplotlib
```

## Algorithms

```bash
pip install 'quonic[algorithms]'    # scipy for VQE/QAOA
```

## Verify Installation

```python
import quonic
print(quonic.__version__)

# Test basic functionality
from quonic import qgate, qshow
from quonic.gates import H
qgate(H, 0)
qshow()
```
