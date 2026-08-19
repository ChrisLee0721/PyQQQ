"""Color code error correction demo.

Demonstrates the color code — a topological code with transversal gates.
Output: corrected logical state.
"""

from quonic.algorithms import color_code_demo

result = color_code_demo(shots=100)
print(result.counts)
