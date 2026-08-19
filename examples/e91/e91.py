"""E91 quantum key distribution protocol.

Uses entangled pairs and Bell inequality tests for secure key exchange.
Output: shared secret key bits.
"""

from quonic.algorithms import e91

result = e91(n_rounds=100)
print(f"Result: {result.value}")
