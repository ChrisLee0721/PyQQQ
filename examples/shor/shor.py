"""Shor's algorithm / Shor 算法

Shor's algorithm / Shor 算法"""

from quonic.algorithms import shor

result = shor(15, a=7, t=6, shots=256)
print(result.value)                    # 3 or 5
print(result.metadata["period"])       # 4 (the order of 7 mod 15)
