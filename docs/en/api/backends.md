# Backends

QuoNic supports 12+ quantum backends.

## Available Backends

| Backend | Description |
|---------|-------------|
| `native` | Local simulator (default) |
| `qiskit` | IBM Qiskit |
| `cirq` | Google Cirq |
| `gpu` | GPU-accelerated simulator |
| `cudaq` | NVIDIA CUDA-Q |

## Usage

```python
from quonic import qshow

qshow(backend='native')
qshow(backend='qiskit')
qshow(backend='gpu')
```

## Configuration

```python
from quonic.backends import set_backend

set_backend('qiskit')
set_backend('gpu', device='cuda:0')
```
