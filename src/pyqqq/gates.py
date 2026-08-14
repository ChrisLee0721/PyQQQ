"""内置量子门。

门对象是主推 API（与 Qiskit/Cirq 风格一致）：
    from pyqqq.gates import H, X, CX
    qgate(H, 0)

qgate() 同时接受门对象或门名字符串（如 qgate("h", 0)）。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Gate:
    name: str
    num_qubits: int


H = Gate("h", 1)
X = Gate("x", 1)
Y = Gate("y", 1)
Z = Gate("z", 1)
CX = Gate("cx", 2)
MEASURE = Gate("measure", 1)

_BY_NAME = {g.name: g for g in (H, X, Y, Z, CX, MEASURE)}


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


__all__ = ["Gate", "H", "X", "Y", "Z", "CX", "MEASURE", "resolve"]
