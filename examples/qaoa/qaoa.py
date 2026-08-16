"""QAOA: solve MaxCut on a triangle graph (3 vertices, 3 edges).

Max cut = 2. Requires scipy: pip install 'quonic[algorithms]'.
"""

from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)
print(result.value)  # ≈ 2.0
