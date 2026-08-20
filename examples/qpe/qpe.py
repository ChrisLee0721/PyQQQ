"""Quantum Phase Estimation / 量子相位估计

Quantum Phase Estimation / 量子相位估计"""

import math

from quonic.algorithms import qpe

result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)  # dominated by "...010" (rightmost 3 bits -> j = 2)
