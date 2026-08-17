"""cwhile → groverize: compile a repeat-until-success loop into a static circuit.

Ry(2π/3) then measure q0 succeeds (q0 == 0) with probability p = 1/4.
groverize turns the "retry until success" loop into a fixed-depth static circuit
(deferred measurement + amplitude amplification), so it runs on any backend —
including real hardware, which has no mid-circuit measurement feedback.
"""

import math

from quonic import creg, cwhile, qgate
from quonic.backends import get_backend
from quonic.gates import Ry

flag = creg("flag")
with cwhile(flag, until=0) as loop:
    qgate(Ry(2 * math.pi / 3), 0)   # 单次成功概率 p = 1/4
    flag.measure(0)

static = loop.groverize()   # 编译成静态 Grover 电路（success_prob 自动推断）

# 静态电路无中段反馈，任意后端都能跑；成功态 |00> 的概率从 1/4 放大到 1
print(get_backend("qiskit").run(static, shots=1024).counts)  # {'00': 1024}

# 真机（Quantum Inspire，需登录排队）同样能跑：
# print(get_backend("qi", device="tuna9").run(static, shots=1024).counts)
