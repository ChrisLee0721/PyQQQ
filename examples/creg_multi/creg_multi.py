"""Multi-bit classical register: creg(width=2) + cwhile + cif + groverize.

A 2-bit register stores integer values 0..3. The RUS loop prepares two qubits
with H each and measures both into the register, retrying until reg == 2 ("10").
groverize() compiles the retry loop into a static circuit, amplifying the
success probability from 1/4 to 1. A multi-bit cif then branches on the full
register value.
"""

from quonic import cif, creg, cwhile, qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, I, X
from quonic.stack import current_circuit

# --- 多比特 cwhile + groverize ---
# 两比特各自 H，直到寄存器值 == 2 ("10")；单次成功概率 p = 1/4
reg = creg("reg", width=2)
with cwhile(reg, until=2) as loop:
    qgate(H, 0)
    qgate(H, 1)
    reg.measure(0, bit=0)
    reg.measure(1, bit=1)

static = loop.groverize()  # 成功态 (reg == 2) 从 1/4 放大到 1
result = get_backend("native").run(static, shots=1024)
# 4 比特输出：ancilla 寄存器(左 2 位 "10") + 数据(q1 q0 = "10")
print("groverize 后:", result.counts)  # {'1010': 1024}

# --- 多比特 cif ---
reset()
qgate(X, 1)                       # q1 = 1
reg2 = creg("reg2", width=2)
reg2.measure(0, bit=0)            # bit0 = 0
reg2.measure(1, bit=1)            # bit1 = 1 -> 寄存器值 2
cif(reg2, 2).then(X, 2).else_(I, 2)  # reg2 == 2 -> 翻转 q2
result2 = get_backend("native").run(current_circuit(), shots=256)
print("cif 后:      ", result2.counts)  # {'110': 256}
