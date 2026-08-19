"""Fault-tolerant gate demo.

Demonstrates gates implemented with error detection/correction.
Output: logically encoded state.
"""

from quonic.algorithms import ft_gate_demo

result = ft_gate_demo(shots=100)
print(result.counts)
