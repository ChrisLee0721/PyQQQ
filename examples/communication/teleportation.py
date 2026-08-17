"""Quantum Teleportation example.

Teleports a quantum state from Alice to Bob using entanglement.
"""

from quonic.algorithms import teleportation
import math

print("=== Quantum Teleportation ===\n")

# Teleport |0> (theta=0)
result0 = teleportation(theta=0, shots=1000)
print(f"Teleport |0>: {result0.counts}")

# Teleport |1> (theta=pi)
result1 = teleportation(theta=math.pi, shots=1000)
print(f"Teleport |1>: {result1.counts}")

# Teleport |+> (theta=pi/2)
result_plus = teleportation(theta=math.pi / 2, shots=1000)
print(f"Teleport |+>: {result_plus.counts}")
