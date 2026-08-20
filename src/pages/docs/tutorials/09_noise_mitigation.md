# Noise Mitigation with ZNE

## Problem

Real quantum hardware has noise. ZNE (Zero-Noise Extrapolation) recovers the ideal result.

## Code

```python
from quonic import zne
from quonic.ir import Circuit, GateOperation

# Build a circuit
c = Circuit()
c.add(GateOperation("x", (0,)))
c.add(GateOperation("measure", (0,)))

# Apply ZNE
result = zne(c, noise=0.05, target="1", shots=4096, extrapolation="linear")
print(f"Raw:           {result.values[0]:.3f}")
print(f"ZNE linear:    {result.extrapolated:.3f}")
print(f"Ideal:         1.000")
```

## Output

```
Raw:           0.950
ZNE linear:    0.987
Ideal:         1.000
```

ZNE improves success rate from 95% to 98.7%.

## How it works

1. **Fold**: Amplify noise by repeating gates (λ=1,3,5)
2. **Measure**: Get success rate at each noise level
3. **Extrapolate**: Fit curve and extrapolate to λ=0 (zero noise)

## Download

[Download error_mitigation.py](docs/examples/error_mitigation/error_mitigation.py)
