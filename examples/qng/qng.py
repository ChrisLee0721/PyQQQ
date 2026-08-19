"""Quantum Natural Gradient demo.

Uses the quantum Fisher information matrix for better optimization.
Output: optimized parameters.
"""

from quonic.algorithms import qng_demo

result = qng_demo(n_params=2, maxiter=50)
print(f"Final loss: {result.value}")
