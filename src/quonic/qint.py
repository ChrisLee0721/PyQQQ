"""QInt —— 量子整数寄存器。

一个 QInt 占据当前电路中的连续 n_bits 个量子比特，支持经典加载、
均匀叠加与量子加法（QFT 加法），最后用 qshow() 测量。

示例：
    from quonic import QInt, qshow

    x = QInt(3, value=5)   # |5> = |101>
    x.h()                  # 均匀叠加到 |0>..|7>
    x += 3                 # 每个分量加 3（模 8）
    qshow()                # 测量并显示
"""

import math

from .gates import H, Rz, X
from .qft import add_iqft, add_qft
from .qgate import qgate
from .qif import controlled
from .stack import current_circuit


class QInt:
    """量子整数寄存器。

    参数：
        n_bits: 位宽。
        value: 初始经典值（None 表示 |0>，等价于 value=0）。
    """

    def __init__(self, n_bits, value=None):
        if not isinstance(n_bits, int) or n_bits < 1:
            raise ValueError(f"n_bits 必须是正整数，收到 {n_bits!r}")
        self.n_bits = n_bits
        base = current_circuit().num_qubits
        current_circuit().allocate(base + n_bits)
        self.qubits = tuple(range(base, base + n_bits))
        if value is not None:
            self.load(value)

    def load(self, value):
        """经典加载：把寄存器置为 |value>。"""
        value = int(value)
        if not 0 <= value < 2 ** self.n_bits:
            raise ValueError(
                f"value 超出 {self.n_bits} 位整数范围 [0, {2 ** self.n_bits})，收到 {value}"
            )
        for j in range(self.n_bits):
            if (value >> j) & 1:
                qgate(X, self.qubits[j])
        return self

    def h(self):
        """对每一位施加 Hadamard，得到 2**n_bits 个基态的均匀叠加。"""
        for q in self.qubits:
            qgate(H, q)
        return self

    def superpose(self):
        """h() 的别名：均匀叠加。"""
        return self.h()

    def add(self, k):
        """量子加法：|a> -> |a + k mod 2**n_bits>（k 为经典常数）。

        用 QFT 加法（Draper 加法）实现，k 可为任意整数（自动取模）。
        """
        k = int(k) % 2 ** self.n_bits
        add_qft(current_circuit(), self.qubits)
        for j in range(self.n_bits):
            qgate(Rz(2 * math.pi * k / 2 ** (j + 1)), self.qubits[j])
        add_iqft(current_circuit(), self.qubits)
        return self

    def __iadd__(self, k):
        return self.add(k)

    def sub(self, k):
        """量子减法：|a> -> |a - k mod 2**n_bits>（等价于加 -k）。"""
        return self.add(-int(k))

    def __isub__(self, k):
        return self.sub(k)

    def __int__(self):
        raise TypeError(
            "量子整数处于叠加态，无法直接转成 int；请先 qshow() 测量后读取结果"
        )

    def lt(self, k):
        """比较：返回一个标志比特，x < k 时为 1（x 保持不变）。"""
        from .compare import qlt

        return qlt(self, k)

    def eq(self, k):
        """比较：返回一个标志比特，x == k 时为 1（x 保持不变）。"""
        from .compare import qeq

        return qeq(self, k)

    def gt(self, k):
        """比较：返回一个标志比特，x > k 时为 1（x 保持不变）。"""
        from .compare import qgt

        return qgt(self, k)

    def mul(self, k):
        """乘法：返回一个新 QInt，值为 |x * k mod 2**n_bits>（x 保持不变）。"""
        return mul(self, k)

    def __repr__(self):
        return f"QInt({self.n_bits} 位, qubits={list(self.qubits)})"


def _add_quantum(circuit, a_qubits, b_qubits, shift=0):
    """量子-量子加法：|a>|b> -> |a>|b + (a << shift) mod 2**n>（Draper 加法）。

    与 _add_const（加经典常数）不同，这里把 a 的每一位当成受控相位条件，
    用 controlled(Rz) 实现受控旋转。shift 用于「移位加」乘法。
    """
    n = len(b_qubits)
    add_qft(circuit, b_qubits)
    for j in range(n):
        for i in range(n):
            p = i + shift
            if p <= j:
                theta = 2 * math.pi / (2 ** (j - p + 1))
                controlled(Rz(theta), a_qubits[i], b_qubits[j])
    add_iqft(circuit, b_qubits)


def mul(x, k):
    """量子乘法：返回新 QInt，值为 |x * k mod 2**n>，x 保持不变。

    用「移位加 + 量子-量子 Draper 加法」实现：对 k 的每个置位 b，把 x << b
    累加到零初始化的结果寄存器。结果存进干净寄存器而非就地覆盖，因此对任意
    k（含偶数）都成立（偶数 k 就地乘法不可逆）。

    例：
        a = QInt(2, value=1)     # |1>
        p = mul(a, 3)            # p = |3>
        qshow()                  # 读 a、p
    """
    n = x.n_bits
    k = int(k) % (2 ** n)
    result = QInt(n)
    for b in range(n):
        if (k >> b) & 1:
            _add_quantum(current_circuit(), x.qubits, result.qubits, shift=b)
    return result
