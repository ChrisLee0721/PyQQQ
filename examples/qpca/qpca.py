"""Quantum PCA (Principal Component Analysis) demo.

Exponentially faster PCA for density matrices.
Output: principal eigenvalues.
"""

from quonic.algorithms import qpca_demo

result = qpca_demo()
print(result.counts)
