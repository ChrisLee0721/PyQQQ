"""Amplitude estimation: estimate the amplitude of a marked state.

Uses precision qubits to estimate the success probability of an oracle.
Output: estimated amplitude close to the true value.
"""

from quonic.algorithms import amplitude_estimation_demo

result = amplitude_estimation_demo(n_qubits=2, n_precision=3, shots=1024)
print(result.counts)
