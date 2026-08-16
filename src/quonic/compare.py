"""比较器：qlt / qeq / qgt —— 用量子寄存器与经典常数比较，结果存入一个标志位。

三种比较都返回一个新的 ancilla 比特（标志位），比较前后量子寄存器 x 保持不变：

    from quonic import QInt, qlt, qeq, qgt, qshow

    x = QInt(3); x.h()          # |0..7> 均匀叠加
    lt = qlt(x, 4)              # lt 标志位，x < 4 时为 1
    qshow()                     # 测量所有比特，读 lt 标志

实现要点：
- qeq 精确：x - k mod 2^n 是否为零（X 全翻转后用多控制 Z 检测全零）。
- qlt 用 n+1 位补码：x - k 的符号位（第 n 位）指示 x < k；符号位来自一个
  干净的 sign ancilla，比较后 uncompute 还原 x 与 ancilla。
- qgt = NOT qlt(k+1)（x > k ⟺ x >= k+1 ⟺ 非 x < k+1）。

全部基于 QFT 加法（与 QInt.add 同一套 Draper 加法）。numpy 只在运行时经
add_qft / 门矩阵间接使用，保证 `import quonic` 零开销。
"""

import math

from .gates import CX, H, Rz, X
from .ir import GateOperation
from .qft import add_iqft, add_qft
from .qgate import qgate
from .stack import current_circuit


def _alloc_ancilla():
    """分配一个干净的 |0> ancilla 比特，返回其下标。"""
    circ = current_circuit()
    q = circ.num_qubits
    circ.allocate(q + 1)
    return q


def _add_const(circuit, qubits, k):
    """QFT 加法：|a> -> |a + k mod 2**len(qubits)>，k 可为负。"""
    n = len(qubits)
    k = int(k) % (2 ** n)
    add_qft(circuit, qubits)
    for j in range(n):
        qgate(Rz(2 * math.pi * k / 2 ** (j + 1)), qubits[j])
    add_iqft(circuit, qubits)


def _check_qint(x):
    if not (hasattr(x, "n_bits") and hasattr(x, "qubits")):
        raise TypeError(f"比较器需要 QInt 寄存器，收到 {type(x).__name__}")


def qeq(x, k):
    """flag == 1 iff x == k（精确，x 保持不变）。返回标志比特下标。"""
    _check_qint(x)
    flag = _alloc_ancilla()
    _add_const(current_circuit(), x.qubits, -int(k))
    for q in x.qubits:
        qgate(X, q)
    qgate(H, flag)
    current_circuit().add(GateOperation("mcz", x.qubits + (flag,)))
    qgate(H, flag)
    for q in x.qubits:
        qgate(X, q)
    _add_const(current_circuit(), x.qubits, int(k))
    return flag


def qlt(x, k):
    """flag == 1 iff x < k（x 保持不变）。返回标志比特下标。"""
    _check_qint(x)
    sign = _alloc_ancilla()
    flag = _alloc_ancilla()
    qubits = x.qubits + (sign,)
    _add_const(current_circuit(), qubits, -int(k))
    qgate(CX, sign, flag)
    _add_const(current_circuit(), qubits, int(k))
    return flag


def qgt(x, k):
    """flag == 1 iff x > k（x 保持不变）。返回标志比特下标。"""
    flag = qlt(x, int(k) + 1)
    qgate(X, flag)
    return flag


__all__ = ["qlt", "qeq", "qgt"]
