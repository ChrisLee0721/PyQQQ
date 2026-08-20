# Grover Search Tutorial

## Problem

Search an unsorted database of N items for a specific target. Classical: O(N) queries. Quantum: O(√N) queries.

## Code

```python
from quonic.algorithms import grover

# Search for |11> in 2-qubit space
result = grover("11", 2, shots=1024)
print(result.counts)
```

## Output

```
{'11': 1000, '00': 8, '01': 8, '10': 8}
```

Target state |11⟩ found with ~98% probability.

## How it works

1. **Superposition**: Apply H to all qubits → equal superposition
2. **Oracle**: Mark the target state (flip its phase)
3. **Diffusion**: Amplify the marked state's amplitude
4. **Repeat**: √N iterations for optimal success

## Real hardware

```python
# Run on Origin Quantum WK_C180
result = grover("11", 2, shots=1024, backend='qpanda', device='WK_C180')

# Run on AWS Braket
result = grover("11", 2, shots=1024, backend='braket', device='sv1')
```

## Download

[Download grover.py](docs/examples/grover/grover.py)
