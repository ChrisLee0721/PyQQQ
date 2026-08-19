"""Steane code: [[7,1,3]] CSS code.

Corrects any single-qubit error using 7 physical qubits.
Output: corrected logical state.
"""

from quonic.algorithms import steane_code

result = steane_code(error_qubit=0, shots=100)
print(result.counts)
