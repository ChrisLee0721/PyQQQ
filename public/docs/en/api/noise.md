# Noise Models

QuoNic provides noise models for quantum simulation.

## Available Models

- Depolarizing noise
- Bit flip noise
- Phase flip noise
- Thermal noise

## Usage

```python
from quonic.noise import noise_model

model = noise_model(error_rate=0.01, noise_type='depolarizing')
qshow(noise=model)
```
