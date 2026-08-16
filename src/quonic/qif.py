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
    ClassicalIfOperation,
    ClassicalWhileOperation,
    CMeasureOperation,
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


class CReg:
    """Named classical bit: holds one measurement result, read by cif / cwhile."""

    def __init__(self, name: str) -> None:
        if not isinstance(name, str) or not name:
            raise ValueError(tr("err.creg_name", name=name))
        self.name: str = name

    def measure(self, qubit: int) -> CReg:
        """Measure qubit and store the result in this classical bit. Returns self for chaining."""
        current_circuit().add(CMeasureOperation(int(qubit), self.name))
        return self

    def __repr__(self) -> str:
        return f"CReg({self.name!r})"


def creg(name: str) -> CReg:
    """Declare a named classical bit.

    Usage: flag = creg("flag"); flag.measure(0) stores the measurement result of qubit 0;
    then pass it to cif(flag) / cwhile(flag) for branching or looping.
    """
    return CReg(name)


class _CIfBuilder:
    def __init__(self, control: Union[int, CReg]) -> None:
        self.control: Union[int, CReg] = control  # int (qubit) or CReg (classical bit)
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
            ctrl: Union[int, str] = self.control.name
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


def cif(control: Union[int, CReg]) -> _CIfBuilder:
    """Classical if: apply one of two branch gates depending on the control source.

    Unlike qif (quantum-superposition if), cif produces a classical mixed state rather than coherent entanglement.
    control may be:
      - a qubit index: **measure** that bit first, then branch (measured |1> applies then, |0> applies else)
      - a CReg (a classical bit declared with creg()): directly read the already-stored measurement result

    Examples:
        qgate(H, 0)
        cif(0).then(X, 1).else_(Z, 1)      # measure q0 first, then pick one

        flag = creg("flag"); flag.measure(0)
        cif(flag).then(X, 1).else_(I, 1)   # branch on flag's stored result
    """
    return _CIfBuilder(control)


class _CWhileBuilder:
    def __init__(self, cond: CReg, until: int, max_iters: int) -> None:
        if not isinstance(cond, CReg):
            raise TypeError(tr("err.cwhile_cond", cond=cond))
        self.creg: CReg = cond
        self.until: int = int(until)
        if self.until not in (0, 1):
            raise ValueError(tr("err.cwhile_until", until=self.until))
        self.max_iters: int = int(max_iters)
        if self.max_iters < 1:
            raise ValueError(tr("err.cwhile_max_iters", max_iters=self.max_iters))

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
        op = ClassicalWhileOperation(self.creg.name, self.until, tuple(body.ops))
        current_circuit().add(op)
        return False


def cwhile(cond: CReg, until: int = 0, max_iters: int = 10000) -> _CWhileBuilder:
    """Classical feedback loop (repeat-until-success): repeat the loop body until the creg measurement
    result equals until. The loop body ends with creg.measure(...) to update the condition.

    Usage (context manager):
        flag = creg("flag")
        with cwhile(flag, until=0):
            qgate(H, 0)
            flag.measure(0)   # re-measure flag on every attempt

    Note: only the native backend supports cwhile (dynamic per-shot execution); other backends raise
    NotImplementedError. The loop body must measure the condition creg, otherwise it loops until the
    max_iters limit.
    """
    return _CWhileBuilder(cond, until, max_iters)
