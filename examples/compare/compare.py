"""Comparator: qlt / qeq / qgt compare a register against a constant.

Each returns a flag qubit (1 = condition holds) entangled with the register,
leaving x unchanged. Here x is a uniform superposition |0..7>; measuring
everything shows the flag is exactly 1 on the x < 4 branch.
"""

from quonic import QInt, qlt, qshow

x = QInt(3)
x.h()            # uniform superposition |0>..|7>
flag = qlt(x, 4) # flag = 1 iff x < 4

qshow()
