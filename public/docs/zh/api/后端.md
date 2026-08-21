# Backends API

QuoNic supports 12+ backends. Use `get_backend()` to get a backend instance, then call `run()` to execute a circuit.

## Quick Start / 快速开始

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

# Auto-select best backend / 自动选择最佳后端
qshow()

# Specify backend / 指定后端
qshow(backend='qiskit')
qshow(backend='cirq')
qshow(backend='qulacs')
```

## get_backend(name, device=None)

Get a backend by name. Supports fuzzy matching for typos.

按名称获取后端。支持模糊匹配。

```python
from quonic.backends import get_backend

backend = get_backend("native")      # Native Python simulator
backend = get_backend("qiskit")      # Qiskit AerSimulator
backend = get_backend("qulacs")      # Qulacs C++ simulator
backend = get_backend("qi", device="Tuna-9")  # Quantum Inspire hardware
```

## available_backends()

List all available backends (checks if SDK is installed).

列出所有可用后端（检查 SDK 是否已安装）。

```python
from quonic.backends import available_backends

backends = available_backends()
print(backends)
# ['native', 'qiskit', 'cirq', 'qulacs', ...]
```

## Backend.run(circuit, shots=1024)

Execute a circuit and return results.

执行电路并返回结果。

```python
from quonic.backends import get_backend
from quonic.stack import current_circuit

backend = get_backend("native")
result = backend.run(current_circuit(), shots=4096)

print(result.counts)    # {'00': 2048, '11': 2048}
print(result.backend)   # 'native'
```

## Available Backends / 可用后端

| Backend | SDK | GPU | Noise | Classical Control |
|---------|-----|-----|-------|-------------------|
| `native` | numpy | ✗ | ✓ | ✓ |
| `qiskit` | Qiskit + Aer | ✓ | ✓ | ✓ |
| `cirq` | Cirq | ✗ | ✓ | ✓ |
| `pennylane` | PennyLane | ✗ | ✗ | ✗ |
| `qulacs` | Qulacs | ✓ | ✓ | ✓ |
| `tensorcircuit` | TensorCircuit | ✓ | ✓ | ✓ |
| `cudaq` | CUDA-Q | ✓ | ✓ | ✓ |
| `mindquantum` | MindQuantum | ✓ | ✓ | ✓ |
| `qpanda` | QPanda3 | ✓ | ✓ | ✓ |
| `cqlib` | CqLib | ✗ | ✗ | ✗ |
| `cupy` | CuPy | ✓ | ✓ | ✓ |
| `qi` | Quantum Inspire | ✗ | ✗ | ✗ |

## Smart Scheduling / 智能调度

QuoNic's scheduler auto-selects the best backend based on circuit features.

QuoNic 的调度器根据电路特征自动选择最佳后端。

```python
from quonic import qshow

# Scheduler picks: stabilizer for Clifford circuits
# 调度器选择：Clifford 电路用 stabilizer
qshow()  # Auto-selects based on gates, qubits, noise
```

## Hardware Backends / 硬件后端

### Quantum Inspire

```python
qshow(backend='qi', device='Tuna-9')    # 9-qubit
qshow(backend='qi', device='Tuna-17')   # 17-qubit
```

### AWS Braket

```python
qshow(backend='braket', device='arn:aws:braket:...')
```

### IBM Quantum

```python
qshow(backend='ibm', device='ibm_brisbane')
```

## Examples / 示例

### Compare backends / 对比后端

```python
from quonic import qgate, reset, qshow
from quonic.gates import H, CX

reset()
qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)

for b in ['native', 'qiskit', 'cirq']:
    print(f"\n--- {b} ---")
    qshow(backend=b)
```

### With noise / 加噪声

```python
from quonic import qshow

qshow(noise=0.05)  # 5% depolarizing noise
```
