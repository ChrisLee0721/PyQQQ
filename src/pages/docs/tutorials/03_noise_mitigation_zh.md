# 03_noise_mitigation 中文版

参见 [英文版](03_noise_mitigation.md)


Real quantum hardware has noise. QuoNic provides two error mitigation techniques: ZNE and readout calibration.

## Adding Noise

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=0.05)  # 5% depolarizing noise
```

## ZNE (Zero-Noise Extrapolation)

ZNE amplifies the noise by folding the circuit, then extrapolates to zero noise:

```python
from quonic import zne

result = zne(
    circuit,
    noise=0.05,
    target="11",           # success metric: P(|11>)
    factors=(1, 3, 5),     # noise amplification factors
    extrapolation="exponential",  # or "linear"
)
print(f"Extrapolated: {result.extrapolated:.3f}")
print(f"Raw: {result.values[0]:.3f}")
```

## Readout Calibration

Readout errors flip measurement results. Calibration corrects them:

```python
from quonic import calibrate

# Build calibration matrix
cal = calibrate(n=2, backend="native", shots=4096, noise=NoiseModel(readout=0.05))

# Apply to measured counts
corrected = cal.apply(raw_counts, shots=4096)
```

## Stacking ZNE + Readout Calibration

For best results, combine both:

```python
cal = calibrate(n=2, backend="native", shots=4096, noise=NoiseModel(readout=0.05))
result = zne(
    circuit, noise=0.05, target="11",
    calibration=cal, extrapolation="exponential"
)
```

## Real Hardware Results (Tuna-17)

| Method | Single-bit (n=2) | Multi-bit (n=4) |
|--------|-----------------|-----------------|
| Raw | 0.936 | 0.706 |
| Readout calibration | 0.982 | 0.788 |
| ZNE exponential | 0.920 | 0.812 |
| Stacked | **0.963** | **0.869** |
