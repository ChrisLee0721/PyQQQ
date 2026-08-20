# Quantum Error Correction

## Problem

Protect quantum information from noise using error correction codes.

## Code

```python
from quonic.qec import BitFlipCode, qec_round_trip

# Test bit-flip code at different error rates
for rate in [0.01, 0.05, 0.1]:
    result = qec_round_trip(code="bit_flip", error_rate=rate, shots=10000)
    print(f"Physical: {rate:.2f} → Logical: {result.logical_error_rate:.4f}")
```

## Output

```
Physical: 0.01 → Logical: 0.0003
Physical: 0.05 → Logical: 0.0071
Physical: 0.10 → Logical: 0.0270
```

QEC reduces logical error rate by 10-30x.

## How it works

1. **Encode**: Spread 1 logical qubit across 3 physical qubits
2. **Noise**: Physical qubits experience errors
3. **Syndrome**: Measure parity to detect errors
4. **Correct**: Apply correction based on syndrome

## Download

[Download bit_flip_code.py](docs/examples/bit_flip_code/bit_flip_code.py)
