"""Quantum clustering demo.

Quantum algorithm for unsupervised clustering.
Output: cluster assignments.
"""

from quonic.algorithms import quantum_clustering_demo

result = quantum_clustering_demo()
print(result.counts)
