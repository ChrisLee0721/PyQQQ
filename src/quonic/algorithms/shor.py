"""Shor 算法：量子周期查找 + 连分数分解大整数。

对奇数合数 N（非素数幂）找到一个非平凡因子。

原理：
    1. 随机取 a 与 N 互素，其阶 r 满足 a^r ≡ 1 (mod N)。
    2. 量子周期查找：用 QPE 估计模乘算子 U_a |y> = |a·y mod N> 的本征相位 s/r。
    3. 连分数从相位 j/2^t 反解出 r。
    4. 若 r 为偶数且 a^{r/2} ≠ -1 (mod N)，则 gcd(a^{r/2} ± 1, N) 给出因子。

示例：
    from quonic.algorithms import shor

    result = shor(15)          # 返回 3 或 5
    print(result.value)
"""

import math
import random

from ..backends import get_backend
from ..ir import Circuit, GateOperation
from ..qft import add_iqft, add_qft
from ..result import Result

# ---------------------------------------------------------------------------
# 基础量子门
# ---------------------------------------------------------------------------

def _crz(circuit, c, t, phi):
    # 受控 Rz(phi)：Rz(phi/2); CX; Rz(-phi/2); CX
    circuit.add(GateOperation("rz", (t,), (phi / 2,)))
    circuit.add(GateOperation("cx", (c, t)))
    circuit.add(GateOperation("rz", (t,), (-phi / 2,)))
    circuit.add(GateOperation("cx", (c, t)))


def _toffoli(circuit, c1, c2, t):
    circuit.add(GateOperation("ccx", (c1, c2, t)))


def _cswap(circuit, control, a, b):
    # Fredkin 门：受控交换（3 个 Toffoli）
    _toffoli(circuit, control, a, b)
    _toffoli(circuit, control, b, a)
    _toffoli(circuit, control, a, b)


# ---------------------------------------------------------------------------
# QFT 加法（Draper 加法）
# ---------------------------------------------------------------------------

def _add_const(circuit, qubits, k):
    """|x> -> |x + k mod 2^m>，m = len(qubits)。"""
    m = len(qubits)
    add_qft(circuit, qubits)
    for j in range(m):
        circuit.add(GateOperation("rz", (qubits[j],), (2 * math.pi * k / 2 ** (j + 1),)))
    add_iqft(circuit, qubits)


def _cadd_const(circuit, qubits, k, control):
    """受控加法：control=1 时 |x> -> |x + k mod 2^m>。control 不在 qubits 中。"""
    m = len(qubits)
    add_qft(circuit, qubits)
    for j in range(m):
        _crz(circuit, control, qubits[j], 2 * math.pi * k / 2 ** (j + 1))
    add_iqft(circuit, qubits)


# ---------------------------------------------------------------------------
# 模运算
# ---------------------------------------------------------------------------

def _modinv(a, m):
    """模逆元 a^{-1} mod m（a 与 m 互素），用扩展欧几里得。"""
    a %= m
    if math.gcd(a, m) != 1:
        return None
    t, newt = 0, 1
    r, newr = m, a
    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    if t < 0:
        t += m
    return t


def cadd_mod(circuit, qubits, flag, b, N, control):
    """受控就地模加：control=1 时 |x> -> |(x + b) mod N>，flag 回到 |0>。

    qubits 长度为 n+1（n = N 的位宽），x、b ∈ [0, N)。
    flag 是一个额外的辅助比特（初末均为 |0>），记录「x + b < N」的借位标志。
    """
    n = len(qubits) - 1
    M = 2 ** (n + 1)
    _cadd_const(circuit, qubits, b, control)      # x -> x + b
    _cadd_const(circuit, qubits, M - N, control)  # x + b -> x + b - N
    circuit.add(GateOperation("cx", (qubits[n], flag)))  # flag = 下溢标志
    _cadd_const(circuit, qubits, N, flag)         # 若下溢，加回 N
    # 反演 flag（用关系 flag = 「(x+b) mod N >= b」）：
    _cadd_const(circuit, qubits, M - b, control)  # x -> x - b
    circuit.add(GateOperation("cx", (qubits[n], flag)))
    circuit.add(GateOperation("cx", (control, flag)))
    _cadd_const(circuit, qubits, b, control)      # 恢复 x


def _cmul_mod(circuit, q, reg, c, N, scratch, anc, flag):
    """受控就地模乘：q=1 时 |reg> -> |c·reg mod N>，scratch/anc/flag 均回到 |0>。

    reg、scratch 均为 n+1 个量子比特；anc 是 Toffoli 辅助比特，flag 是模加标志。
    """
    n = len(reg) - 1
    cinv = _modinv(c, N)
    # 1) scratch = c·reg mod N
    for i in range(n):
        a_i = (2 ** i * c) % N
        _toffoli(circuit, q, reg[i], anc)
        cadd_mod(circuit, scratch, flag, a_i, N, anc)
        _toffoli(circuit, q, reg[i], anc)
    # 2) 受控交换 reg <-> scratch
    for i in range(n + 1):
        _cswap(circuit, q, reg[i], scratch[i])
    # 3) scratch -= c^{-1}·reg（清零 scratch）
    for i in range(n):
        b_i = (N - (2 ** i * cinv) % N) % N
        _toffoli(circuit, q, reg[i], anc)
        cadd_mod(circuit, scratch, flag, b_i, N, anc)
        _toffoli(circuit, q, reg[i], anc)


