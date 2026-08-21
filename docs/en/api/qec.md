# Quantum Error Correction

QuoNic provides quantum error correction codes.

## Available Codes

- Bit flip code
- Phase flip code
- Shor code (9 qubits)
- Steane code (7 qubits)
- Surface code

## Usage

```python
from quonic.qec import bit_flip_code, surface_code

# Bit flip code
result = bit_flip_code(error_qubit=1)

# Surface code
result = surface_code(distance=3, error_rate=0.01)
```
