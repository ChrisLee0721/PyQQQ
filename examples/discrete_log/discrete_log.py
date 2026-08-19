"""Discrete logarithm: find x such that a^x = b mod p.

Quantum algorithm for the discrete log problem.
Output: the discrete logarithm.
"""

from quonic.algorithms import discrete_log_demo

result = discrete_log_demo(a=2, b=8, p=11)
print(result.counts)
