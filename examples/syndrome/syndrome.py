"""Syndrome measurement demo.

Extracts error syndromes without disturbing the encoded state.
Output: syndrome bits indicating error location.
"""

from quonic.algorithms import syndrome_demo

result = syndrome_demo(n_data=3, shots=100)
print(result.counts)
