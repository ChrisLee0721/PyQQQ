"""Quantum integer / 量子整数

Quantum integer / 量子整数"""

from quonic import QInt, qshow

x = QInt(3, value=5)  # |5> = |101>
x += 3                # quantum addition: 5 + 3 ≡ 0 (mod 8)
qshow()
