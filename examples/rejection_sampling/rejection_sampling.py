"""Quantum rejection sampling demo.

Quantum-enhanced rejection sampling from a target distribution.
Output: samples from the target distribution.
"""

from quonic.algorithms import rejection_sampling_demo

result = rejection_sampling_demo(n_samples=100)
print(result.counts)
