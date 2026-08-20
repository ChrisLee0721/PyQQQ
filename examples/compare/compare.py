"""Compare backends / 比较后端

Compare backends / 比较后端"""

from quonic import QInt, qlt, qshow

x = QInt(3)
x.h()            # uniform superposition |0>..|7>
flag = qlt(x, 4) # flag = 1 iff x < 4

qshow()
