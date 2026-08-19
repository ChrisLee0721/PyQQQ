"""Superdense coding: send 2 classical bits using 1 qubit.

Alice encodes 2 bits by manipulating her half of an entangled pair.
Output: decoded message.
"""

from quonic.algorithms import superdense_coding

for msg in ["00", "01", "10", "11"]:
    result = superdense_coding(message=msg, shots=100)
    # value is the decoded integer (0-3)
    decoded = f"{int(result.value):02b}"
    print(f"Sent: {msg}, Decoded: {decoded}")
