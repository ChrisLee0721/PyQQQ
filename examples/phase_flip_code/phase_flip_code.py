"""Phase flip error correction code.

Encodes logical qubit against phase errors using 3 physical qubits.
Output: corrected logical state.
"""

from quonic.algorithms import phase_flip_code

result = phase_flip_code(error_qubit=0, shots=100)
print(result.counts)
