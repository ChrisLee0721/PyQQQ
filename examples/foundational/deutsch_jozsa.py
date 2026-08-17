"""Deutsch-Jozsa algorithm example.

Determines whether a Boolean function is constant or balanced in a single query.
"""

from quonic.algorithms import deutsch_jozsa
from quonic.ir import GateOperation


# Constant oracle: f(x) = 0 for all x
def constant_oracle(circuit, n):
    pass


# Balanced oracle: f(x) = x_0
def balanced_oracle(circuit, n):
    circuit.add(GateOperation("cx", (0, n)))


print("=== Deutsch-Jozsa Algorithm ===\n")

result_const = deutsch_jozsa(3, constant_oracle, shots=100)
print(f"Constant oracle: is_balanced = {result_const.metadata['is_balanced']}")

result_bal = deutsch_jozsa(3, balanced_oracle, shots=100)
print(f"Balanced oracle: is_balanced = {result_bal.metadata['is_balanced']}")
