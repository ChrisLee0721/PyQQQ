"""Shor's 9-qubit code: the first quantum error correction code.

Corrects arbitrary single-qubit errors.
Output: corrected logical state.
"""

from quonic.algorithms import shor_code

result = shor_code(error_qubit=0, shots=100)
print(result.counts)
