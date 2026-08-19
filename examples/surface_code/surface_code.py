"""Surface code error correction demo.

The leading candidate for fault-tolerant quantum computation.
Output: logical qubit with error correction.
"""

from quonic.algorithms import surface_code_demo

result = surface_code_demo(distance=3, shots=100)
print(result.counts)
