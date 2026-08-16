"""QInt: load a 3-bit register as |5>, then quantum-add 3 (mod 8).

5 + 3 ≡ 0 (mod 8), so the output is almost surely |000>.
"""

from quonic import QInt, qshow

x = QInt(3, value=5)  # |5> = |101>
x += 3                # quantum addition: 5 + 3 ≡ 0 (mod 8)
qshow()
