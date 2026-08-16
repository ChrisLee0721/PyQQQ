"""Built-in quantum gates.

Gate objects are the primary API (consistent with the Qiskit/Cirq style):
    from quonic.gates import H, X, CX
    qgate(H, 0)

qgate() accepts either a gate object or a gate name string (e.g. qgate("h", 0)).
Parameterized gates (Rx/Ry/Rz) are factory functions that return gate objects with parameters:
    from quonic.gates import Rx
    qgate(Rx(0.5), 0)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Tuple, Union

from ._i18n import tr


@dataclass(frozen=True)
class Gate:
    name: str
    num_qubits: int
    params: Tuple[float, ...] = field(default_factory=tuple)


H = Gate("h", 1)
X = Gate("x", 1)
Y = Gate("y", 1)
Z = Gate("z", 1)
I = Gate("i", 1)  # noqa: E741  # identity gate, standard symbol
CX = Gate("cx", 2)
CZ = Gate("cz", 2)
CCX = Gate("ccx", 3)
SWAP = Gate("swap", 2)
MEASURE = Gate("measure", 1)


def _angle(theta: float) -> float:
    try:
        return float(theta)
    except (TypeError, ValueError):
        raise TypeError(
            tr("err.gate_angle", theta=theta, type=type(theta).__name__)
        ) from None


def Rx(theta: float) -> Gate:
    return Gate("rx", 1, (_angle(theta),))


def Ry(theta: float) -> Gate:
    return Gate("ry", 1, (_angle(theta),))


def Rz(theta: float) -> Gate:
    return Gate("rz", 1, (_angle(theta),))


_BY_NAME = {g.name: g for g in (H, X, Y, Z, I, CX, CZ, CCX, SWAP, MEASURE)}

# the allowed values of a gate name string. IDEs (Pylance) use this to autocomplete gate names inside qgate("...").
GateName = Literal["h", "x", "y", "z", "i", "cx", "cz", "ccx", "swap", "measure"]


def resolve(gate: Union[Gate, GateName]) -> Gate:
    """Resolve a gate object or gate name string into a Gate object."""
    if isinstance(gate, Gate):
        return gate
    if isinstance(gate, str):
        name = gate.strip().lower()
        if name in _BY_NAME:
            return _BY_NAME[name]
        raise ValueError(
            tr("err.unknown_gate", gate=gate, gates=", ".join(sorted(_BY_NAME)))
        )
    raise TypeError(tr("err.qgate_arg", type=type(gate).__name__))


__all__ = [
    "Gate",
    "GateName",
    "H", "X", "Y", "Z", "I",
    "CX", "CZ", "CCX", "SWAP",
    "MEASURE",
    "Rx", "Ry", "Rz",
    "resolve",
]
