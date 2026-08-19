"""Quantum Boltzmann Machine demo.

Quantum version of Boltzmann machine for generative modeling.
Output: learned distribution.
"""

from quonic.algorithms import qbm_demo

result = qbm_demo(temperature=1.0)
print(result.counts)
