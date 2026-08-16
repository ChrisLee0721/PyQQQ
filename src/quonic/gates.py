"""内置量子门。

门对象是主推 API（与 Qiskit/Cirq 风格一致）：
    from quonic.gates import H, X, CX
    qgate(H, 0)

qgate() 同时接受门对象或门名字符串（如 qgate("h", 0)）。
参数化门（Rx/Ry/Rz）是工厂函数，返回带参数的门对象：
    from quonic.gates import Rx
    qgate(Rx(0.5), 0)
"""

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class Gate:
    name: str
    num_qubits: int
    params: Tuple[float, ...] = field(default_factory=tuple)


H = Gate("h", 1)
X = Gate("x", 1)
Y = Gate("y", 1)
Z = Gate("z", 1)
I = Gate("i", 1)  # noqa: E741  # 恒等门，标准符号
CX = Gate("cx", 2)
CZ = Gate("cz", 2)
CCX = Gate("ccx", 3)
SWAP = Gate("swap", 2)
MEASURE = Gate("measure", 1)


def _angle(theta):
    try:
        return float(theta)
    except (TypeError, ValueError):
        raise TypeError(
            f"参数化门的旋转角必须是数字（弧度），收到 {theta!r}（{type(theta).__name__}）"
        ) from None


def Rx(theta: float) -> Gate:
    return Gate("rx", 1, (_angle(theta),))


def Ry(theta: float) -> Gate:
    return Gate("ry", 1, (_angle(theta),))


def Rz(theta: float) -> Gate:
    return Gate("rz", 1, (_angle(theta),))


_BY_NAME = {g.name: g for g in (H, X, Y, Z, I, CX, CZ, CCX, SWAP, MEASURE)}


def resolve(gate):
    """把门对象或门名字符串统一解析为 Gate 对象。"""
    if isinstance(gate, Gate):
        return gate
    if isinstance(gate, str):
        name = gate.strip().lower()
        if name in _BY_NAME:
            return _BY_NAME[name]
        raise ValueError(
            f"未知的量子门 '{gate}'。可用门：{', '.join(sorted(_BY_NAME))}"
        )
    raise TypeError(
        f"qgate 的第一个参数必须是门对象或门名字符串，收到 {type(gate).__name__}"
    )


__all__ = [
    "Gate",
    "H", "X", "Y", "Z", "I",
    "CX", "CZ", "CCX", "SWAP",
    "MEASURE",
    "Rx", "Ry", "Rz",
    "resolve",
]
