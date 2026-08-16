"""Quantum counting: estimate how many states satisfy a predicate.

Among 3 qubits (N = 8) there are 4 even numbers (x & 1 == 0), so the
estimate should be close to 4.
"""

from quonic.algorithms import oracle, quantum_counting


@oracle(3)
def even(x):
    return x & 1 == 0


result = quantum_counting(even, 3, shots=2048)
print(result.value)  # ~ 4
