"""QAOA for MaxCut: find the maximum cut of a graph.

Partitions vertices to maximize edges between partitions.
Output: approximate max cut value.
"""

from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, p=1, maxiter=100)
print(f"Max cut: {result.value}")
