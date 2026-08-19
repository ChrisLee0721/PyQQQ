"""Variational Quantum Regressor.

Quantum model for regression tasks.
Output: predicted values.
"""

from quonic.algorithms import vqr

X = [[0.0], [0.5], [1.0], [1.5]]
y = [0.0, 0.479, 0.841, 0.997]
result = vqr(X, y, n_params=2, maxiter=100)
print(f"Final loss: {result.value}")
