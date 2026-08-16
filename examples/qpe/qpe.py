"""Quantum phase estimation: estimate the phase of Rz(pi) on |1>.

Rz(theta)|1> = e^{i theta/2}|1>, so the eigenvalue phase is phi = theta/2.
With 3 precision qubits, j/2^3 ~ theta/(4 pi) = 1/4, so j = 2.
The rightmost 3 bits of the output are the phase estimate "010".
"""

import math

from quonic.algorithms import qpe

result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)  # dominated by "...010" (rightmost 3 bits -> j = 2)
