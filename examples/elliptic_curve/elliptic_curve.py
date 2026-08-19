"""Elliptic curve quantum algorithm demo.

Quantum approach to elliptic curve discrete log.
Output: approximate solution.
"""

from quonic.algorithms import elliptic_curve_demo

result = elliptic_curve_demo()
print(result.counts)
