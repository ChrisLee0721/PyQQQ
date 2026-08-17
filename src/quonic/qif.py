"""qif — quantum-superposition if: compile the if/else branches into a controlled unitary, then decompose into basic gates.

    from quonic import qgate, qif
    from quonic.gates import H, X, Z

    qgate(H, 0)
    qif(0).then(X, 1).else_(Z, 1)   # when q0==1 apply X(q1), otherwise Z(q1)

Physical semantics (key): when the control bit is in a superposition it is **not measured**; the two branches superpose coherently into
|0><0|⊗F + |1><1|⊗T (F=else gate, T=then gate), producing true entanglement. This is fundamentally different from a classical if that "measures first and picks one branch by the result" — the former yields a Bell state (entanglement), the latter a classical mixed state (no entanglement).

MVP boundary: only single-bit branch gates, then/else acting on the same target bit, no nesting, no measurement. All numpy imports are inside functions, guaranteeing zero-cost `import quonic`.
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple, Type, Union

from ._i18n import tr
from .gates import Gate, GateName, resolve
from .ir import (
    Circuit,
    ClassicalIfOperation,
    ClassicalWhileOperation,
    CMeasureOperation,
    CRegCondition,
    GateOperation,
)
from .stack import current_circuit, pop, push


def _unitary(gate: Gate) -> Any:
    """Single-bit gate → 2×2 unitary matrix (numpy array)."""
    from .simulators._gates import single

    return single(gate.name, gate.params)


def _zyz(U: Any) -> Tuple[float, float, float, float]:
    """Single-bit unitary U → (alpha, beta, gamma, delta),
    satisfying U = e^{i·alpha} Rz(beta) Ry(gamma) Rz(delta)."""
    import numpy as np

    U = np.asarray(U, dtype=complex)
    det = np.linalg.det(U)
    alpha = float(np.angle(det) / 2.0)
    W = U * np.exp(-1j * alpha)  # det(W) = 1, entering SU(2)
    a = W[0, 0]
    b = W[0, 1]
    gamma = 2.0 * np.arctan2(abs(b), abs(a))
    if np.isclose(abs(b), 0.0):
        beta = -2.0 * np.angle(a)
        delta = 0.0
    elif np.isclose(abs(a), 0.0):
        gamma = np.pi
        beta = -2.0 * np.angle(-b)
        delta = 0.0
    else:
        beta = -np.angle(a) - np.angle(-b)
        delta = -np.angle(a) + np.angle(-b)
    return alpha, float(beta), float(gamma), float(delta)


def _ctrl_unitary_decompose(V: Any, c: int, t: int) -> List[GateOperation]:
    """Controlled single-bit unitary V → basic gate sequence, implementing |0><0|⊗I + |1><1|⊗V.

    Built using Nielsen-Chuang Figure 4.6: first ZYZ-decompose V = e^{iα} Rz(β) Ry(γ) Rz(δ),
    then set A=Rz(β)Ry(γ/2), B=Ry(-γ/2)Rz(-(δ+β)/2), C=Rz((δ-β)/2), so that
    A·B·C = I and A·X·B·X·C = e^{-iα}V. The corresponding circuit (time order):
    P(α) · C · CX · B · CX · A (the two CX each correspond to an X, with A/B/C acting on the target).
    """
    alpha, beta, gamma, delta = _zyz(V)
    g2 = gamma / 2.0

    def _rot(name: str, angle: float) -> Optional[GateOperation]:
        return GateOperation(name, (t,), (angle,)) if abs(angle) > 1e-12 else None

    ops: List[GateOperation] = []
    if abs(alpha) > 1e-12:
        ops.append(GateOperation("p", (c,), (alpha,)))
    for op in [
        _rot("rz", (delta - beta) / 2.0),   # C
        GateOperation("cx", (c, t)),
        _rot("rz", -(delta + beta) / 2.0),  # B first part
        _rot("ry", -g2),                    # B second part
        GateOperation("cx", (c, t)),
        _rot("ry", g2),                     # A first part
        _rot("rz", beta),                   # A second part
    ]:
        if op is not None:
            ops.append(op)
    return ops


def _qif_decompose(F: Gate, T: Gate, c: int, t: int) -> List[GateOperation]:
    """Compile qif into a basic gate sequence: |0><0|⊗F + |1><1|⊗T = ctrl(T·F†) · (I⊗F).

    First apply F unconditionally (else branch), then apply controlled V=T·F†: control=0 yields F,
    control=1 yields V·F = T·F†·F = T."""
    import numpy as np

    if F == T:
        # same branches → unconditional F; identity gate means empty overall
        return [] if F.name == "i" else [GateOperation(F.name, (t,), F.params)]

    Fm = np.asarray(_unitary(F), dtype=complex)
    Tm = np.asarray(_unitary(T), dtype=complex)
    # apply F first (unconditional), then controlled V: control=0 yields F, control=1 yields V·F=T ⟹ V=T·F†
    V = Tm @ Fm.conj().T
    ops = _ctrl_unitary_decompose(V, c, t)
    # when F is the identity gate, skip emitting a useless I gate (common with else_(I, ...))
    if F.name == "i":
        return ops
    return [GateOperation(F.name, (t,), F.params)] + ops


def _check_branch(g: Gate, which: str, kind: str = "qif") -> None:
    if g.num_qubits != 1:
        raise ValueError(tr("err.qif_single_bit", kind=kind, which=which, name=g.name))
    if g.name == "measure":
        raise ValueError(tr("err.qif_unitary", kind=kind))


class _QIfBuilder:
    def __init__(self, control: int) -> None:
        self.control: int = int(control)
        self._then: Optional[Tuple[Gate, int]] = None
        self._else: Optional[Tuple[Gate, int]] = None

    def then(self, gate: Union[Gate, GateName], target: int) -> _QIfBuilder:
        g = resolve(gate)
        _check_branch(g, "then")
        self._then = (g, int(target))
        return self

    def else_(self, gate: Union[Gate, GateName], target: int) -> List[GateOperation]:
        g = resolve(gate)
        _check_branch(g, "else")
        self._else = (g, int(target))
        return self._compile()

    def _compile(self) -> List[GateOperation]:
        if self._then is None:
            raise ValueError(tr("err.qif_missing_then"))
        if self._else is None:
            raise ValueError(tr("err.qif_missing_else"))
        T, tt = self._then
        F, ft = self._else
        if tt != ft:
            raise ValueError(tr("err.qif_same_target", tt=tt, ft=ft))
        if self.control == tt:
            raise ValueError(tr("err.qif_ctrl_eq_target"))
        ops = _qif_decompose(F, T, self.control, tt)
        circ = current_circuit()
        for op in ops:
            circ.add(op)
        return ops


def qif(control: int) -> _QIfBuilder:
    """Quantum-superposition if entry point, returning a builder for chaining .then(...).else_(...)."""
    return _QIfBuilder(control)


def controlled(
    gate: Union[Gate, GateName], control: int, target: int
) -> List[GateOperation]:
    """Apply a controlled single-bit gate `gate` to target, with control as the control bit.

    Example: controlled(X, 0, 1) is equivalent to CNOT(0,1). Implemented via ZYZ + controlled-U decomposition,
    with the result appended to the current circuit. gate may be a gate object or a gate name string (e.g. "h" / Rx(0.5)).
    """
    g = resolve(gate)
    if g.num_qubits != 1:
        raise ValueError(tr("err.controlled_single", name=g.name))
    if g.name == "measure":
        raise ValueError(tr("err.controlled_unitary"))
    control = int(control)
    target = int(target)
    if control == target:
        raise ValueError(tr("err.controlled_ctrl_eq_target"))
    ops = _ctrl_unitary_decompose(_unitary(g), control, target)
    circ = current_circuit()
    for op in ops:
        circ.add(op)
    return ops


def _to_register_value(value: Union[int, str]) -> int:
    """Normalize a register value to an integer: accept an int or a "0/1" bitstring (MSB first)."""
    if isinstance(value, str):
        if not value or any(c not in "01" for c in value):
            raise ValueError(tr("err.creg_bitstring", value=value))
        return int(value, 2)
    return int(value)


class _CRegBit:
    """A single bit slice of a CReg, enabling ``flag[i].measure(q)``."""

    def __init__(self, creg: CReg, bit: int) -> None:
        self.creg: CReg = creg
        self.bit: int = int(bit)

    def measure(self, qubit: int) -> CReg:
        return self.creg.measure(qubit, self.bit)


class CReg:
    """Named classical register of ``width`` bits (width=1 is a single classical bit).

    Holds measurement results read by cif / cwhile; the register value is an integer
    in [0, 2**width), where bit i is stored by ``measure(q, bit=i)``.
    """

    def __init__(self, name: str, width: int = 1) -> None:
        if not isinstance(name, str) or not name:
            raise ValueError(tr("err.creg_name", name=name))
        width = int(width)
        if width < 1:
            raise ValueError(tr("err.creg_width", width=width))
        self.name: str = name
        self.width: int = width

    def measure(self, qubit: int, bit: int = 0) -> CReg:
        """Measure qubit into register bit ``bit``. Returns self for chaining."""
        bit = int(bit)
        if not 0 <= bit < self.width:
            raise ValueError(tr("err.creg_bit", bit=bit, width=self.width))
        current_circuit().add(CMeasureOperation(int(qubit), self.name, bit))
        return self

    def __getitem__(self, bit: int) -> _CRegBit:
        return _CRegBit(self, bit)

    def __repr__(self) -> str:
        if self.width == 1:
            return f"CReg({self.name!r})"
        return f"CReg({self.name!r}, width={self.width})"


def creg(name: str, width: int = 1) -> CReg:
    """Declare a named classical register of ``width`` bits (width=1 by default).

    Usage: flag = creg("flag"); flag.measure(0) stores the measurement of qubit 0
    into bit 0; a width-2 register stores two bits via flag.measure(0, bit=0) and
    flag.measure(1, bit=1), then cif(flag, 2) / cwhile(flag, until=2) branch or loop
    on the full register value.
    """
    return CReg(name, width)


class _CIfBuilder:
    def __init__(self, control: Union[int, CReg], value: Union[int, str] = 1) -> None:
        self.control: Union[int, CReg] = control  # int (qubit) or CReg (classical register)
        self._value: Union[int, str] = value
        self._then: Optional[Tuple[Gate, int]] = None
        self._else: Optional[Tuple[Gate, int]] = None

    def then(self, gate: Union[Gate, GateName], target: int) -> _CIfBuilder:
        g = resolve(gate)
        _check_branch(g, "then", "cif")
        self._then = (g, int(target))
        return self

    def else_(self, gate: Union[Gate, GateName], target: int) -> ClassicalIfOperation:
        g = resolve(gate)
        _check_branch(g, "else", "cif")
        self._else = (g, int(target))
        return self._compile()

    def _compile(self) -> ClassicalIfOperation:
        if self._then is None:
            raise ValueError(tr("err.cif_missing_then"))
        if self._else is None:
            raise ValueError(tr("err.cif_missing_else"))
        T, tt = self._then
        F, ft = self._else
        if tt != ft:
            raise ValueError(tr("err.cif_same_target", tt=tt, ft=ft))
        if isinstance(self.control, CReg):
            reg = self.control
            v = _to_register_value(self._value)
            if not 0 <= v < 2 ** reg.width:
                raise ValueError(tr("err.cif_value", value=self._value, max=2 ** reg.width))
            # single-bit register with value 1 keeps the plain str control (backward compatible)
            ctrl: Union[int, str, CRegCondition] = (
                reg.name if reg.width == 1 and v == 1 else CRegCondition(reg.name, reg.width, v)
            )
        else:
            ctrl = int(self.control)
            if ctrl == tt:
                raise ValueError(tr("err.cif_ctrl_eq_target"))
        op = ClassicalIfOperation(
            ctrl,
            GateOperation(T.name, (tt,), T.params),
            GateOperation(F.name, (ft,), F.params),
        )
        current_circuit().add(op)
        return op


def cif(control: Union[int, CReg], value: Union[int, str] = 1) -> _CIfBuilder:
    """Classical if: apply one of two branch gates depending on the control source.

    Unlike qif (quantum-superposition if), cif produces a classical mixed state rather than coherent entanglement.
    control may be:
      - a qubit index: **measure** that bit first, then branch (measured |1> applies then, |0> applies else);
        ``value`` is ignored in this form.
      - a CReg (a classical register declared with creg()): apply then when the register
        value equals ``value`` (int or "0/1" bitstring), else otherwise. For a single-bit
        register, ``value`` defaults to 1.

    Examples:
        qgate(H, 0)
        cif(0).then(X, 1).else_(Z, 1)      # measure q0 first, then pick one

        flag = creg("flag"); flag.measure(0)
        cif(flag).then(X, 1).else_(I, 1)   # branch on flag == 1

        reg = creg("reg", width=2); reg.measure(0, bit=0); reg.measure(1, bit=1)
        cif(reg, 2).then(X, 2).else_(I, 2) # branch on reg == 2 ("10")
    """
    return _CIfBuilder(control, value)


class _CWhileBuilder:
    def __init__(self, cond: CReg, until: Union[int, str], max_iters: int) -> None:
        if not isinstance(cond, CReg):
            raise TypeError(tr("err.cwhile_cond", cond=cond))
        self.creg: CReg = cond
        self.width: int = cond.width
        self.until: int = _to_register_value(until)
        if not 0 <= self.until < 2 ** self.width:
            raise ValueError(tr("err.cwhile_until", until=until, max=2 ** self.width))
        self.max_iters: int = int(max_iters)
        if self.max_iters < 1:
            raise ValueError(tr("err.cwhile_max_iters", max_iters=self.max_iters))
        self.op: Optional[ClassicalWhileOperation] = None

    def __enter__(self) -> _CWhileBuilder:
        push()  # capture the loop body into a new circuit scope
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> bool:
        body = pop()
        if exc_type is not None:
            return False  # exception in loop body: already popped, propagate upward
        self.op = ClassicalWhileOperation(
            self.creg.name, self.until, tuple(body.ops), self.width
        )
        current_circuit().add(self.op)
        return False

    def groverize(self, success_prob: Optional[float] = None) -> Circuit:
        """Compile this loop into a static Grover circuit (see quonic.compiler.groverize).

        success_prob may be omitted: for a purely unitary body it is inferred exactly by
        simulation, so the common single-rotation RUS case needs no manual probability.
        """
        from .compiler import groverize as _groverize

        if self.op is None:
            raise ValueError(tr("err.grover_no_op"))
        return _groverize(self.op, success_prob)


def cwhile(
    cond: CReg, until: Union[int, str] = 0, max_iters: int = 10000
) -> _CWhileBuilder:
    """Classical feedback loop (repeat-until-success): repeat the loop body until the creg
    register value equals until (an int register value, or a "0/1" bitstring MSB-first).
    The loop body ends with creg.measure(...) to update the condition.

    Usage (context manager):
        flag = creg("flag")
        with cwhile(flag, until=0):
            qgate(H, 0)
            flag.measure(0)   # re-measure flag on every attempt

    Capture the loop object and call .groverize() to compile it into a static circuit:

        with cwhile(flag, until=0) as loop:
            qgate(Ry(2 * math.pi / 3), 0)
            flag.measure(0)
        static = loop.groverize()   # success_prob auto-inferred for unitary bodies

    Note: only the native backend supports cwhile (dynamic per-shot execution); other backends raise
    NotImplementedError. The loop body must measure the condition creg, otherwise it loops until the
    max_iters limit.
    """
    return _CWhileBuilder(cond, until, max_iters)
