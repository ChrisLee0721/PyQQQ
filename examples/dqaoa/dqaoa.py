"""Dynamic QAOA (DQAOA): adaptive layer QAOA variant.

Adds layers dynamically until convergence.
Output: approximate optimal solution.
"""

from quonic.algorithms import dqaoa_demo

result = dqaoa_demo()
print(result.counts)
