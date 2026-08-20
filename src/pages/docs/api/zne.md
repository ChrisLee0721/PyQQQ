# ZNE (Zero-Noise Extrapolation) API

Error mitigation by amplifying noise and extrapolating to zero noise.

通过放大噪声并外推到零噪声来缓解误差。

## Quick Start / 快速开始

```python
from quonic import zne

# Mitigate noise effects
# 缓解噪声效应
result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)  # Closer to noiseless result
print(result.raw_value)        # Noisy result
```

## zne(circuit, noise, extrapolation) — Full ZNE / 完整 ZNE

```python
from quonic import zne

result = zne(
    circuit,
    noise=0.05,                    # Base noise level
    scale_factors=[1, 3, 5],       # Noise scaling factors
    extrapolation="linear",        # "linear", "richardson", "exponential"
    backend="native",
)
```

### Parameters / 参数

| Parameter | Type | Description |
|-----------|------|-------------|
| `circuit` | Circuit | Circuit to mitigate |
| `noise` | float | Base noise level (0.0-1.0) |
| `scale_factors` | list | Noise scaling factors |
| `extrapolation` | str | Extrapolation method |
| `backend` | str | Backend to use |

### Extrapolation methods / 外推方法

| Method | Description | Best for |
|--------|-------------|----------|
| `linear` | Linear fit | Low noise |
| `richardson` | Richardson extrapolation | Medium noise |
| `exponential` | Exponential decay fit | High noise |

## fold(circuit, scale_factor) — Noise Folding / 噪声折叠

Amplify noise by folding the circuit: U → U·U†·U.

通过折叠电路放大噪声：U → U·U†·U。

```python
from quonic.zne import fold

# Scale noise by 3x
folded = fold(circuit, scale_factor=3)
```

## ZNEResult — Result Object / 结果对象

```python
result = zne(circuit, noise=0.05)

print(result.mitigated_value)   # Extrapolated noiseless value
print(result.raw_value)         # Noisy measurement
print(result.scale_factors)     # [1, 3, 5]
print(result.scaled_values)     # Values at each scale factor
print(result.extrapolation)     # Method used
```

## Examples / 示例

### Compare extrapolation methods / 对比外推方法

```python
from quonic import zne

for method in ["linear", "richardson", "exponential"]:
    result = zne(circuit, noise=0.05, extrapolation=method)
    print(f"{method}: {result.mitigated_value:.4f}")
```

### ZNE with different noise levels / 不同噪声水平的 ZNE

```python
from quonic import zne

for noise in [0.01, 0.05, 0.1]:
    result = zne(circuit, noise=noise)
    print(f"noise={noise}: raw={result.raw_value:.4f} → mitigated={result.mitigated_value:.4f}")
```

### Plot ZNE results / 绘制 ZNE 结果

```python
from quonic.viz import plot_zne

result = zne(circuit, noise=0.05)
plot_zne(result)  # Shows extrapolation curve
```
