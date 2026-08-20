"""Quantum teleportation / 量子隐形传态

Quantum teleportation / 量子隐形传态

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

import math

from quonic.algorithms import teleportation

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
