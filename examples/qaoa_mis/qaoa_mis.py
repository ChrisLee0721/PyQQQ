"""QAOA for Maximum Independent Set.

Finds the largest set of non-adjacent vertices.
Output: approximate MIS size.
"""

from quonic.algorithms import qaoa_mis

edges = [(0, 1), (1, 2)]
result = qaoa_mis(edges, 3, p=1, maxiter=100)
print(f"MIS size: {result.value}")
