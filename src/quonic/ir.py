"""Backend-independent intermediate representation (IR).

qgate() first records user operations into backend-independent GateOperation / Circuit,
then qshow() hands them to a concrete backend (Qiskit / Cirq / ...) to translate and execute.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Union


@dataclass(frozen=True)
class GateOperation:
    name: str
    qubits: Tuple[int, ...]
    params: Tuple[float, ...] = ()


@dataclass(frozen=True)
class ClassicalIfOperation:
    """Classical control flow: apply one of two branch gates depending on the control source.

    Unlike qif's quantum superposition, this produces a classical mixed state (incoherent entanglement).
    control may be:
      - int: measure that qubit (measure first, then branch)
      - str: read the measurement result already stored in the named classical bit creg
    then_op / else_op are single-bit branch gates.
    """

    control: Union[int, str]
    then_op: GateOperation
    else_op: GateOperation

    @property
    def name(self) -> str:
        return "cif"

    @property
    def params(self) -> Tuple[()]:
        return ()

    @property
    def qubits(self) -> Tuple[int, ...]:
        qs = set()
        if isinstance(self.control, int):
            qs.add(self.control)
        qs.update(self.then_op.qubits)
        qs.update(self.else_op.qubits)
        return tuple(sorted(qs))


@dataclass(frozen=True)
class CMeasureOperation:
    """Measure qubit and store the result in the named classical bit creg."""

    qubit: int
    creg: str

    @property
    def name(self) -> str:
        return "cmeasure"

    @property
    def params(self) -> Tuple[()]:
        return ()

    @property
    def qubits(self) -> Tuple[int, ...]:
        return (self.qubit,)


@dataclass(frozen=True)
class ClassicalWhileOperation:
    """Classical feedback loop: repeat body until the creg measurement result equals until.

    body is a tuple of ops (usually ending with creg.measure(...) to update the condition),
    the core of repeat-until-success (RUS) dynamic circuits.
    """

    creg: str
    until: int
    body: Tuple[object, ...]

    @property
    def name(self) -> str:
        return "cwhile"

    @property
    def params(self) -> Tuple[()]:
        return ()

    @property
    def qubits(self) -> Tuple[int, ...]:
        qs = set()
        for op in self.body:
            qs.update(op.qubits)
        return tuple(sorted(qs))


_MEASURE_NAMES = ("measure", "cmeasure")


class Circuit:
    def __init__(self) -> None:
        self.ops: List[object] = []
        self.num_qubits: int = 0

    def add(self, op: object) -> None:
        self.ops.append(op)
        for q in op.qubits:
            if q + 1 > self.num_qubits:
                self.num_qubits = q + 1

    def allocate(self, n_qubits: int) -> None:
        # pre-reserve qubits (without emitting a gate), so QInt etc. can occupy indices even without initial gates
        if n_qubits > self.num_qubits:
            self.num_qubits = n_qubits

    def measured_qubits(self) -> set:
        measured = set()
        for op in self.ops:
            if op.name == "measure":
                measured.add(op.qubits[0])
            elif op.name == "cmeasure":
                measured.add(op.qubit)
            elif op.name == "cif":
                if isinstance(op.control, int):
                    measured.add(op.control)
        return measured

    def unmeasured_qubits(self) -> List[int]:
        measured = self.measured_qubits()
        return [q for q in range(self.num_qubits) if q not in measured]

    def is_empty(self) -> bool:
        return not self.ops

    def gate_count(self) -> int:
        """Logical gate count (excluding measurement gates)."""
        return sum(1 for op in self.ops if op.name not in _MEASURE_NAMES)

    def depth(self) -> int:
        """Circuit depth: the longest dependency chain of non-measurement gates (multi-qubit gates synchronized per-qubit clock)."""
        clocks = [0] * self.num_qubits
        for op in self.ops:
            if op.name in _MEASURE_NAMES:
                continue
            d = max(clocks[q] for q in op.qubits) + 1
            for q in op.qubits:
                clocks[q] = d
        return max(clocks) if clocks else 0
