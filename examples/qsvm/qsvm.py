"""Quantum Support Vector Machine demo.

Uses quantum kernel for classification.
Output: classification accuracy.
"""

from quonic.algorithms import qsvm_demo

result = qsvm_demo()
print(result.counts)
