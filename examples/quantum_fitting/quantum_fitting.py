"""Quantum curve fitting demo.

Quantum version of regression/curve fitting.
Output: fitted parameters.
"""

from quonic.algorithms import quantum_fitting_demo

result = quantum_fitting_demo()
print(result.counts)
