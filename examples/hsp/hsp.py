"""Hidden Subgroup Problem demo.

General framework for Simon, Shor, and other HSP-based algorithms.
Output: subgroup generators.
"""

from quonic.algorithms import hsp_demo

result = hsp_demo()
print(result.counts)
