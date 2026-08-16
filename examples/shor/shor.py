"""Shor's algorithm: factor 15 using quantum period finding.

15 = 3 x 5. With base a=7 (whose order is 4), one small-precision run
(t=6, shots=256) returns 3 or 5 in a few seconds.

Requires a sampling backend; use `pip install 'quonic[qiskit]'` for speed
(an auto-detected backend or the numpy-only native engine also works).
"""

from quonic.algorithms import shor

result = shor(15, a=7, t=6, shots=256)
print(result.value)                    # 3 or 5
print(result.metadata["period"])       # 4 (the order of 7 mod 15)
