# Zero Noise Extrapolation

ZNE is a noise mitigation technique.

## How it Works

1. Run circuit at multiple noise levels
2. Fit noise-expectation curve
3. Extrapolate to zero noise

## Usage

```python
from quonic.mitigation import zne

noise_levels = [0.0, 0.01, 0.02, 0.03]
expectation_values = [...]
mitigated = zne(noise_levels, expectation_values)
```
