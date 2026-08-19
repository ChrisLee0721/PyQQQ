"""Amplitude amplification: boost probability of a target state.

Like Grover but with a custom state preparation oracle.
Output: amplified probability of the marked state.
"""

from quonic.algorithms import amplitude_amplification, mark_state

oracle_fn = mark_state("11")
result = amplitude_amplification(2, oracle_fn, shots=1024)
print(result.counts)
