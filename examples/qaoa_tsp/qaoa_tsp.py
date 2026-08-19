"""QAOA for the Traveling Salesman Problem.

Finds the shortest route visiting all cities exactly once.
Output: approximate tour cost.
"""

from quonic.algorithms import qaoa_tsp

distances = {
    (0, 1): 1.0, (1, 0): 1.0,
    (1, 2): 2.0, (2, 1): 2.0,
    (0, 2): 1.5, (2, 0): 1.5,
}
result = qaoa_tsp(distances, 3, p=1, maxiter=100)
print(f"Tour cost: {result.value}")
