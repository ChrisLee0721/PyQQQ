"""Quantum Topological Data Analysis demo.

Quantum algorithm for persistent homology.
Output: topological features.
"""

from quonic.algorithms import qtda_demo

result = qtda_demo()
print(result.counts)
