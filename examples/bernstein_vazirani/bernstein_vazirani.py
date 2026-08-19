"""Bernstein-Vazirani: find the hidden bitstring s in f(x) = s·x mod 2.

One query suffices — the algorithm reads s directly from the output.
Output: all shots give the hidden string.
"""

from quonic import qgate
from quonic.algorithms import bernstein_vazirani
from quonic.gates import CZ

# Hidden string s = "1010" (decimal 10)
S = 10
N = 4

def bv_oracle(circuit, n):
    """Phase oracle for f(x) = s·x mod 2."""
    for i in range(n):
        if (S >> i) & 1:
            qgate(CZ, i, n)

result = bernstein_vazirani(N, bv_oracle, shots=1024)
print(result.counts)
