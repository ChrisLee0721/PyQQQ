"""Classical while loop / 经典 while 循环

Classical while loop / 经典 while 循环"""

from quonic import creg, cwhile, qgate, qshow
from quonic.gates import H

flag = creg("flag")
with cwhile(flag, until=0):
    qgate(H, 0)
    flag.measure(0)

qshow(backend="native")  # cwhile 逐 shot 动态执行，仅 native 后端支持
