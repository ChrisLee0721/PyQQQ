"""HHL algorithm: quantum linear system solver.

Solves Ax = b exponentially faster than classical for sparse matrices.
Output: quantum state proportional to x = A^{-1}b.
"""

from quonic.algorithms import hhl_demo

result = hhl_demo()
print(result.counts)
