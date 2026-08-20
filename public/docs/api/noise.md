# Noise API

Noise models for simulating quantum hardware imperfections.

模拟量子硬件缺陷的噪声模型。

## Quick Start / 快速开始

```python
from quonic import qshow

# Simple: add depolarizing noise
# 简单：添加去极化噪声
qshow(noise=0.05)  # 5% noise level
```

## NoiseModel — Custom Noise / 自定义噪声

```python
from quonic.noise import NoiseModel

model = NoiseModel()

# Add depolarizing noise to specific gates
# 对特定门添加去极化噪声
model.add_depolarizing("h", p=0.01)    # 1% on Hadamard
model.add_depolarizing("cx", p=0.02)   # 2% on CNOT

# Add readout (measurement) noise
# 添加读出噪声
model.add_readout_error(p0given1=0.03, p1given0=0.02)

# Use the model
qshow(noise=model)
```

## depolarizing(p) — Depolarizing Channel / 去极化通道

Applies random Pauli errors with probability p.

以概率 p 施加随机 Pauli 错误。

```python
from quonic.noise import depolarizing

# Single-qubit depolarizing
noise = depolarizing(p=0.05)
# ρ → (1-p)ρ + p/3(XρX + YρY + ZρZ)

# Two-qubit depolarizing
noise = depolarizing(p=0.05, n_qubits=2)
```

## Noise Types / 噪声类型

| Type | Description | Effect |
|------|-------------|--------|
| Depolarizing | Random Pauli errors | Mixed state |
| Bit-flip | X errors only | \|0⟩↔\|1⟩ |
| Phase-flip | Z errors only | Phase errors |
| Amplitude damping | Energy relaxation | \|1⟩→\|0⟩ |
| Readout error | Measurement errors | Wrong counts |

## Examples / 示例

### Compare noise levels / 对比噪声水平

```python
from quonic import qgate, qshow, reset
from quonic.gates import CX, H

reset()
qgate(H, 0)
qgate(CX, 0, 1)

for noise in [0, 0.01, 0.05, 0.1]:
    print(f"\n--- noise={noise} ---")
    qshow(noise=noise)
```

### Custom noise model / 自定义噪声模型

```python
from quonic.noise import NoiseModel
from quonic import qshow

model = NoiseModel()
model.add_depolarizing("h", p=0.02)
model.add_depolarizing("cx", p=0.05)
model.add_readout_error(p0given1=0.05, p1given0=0.03)

qshow(noise=model)
```

### Noise with ZNE / 噪声 + ZNE

```python
from quonic import zne

# Zero-noise extrapolation
result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)  # Closer to noiseless
```
