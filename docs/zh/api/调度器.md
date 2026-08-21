# Scheduler API

Automatically picks the best backend and method for a circuit based on its features.

根据电路特征自动选择最佳后端和方法。

## Quick Start / 快速开始

```python
from quonic import qshow

# Scheduler auto-selects best backend
# 调度器自动选择最佳后端
qshow()  # Picks based on gates, qubits, noise
```

## schedule(circuit) — Full Scheduling / 完整调度

```python
from quonic.scheduler import schedule

rec = schedule(circuit)
print(rec.backend)  # e.g., "qiskit"
print(rec.method)   # e.g., "stabilizer"
print(rec.reason)   # Why this choice
```

## circuit_features(circuit) — Extract Features / 提取特征

```python
from quonic.scheduler import circuit_features

features = circuit_features(circuit)
print(features.gate_types)    # {"h": 5, "cx": 10}
print(features.n_qubits)      # 8
print(features.treewidth)      # 3
print(features.is_clifford)    # True
```

## recommend_method(features) — Method Selection / 方法选择

```python
from quonic.scheduler import recommend_method

rec = recommend_method(features)
# Returns: Recommendation(backend, method, reason)
```

### Decision logic / 决策逻辑

```
电路特征
  │
  ├─ Clifford? ──► stabilizer (polynomial)
  │
  ├─ Low treewidth? ──► matrix_product_state (linear)
  │
  └─ General ──► statevector (exponential but universal)
```

## recommend_backend_gpu(features) — GPU Selection / GPU 选择

```python
from quonic.scheduler import recommend_backend_gpu

backend = recommend_backend_gpu(features)
# Returns: "cupy", "qulacs", "cudaq", etc.
```

## Examples / 示例

### Compare scheduling decisions / 对比调度决策

```python
from quonic.scheduler import schedule, circuit_features
from quonic import qgate, reset
from quonic.gates import CX, H

# Clifford circuit → stabilizer
reset()
qgate(H, 0)
for i in range(7):
    qgate(CX, i, i + 1)
rec = schedule(current_circuit())
print(f"Clifford: {rec.method}")  # stabilizer

# Non-clifford → statevector
reset()
qgate(Ry(0.5), 0)
qgate(CX, 0, 1)
rec = schedule(current_circuit())
print(f"Non-clifford: {rec.method}")  # statevector
```
