"""Bit-flip error correction example.

Demonstrates the simplest quantum error correction code.
"""

from quonic.algorithms import bit_flip_code

print("=== Bit-flip Error Correction ===\n")

for error_qubit in [0, 1, 2]:
    result = bit_flip_code(error_qubit=error_qubit, shots=100)
    print(f"Error on qubit {error_qubit}: counts = {result.counts}")