def _mod_exp(circuit, exponent, reg, a, N, scratch, anc, flag):
    """|reg> -> |a^x mod N>，x 为 exponent 寄存器（LSB 在 exponent[0]）。

    与 qpe.py 一致的无 swap IQFT 约定：第 j 个相位比特控制 U^{2^{t-1-j}}。
    """
    t = len(exponent)
    for j in range(t):
        c = pow(a, 2 ** (t - 1 - j), N)
        _cmul_mod(circuit, exponent[j], reg, c, N, scratch, anc, flag)


# ---------------------------------------------------------------------------
# 经典部分：连分数、因子提取
# ---------------------------------------------------------------------------

def _convergents(x, max_q):
    """生成实数 x 的连分数渐近分数 p/q（q <= max_q）。"""
    if x <= 0:
        return
    p0, p1 = 0, 1
    q0, q1 = 1, 0
    r = x
    for _ in range(1000):
        a = int(math.floor(r + 1e-12))
        p = a * p1 + p0
        q = a * q1 + q0
        if q > max_q:
            return
        yield (p, q)
        p0, p1 = p1, p
        q0, q1 = q1, q
        frac = r - a
        if abs(frac) < 1e-12:
            return
        r = 1.0 / frac


def _period_from_phase(j, t, a, N):
    """从相位 j/2^t 用连分数反解 a 的阶 r。"""
    phi = j / (2 ** t)
    if phi == 0:
        return None
    for _, q in _convergents(phi, N):
        if q and pow(a, q, N) == 1:
            return q
    return None


def _factor_from_period(a, r, N):
    """由阶 r 提取因子；r 为奇数或 a^{r/2}≡-1 时返回 None。"""
    if r is None or r % 2 != 0:
        return None
    x = pow(a, r // 2, N)
    if x == N - 1:
        return None
    for cand in (math.gcd(x - 1, N), math.gcd(x + 1, N)):
        if 1 < cand < N:
            return cand
    return None


def _perfect_power_factor(N):
    """若 N 是完全幂 b^k，返回 b，否则 None。"""
    for b in range(2, N.bit_length() + 1):
        root = int(round(N ** (1.0 / b)))
        for r in (root - 1, root, root + 1):
            if r >= 2 and r ** b == N:
                return r
    return None


def _run_once(N, a, t, backend, shots):
    """运行一次量子周期查找，返回 (factor, j, r, exp_counts)。"""
    n = (N - 1).bit_length()
    exponent = list(range(t))
    base = t
    reg = list(range(base, base + n + 1))
    base += n + 1
    scratch = list(range(base, base + n + 1))
    base += n + 1
    anc = base
    flag = base + 1

    circuit = Circuit()
    circuit.add(GateOperation("x", (reg[0],)))  # reg = |1>
    for q in exponent:
        circuit.add(GateOperation("h", (q,)))
    _mod_exp(circuit, exponent, reg, a, N, scratch, anc, flag)
    add_iqft(circuit, exponent)

    result = get_backend(backend).run(circuit, shots=shots)

    # 只关心指数寄存器（最右 t 位），对其它比特求和
    exp_counts = {}
    for bitstring, count in result.counts.items():
        e = bitstring[-t:]
        exp_counts[e] = exp_counts.get(e, 0) + count

    for e in sorted(exp_counts, key=exp_counts.get, reverse=True):
        j = int(e, 2)
        r = _period_from_phase(j, t, a, N)
        factor = _factor_from_period(a, r, N)
        if factor is not None:
            return factor, j, r, exp_counts
    return None, None, None, exp_counts


def shor(N, a=None, t=None, backend="auto", shots=1024, attempts=8):
    """分解整数 N（奇数合数且非素数幂），返回一个非平凡因子。

    参数：
        N: 待分解整数。
        a: 随机基（默认随机选取）。
        t: 周期查找的精度比特数，默认 2·位宽。
        backend / shots: 采样参数。
        attempts: 失败重试次数。

    返回：Result（kind="value"），result.value 为 N 的一个非平凡因子。
    """
    N = int(N)
    if N < 2:
        raise ValueError(f"N 必须 >= 2，收到 {N}")

    if N % 2 == 0:
        return Result.from_value(2, factor_of=N, method="even")

    pp = _perfect_power_factor(N)
    if pp is not None:
        return Result.from_value(pp, factor_of=N, method="perfect_power")

    if t is None:
        t = 2 * (N - 1).bit_length()

    fixed_a = a is not None
    for _ in range(attempts):
        x = a if fixed_a else random.randint(2, N - 1)
        g = math.gcd(x, N)
        if 1 < g < N:
            return Result.from_value(g, factor_of=N, method="gcd", a=x)

        factor, j, r, counts = _run_once(N, x, t, backend, shots)
        if factor is not None:
            return Result.from_value(
                factor, factor_of=N, a=x, period=r, phase_j=j, counts=counts
            )
        if fixed_a:
            break

    raise RuntimeError(
        f"Shor 算法未能找到 {N} 的因子；请增加 shots / attempts，或更换 N"
    )
