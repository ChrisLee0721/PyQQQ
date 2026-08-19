"""Simon's algorithm: find the period of a 2-to-1 function.

Exponential speedup over classical; precursor to Shor's algorithm.
Output: the hidden period string s where f(x) = f(x XOR s).
"""

from quonic import qgate
from quonic.algorithms import simon
from quonic.gates import CX

# Hidden period s = "101" (decimal 5)
S = 5
N = 3

def simon_oracle(circuit, n):
    """Oracle for f(x) = f(x XOR s)."""
    for i in range(n):
        qgate(CX, i, i + n)
    for i in range(n):
        if (S >> i) & 1:
            qgate(CX, 0, i + n)

result = simon(N, simon_oracle, shots=200)
print(result.counts)
