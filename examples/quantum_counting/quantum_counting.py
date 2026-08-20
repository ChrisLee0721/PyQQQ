"""Quantum Counting / 量子计数

Quantum Counting / 量子计数"""

from quonic.algorithms import oracle, quantum_counting


@oracle(3)
def even(x):
    return x & 1 == 0


result = quantum_counting(even, 3, shots=2048)
print(result.value)  # ~ 4
