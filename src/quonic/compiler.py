"""Compiler seam: gate decomposition + topology validation (does not execute, does not touch real hardware).

Two things:

1. **Gate decomposition** (`decompose`) — expands high-level gates into the basic gate set; it is the backend-independent
   "portable core" owned by QuoNic, so users are not tied to any backend's circuit shape.
2. **Connectivity validation** (`compile`) — checks against the coupling_map whether two/multi-qubit gates
   fall on allowed edges; raises RoutingError if they do not fit.

SWAP routing is the reserved next extension point, wired in right after this without changing the IR or the scheduler.
"""

from __future__ import annotations

import math
from collections import deque
from typing import Callable, Dict, List, Optional, Set, Tuple

from ._i18n import tr
from .ir import (
    Circuit,
    ClassicalIfOperation,
    ClassicalWhileOperation,
    CMeasureOperation,
    GateOperation,
)
from .topology import CouplingMap


class RoutingError(ValueError):
    """The circuit cannot be mapped onto the target coupling map."""


# the basic gate set allowed after decomposition (decompose's output is guaranteed to lie within it)
BASIC_GATES: Set[str] = {"i", "h", "x", "y", "z", "rx", "ry", "rz", "p", "cx", "cz"}


def _p(q: int, theta: float) -> GateOperation:
    return GateOperation("p", (q,), (theta,))


def _decompose_cp(c: int, t: int, theta: float) -> List[GateOperation]:
    """Controlled phase cp(theta) = p·cx·p·cx·p (exact, no ancilla)."""
    half = theta / 2
    return [
        _p(c, half),
        GateOperation("cx", (c, t)),
        _p(t, -half),
        GateOperation("cx", (c, t)),
        _p(t, half),
    ]


def _decompose_ccx(a: int, b: int, c: int) -> List[GateOperation]:
    """Exact Toffoli (Nielsen-Chuang Figure 4.9), using p(π/4) as the T gate, 6 cx gates."""
    t = math.pi / 4
    return [
        GateOperation("h", (c,)),
        GateOperation("cx", (b, c)),
        _p(c, -t),
        GateOperation("cx", (a, c)),
        _p(c, t),
        GateOperation("cx", (b, c)),
        _p(c, -t),
        GateOperation("cx", (a, c)),
        _p(b, t),
        _p(c, t),
        GateOperation("h", (c,)),
        GateOperation("cx", (a, b)),
        _p(a, t),
        _p(b, -t),
        GateOperation("cx", (a, b)),
    ]


def _decompose_mcx(
    controls: Tuple[int, ...],
    target: int,
    new_ancillas: Callable[[int], Tuple[int, ...]],
) -> List[GateOperation]:
    """Multi-controlled X: k=1 -> cx; k=2 -> Toffoli; k>=3 -> AND cascade (k-2 clean ancillas)."""
    k = len(controls)
    if k == 1:
        return [GateOperation("cx", (controls[0], target))]
    if k == 2:
        return _decompose_ccx(controls[0], controls[1], target)

    anc = new_ancillas(k - 2)
    ops: List[GateOperation] = []
    # forward: anc[0] = c1&c2, anc[j] = anc[j-1] & c_{j+2}
    ops += _decompose_ccx(controls[0], controls[1], anc[0])
    for j in range(1, k - 2):
        ops += _decompose_ccx(anc[j - 1], controls[j + 1], anc[j])
    # apply: t ^= anc[k-3] & c_k
    ops += _decompose_ccx(anc[k - 3], controls[k - 1], target)
    # uncompute (restore ancilla to |0>)
    for j in range(k - 3, 0, -1):
        ops += _decompose_ccx(anc[j - 1], controls[j + 1], anc[j])
    ops += _decompose_ccx(controls[0], controls[1], anc[0])
    return ops


def _decompose_mcz(
    qubits: Tuple[int, ...],
    new_ancillas: Callable[[int], Tuple[int, ...]],
) -> List[GateOperation]:
    """Multi-controlled Z: the last bit is the target, mcz = H·mcx·H; a single control becomes cz directly."""
    t = qubits[-1]
    controls = qubits[:-1]
    if len(controls) == 1:
        return [GateOperation("cz", (controls[0], t))]
    return (
        [GateOperation("h", (t,))]
        + _decompose_mcx(controls, t, new_ancillas)
        + [GateOperation("h", (t,))]
    )


def decompose(circuit: Circuit) -> Circuit:
    """Expand high-level gates (cp / ccx / mcz) into the basic gate set, returning a new Circuit.

    The output gate set ∈ {i, h, x, y, z, rx, ry, rz, p, cx, cz} (BASIC_GATES).
    Multi-controlled mcz (>2 controls) introduces clean ancillas (both start and end at |0>), so the output bit count
    may exceed the input. The decomposition is exact (no relative phase) and can be verified against the statevector.

    The original circuit object is not modified.
    """
    out = Circuit()
    out.allocate(circuit.num_qubits)
    # reusable clean ancillas: after each multi-controlled gate decomposition the ancillas are restored to |0>,
    # so the same set of ancillas can be reused by subsequent gates; total ancilla count = the maximum required by any gate.
    pool: List[int] = []
    next_ancilla = [circuit.num_qubits]

    def new_ancillas(m: int) -> Tuple[int, ...]:
        while len(pool) < m:
            pool.append(next_ancilla[0])
            next_ancilla[0] += 1
        return tuple(pool[:m])

    for op in circuit.ops:
        if op.name == "cp":
            for g in _decompose_cp(op.qubits[0], op.qubits[1], op.params[0]):
                out.add(g)
        elif op.name == "ccx":
            for g in _decompose_ccx(*op.qubits):
                out.add(g)
        elif op.name == "mcz":
            for g in _decompose_mcz(op.qubits, new_ancillas):
                out.add(g)
        else:
            out.add(op)
    return out


def _violates(op: GateOperation, coupling_map: CouplingMap) -> bool:
    """Whether any pair of qubits in a two/multi-qubit gate are not connected."""
    qs = op.qubits
    if len(qs) < 2:
        return False
    for i in range(len(qs)):
        for j in range(i + 1, len(qs)):
            if not coupling_map.has_edge(qs[i], qs[j]):
                return True
    return False


def compile(
    circuit: Circuit,
    coupling_map: Optional[CouplingMap] = None,
    route: bool = False,
) -> Circuit:
    """Compile the circuit onto the target topology, returning a new Circuit (without modifying the original).

    Parameters:
        circuit: the source circuit.
        coupling_map: a CouplingMap; None means fully connected (no connectivity constraints).
        route: when True, decompose high-level gates (cp/ccx/mcz) and insert SWAPs to map
            every two-qubit gate onto the coupling_map, instead of only validating connectivity.

    With route=False this only performs connectivity validation (raising RoutingError on violation).
    With route=True it returns a routed copy: ``route_swaps(decompose(circuit), coupling_map)``.
    cwhile loops cannot be routed directly — groverize() them into a static circuit first.
    """
    if route:
        dec = decompose(circuit)
        if coupling_map is None:
            return dec
        return route_swaps(dec, coupling_map)

    out = Circuit()
    out.allocate(circuit.num_qubits)

    if coupling_map is None:
        for op in circuit.ops:
            out.add(op)
        return out

    problems = [
        op for op in circuit.ops
        if op.name not in ("measure", "cmeasure", "cif", "cwhile")
        and _violates(op, coupling_map)
    ]
    if problems:
        detail = ", ".join(f"{op.name}{op.qubits}" for op in problems[:5])
        if len(problems) > 5:
            detail += tr("err.routing_etc", n=len(problems))
        raise RoutingError(
            tr("err.routing", map=coupling_map, detail=detail)
        )

    for op in circuit.ops:
        out.add(op)
    return out


# ---------------------------------------------------------------------------
# SWAP routing
# ---------------------------------------------------------------------------

def _adjacency(coupling_map: CouplingMap) -> Dict[int, Set[int]]:
    adj: Dict[int, Set[int]] = {q: set() for q in range(coupling_map.n)}
    for u, v in coupling_map.edges():
        adj[u].add(v)
        adj[v].add(u)
    return adj


def _shortest_path(
    adj: Dict[int, Set[int]], src: int, dst: int
) -> Optional[List[int]]:
    """BFS shortest path on the coupling map, returning the node sequence [src, ..., dst]; returns None if disconnected."""
    if src == dst:
        return [src]
    prev: Dict[int, Optional[int]] = {src: None}
    q: deque = deque([src])
    while q:
        u = q.popleft()
        if u == dst:
            break
        for v in adj.get(u, ()):
            if v not in prev:
                prev[v] = u
                q.append(v)
    if dst not in prev:
        return None
    path: List[int] = []
    cur: Optional[int] = dst
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return path[::-1]


def route_swaps(circuit: Circuit, coupling_map: CouplingMap) -> Circuit:
    """Greedy SWAP routing: map two-qubit gates onto the coupling map, inserting SWAPs to bring their ends adjacent.

    Returns a new Circuit whose gate qubit indices are replaced with "physical bit" positions, inserting a "swap" gate
    (on adjacent physical bits) at each two-qubit gate whose ends are not adjacent. Single-qubit gate/measurement indices
    are updated with the mapping; three-or-more-qubit gates are passed through unchanged (callers should decompose() first).
    The original circuit is not modified.
    """
    adj = _adjacency(coupling_map)
    n_phys = max(circuit.num_qubits, coupling_map.n)
    layout = list(range(n_phys))  # layout[q] = the current physical position of logical q
    out = Circuit()
    out.allocate(n_phys)

    def emit(
        name: str, qubits: Tuple[int, ...], params: Tuple[float, ...] = ()
    ) -> None:
        out.add(GateOperation(name, tuple(qubits), params))

    for op in circuit.ops:
        if op.name == "measure":
            emit("measure", (layout[op.qubits[0]],))
            continue
        if op.name == "cif":
            # classical control flow has no adjacency constraint; only remap control/target bit indices with the layout
            ctrl = layout[op.control] if isinstance(op.control, int) else op.control
            out.add(
                ClassicalIfOperation(
                    ctrl,
                    GateOperation(
                        op.then_op.name,
                        (layout[op.then_op.qubits[0]],),
                        op.then_op.params,
                    ),
                    GateOperation(
                        op.else_op.name,
                        (layout[op.else_op.qubits[0]],),
                        op.else_op.params,
                    ),
                )
            )
            continue
        if op.name == "cmeasure":
            # named classical bit measurement: only remap the qubit index, keep the creg name
            out.add(CMeasureOperation(layout[op.qubit], op.creg))
            continue
        if op.name == "cwhile":
            raise NotImplementedError(tr("err.routing_cwhile"))
        if len(op.qubits) == 1:
            emit(op.name, (layout[op.qubits[0]],), op.params)
            continue
        if len(op.qubits) != 2:
            emit(op.name, tuple(layout[q] for q in op.qubits), op.params)
            continue

        c, t = op.qubits
        while True:
            pc, pt = layout[c], layout[t]
            if pt in adj.get(pc, ()):
                emit(op.name, (pc, pt), op.params)
                break
            path = _shortest_path(adj, pc, pt)
            if path is None or len(path) < 2:
                raise RoutingError(
                    tr("err.routing_disconnected", name=op.name, qubits=op.qubits)
                )
            u, v = path[0], path[1]
            emit("swap", (u, v))
            lu, lv = layout.index(u), layout.index(v)
            layout[lu], layout[lv] = layout[lv], layout[lu]

    return out


# ---------------------------------------------------------------------------
# cwhile Grover-ization (compile a repeat-until-success loop into a static circuit)
# ---------------------------------------------------------------------------

# gates whose adjoint is obtained by negating their angle (all others are self-adjoint)
_ADJOINT_NEGATED = frozenset({"rx", "ry", "rz", "p", "cp"})


def _adjoint(op: GateOperation) -> GateOperation:
    """Return the Hermitian adjoint of a single gate operation (self-adjoint gates return themselves)."""
    if op.name in _ADJOINT_NEGATED:
        return GateOperation(op.name, op.qubits, tuple(-a for a in op.params))
    return op


def _oracle_multi(ancillas: List[int], until: int) -> List[GateOperation]:
    """Phase-flip the basis states where the ancilla register equals ``until``.

    Flips an X on each ancilla whose target bit is 0, applies a multi-controlled Z,
    then uncomputes the X gates — so only the register-value == ``until`` state is flipped.
    """
    width = len(ancillas)
    ops: List[GateOperation] = []
    for i in range(width):
        if (until >> i) & 1 == 0:
            ops.append(GateOperation("x", (ancillas[i],)))
    if width == 1:
        ops.append(GateOperation("z", (ancillas[0],)))
    else:
        ops.append(GateOperation("mcz", tuple(ancillas)))
    for i in range(width):
        if (until >> i) & 1 == 0:
            ops.append(GateOperation("x", (ancillas[i],)))
    return ops


def _reflect_zero(circuit: Circuit, n: int) -> None:
    """Append the reflection 2|0…0⟩⟨0…0| − I about the all-zero state."""
    for q in range(n):
        circuit.add(GateOperation("x", (q,)))
    if n == 1:
        circuit.add(GateOperation("z", (0,)))
    else:
        circuit.add(GateOperation("mcz", tuple(range(n))))
    for q in range(n):
        circuit.add(GateOperation("x", (q,)))


def _infer_success_prob(cwhile_op: ClassicalWhileOperation) -> float:
    """Infer the single-shot success probability p by simulating the unitary body on |0…0⟩.

    The loop body is a unitary sequence ending with ``width`` cmeasure ops writing each bit of
    the creg register; deferred measurement copies each measured qubit onto a |0⟩-initialized
    ancilla, so P(success) is exactly P(register == until) under the body unitary. This is exact
    for any unitary body, so the caller only needs ``success_prob`` when the body already
    contains measurements.
    """
    import numpy as np

    from .simulators import StatevectorEngine

    body = cwhile_op.body
    width = cwhile_op.width
    measures = list(body[-width:])
    unitary = list(body[:-width])
    n_data = max(q for o in body for q in o.qubits) + 1

    engine = StatevectorEngine(n_data)
    for o in unitary:
        engine.apply(o.name, list(o.qubits), o.params)

    probs = np.abs(engine.state) ** 2
    idx = np.arange(2 ** n_data)
    reg = np.zeros(2 ** n_data, dtype=int)
    for m in measures:
        reg |= ((idx >> m.qubit) & 1) << m.bit
    return float(np.sum(probs[reg == cwhile_op.until]))


def groverize(
    cwhile_op: ClassicalWhileOperation, success_prob: Optional[float] = None
) -> Circuit:
    """Compile a repeat-until-success ``cwhile`` loop into a static Grover circuit.

    The loop body must be a purely unitary gate sequence ending with a single
    ``creg.measure(q)`` (the success criterion). The measurement is deferred onto a
    fresh ancilla (|0⟩ → CX), and the success subspace (ancilla == until) is amplitude
    amplified with k = ⌊π / (4·arcsin(√p))⌋ Grover iterations, where p = success_prob
    is the single-shot success probability. This trades the classical O(1/p) retries
    for O(1/√p) oracle calls and yields a static, backend-independent circuit.

    Parameters:
        cwhile_op: the ``ClassicalWhileOperation`` produced by the ``with cwhile(...)`` block.
        success_prob: the single-shot success probability p ∈ (0, 1). When omitted (None),
            it is inferred exactly by simulating the unitary body on |0…0⟩.

    Returns: a new ``Circuit`` (data qubits + one ancilla) that measures all qubits at the end.
        The ancilla is the highest-index qubit; its measurement equals ``until`` on success.
    """
    if not isinstance(cwhile_op, ClassicalWhileOperation):
        raise TypeError(tr("err.grover_type", type=type(cwhile_op).__name__))

    body = cwhile_op.body
    width = cwhile_op.width
    if not body or len(body) < width:
        raise ValueError(tr("err.grover_body_unitary"))

    measures = list(body[-width:])
    unitary = list(body[:-width])
    for m in measures:
        if not isinstance(m, CMeasureOperation) or m.creg != cwhile_op.creg:
            raise ValueError(tr("err.grover_body_unitary"))
    if sorted(m.bit for m in measures) != list(range(width)):
        raise ValueError(tr("err.grover_body_bits"))
    for o in unitary:
        if not isinstance(o, GateOperation) or o.name == "measure":
            raise ValueError(tr("err.grover_body_unitary"))

    if success_prob is None:
        p = _infer_success_prob(cwhile_op)
    else:
        p = float(success_prob)
    if not (0.0 < p < 1.0):
        raise ValueError(tr("err.grover_prob", p=p))

    n_data = max(q for o in body for q in o.qubits) + 1
    ancillas = [n_data + i for i in range(width)]
    n_total = n_data + width

    u = unitary + [
        GateOperation("cx", (m.qubit, ancillas[m.bit])) for m in measures
    ]
    u_dag = [
        GateOperation("cx", (m.qubit, ancillas[m.bit])) for m in reversed(measures)
    ] + [_adjoint(o) for o in reversed(unitary)]

    k = int(math.pi / (4 * math.asin(math.sqrt(p))))

    out = Circuit()
    out.allocate(n_total)

    def _emit(ops: List[GateOperation]) -> None:
        for o in ops:
            out.add(o)

    _emit(u)
    for _ in range(k):
        _emit(_oracle_multi(ancillas, cwhile_op.until))
        _emit(u_dag)
        # The reflection acts on the data qubits only: after u† the ancilla is
        # uncomputed back to |0…0⟩, so reflecting about the data |0…0⟩ is
        # equivalent to reflecting about the full |0…0⟩ on the relevant subspace —
        # this turns a C^(n_total-1)Z into a far cheaper C^(n_data-1)Z.
        _reflect_zero(out, n_data)
        _emit(u)

    for q in range(n_total):
        out.add(GateOperation("measure", (q,)))
    return out


# ---------------------------------------------------------------------------
#  Optimization passes
# ---------------------------------------------------------------------------

# Self-inverse gates: applying twice = identity
_SELF_INVERSE: Set[str] = {"x", "y", "z", "h", "cx", "cz", "swap", "ccx"}


def optimize_cancel(circuit: Circuit) -> Circuit:
    """Cancel adjacent self-inverse gate pairs (G·G = I).

    Scans the ops list and removes adjacent pairs of the same self-inverse
    gate on the same qubits.
    """
    out = Circuit()
    out.allocate(circuit.num_qubits)
    ops = list(circuit.ops)
    i = 0
    while i < len(ops):
        if (
            i + 1 < len(ops)
            and isinstance(ops[i], GateOperation)
            and isinstance(ops[i + 1], GateOperation)
            and ops[i].name == ops[i + 1].name
            and ops[i].qubits == ops[i + 1].qubits
            and ops[i].name in _SELF_INVERSE
        ):
            i += 2  # skip the pair
        else:
            out.add(ops[i])
            i += 1
    return out


# Commutation table: gates on different qubits always commute.
# Gates on the same qubit: these pairs commute (can be reordered).
_SAME_QUBIT_COMMUTE: Set[Tuple[str, str]] = {
    ("x", "z"), ("z", "x"),
    ("y", "z"), ("z", "y"),
    ("x", "y"), ("y", "x"),
    ("h", "z"), ("z", "h"),
    ("rx", "rz"), ("rz", "rx"),
    ("ry", "rz"), ("rz", "ry"),
}


def _commutes(a: GateOperation, b: GateOperation) -> bool:
    """Check if two gate operations commute (can be reordered)."""
    # Different qubits always commute
    if set(a.qubits).isdisjoint(set(b.qubits)):
        return True
    # Same qubits: check commutation table
    if a.qubits == b.qubits:
        return (a.name, b.name) in _SAME_QUBIT_COMMUTE
    # Overlapping but not identical qubit sets: don't commute (conservative)
    return False


def optimize_commute(circuit: Circuit) -> Circuit:
    """Reorder gates to bring cancelable pairs together.

    Uses bubble-sort-style passes: for each gate, try to move it left past
    commuting gates to find a cancelable neighbor.
    """
    ops = list(circuit.ops)
    changed = True
    while changed:
        changed = False
        for i in range(1, len(ops)):
            if not isinstance(ops[i], GateOperation):
                continue
            if not isinstance(ops[i - 1], GateOperation):
                continue
            # Try to swap ops[i] left if it commutes with ops[i-1]
            if _commutes(ops[i], ops[i - 1]):
                # Check if swapping creates a cancelable pair with ops[i-2]
                if (
                    i >= 2
                    and isinstance(ops[i - 2], GateOperation)
                    and ops[i].name == ops[i - 2].name
                    and ops[i].qubits == ops[i - 2].qubits
                    and ops[i].name in _SELF_INVERSE
                ):
                    # Swap to bring the pair together
                    ops[i - 1], ops[i] = ops[i], ops[i - 1]
                    changed = True
    out = Circuit()
    out.allocate(circuit.num_qubits)
    for op in ops:
        out.add(op)
    return out


# Peephole patterns: (sequence of gate names+qubits) → replacement
_PEEPHOLE_PATTERNS: List[Tuple[Tuple[str, ...], Tuple[str, ...]]] = [
    # CX(0,1) · CX(1,0) · CX(0,1) = SWAP(0,1)
    (("cx", "cx", "cx"), ("swap",)),
]


def optimize_peephole(circuit: Circuit) -> Circuit:
    """Replace known multi-gate patterns with shorter equivalents.

    Patterns:
      CX(a,b) · CX(b,a) · CX(a,b) → SWAP(a,b)
    """
    ops = list(circuit.ops)
    out = Circuit()
    out.allocate(circuit.num_qubits)

    i = 0
    while i < len(ops):
        # Pattern: CX(a,b) · CX(b,a) · CX(a,b) = SWAP(a,b)
        if (
            i + 2 < len(ops)
            and all(isinstance(ops[i + j], GateOperation) for j in range(3))
            and ops[i].name == "cx"
            and ops[i + 1].name == "cx"
            and ops[i + 2].name == "cx"
            and ops[i].qubits == ops[i + 2].qubits  # first and third same
            and ops[i].qubits[0] == ops[i + 1].qubits[1]  # a == second's target
            and ops[i].qubits[1] == ops[i + 1].qubits[0]  # b == second's control
        ):
            a, b = ops[i].qubits
            out.add(GateOperation("swap", (a, b)))
            i += 3
        else:
            out.add(ops[i])
            i += 1
    return out


def optimize(
    circuit: Circuit,
    passes: Tuple[str, ...] = ("cancel", "commute", "cancel", "peephole"),
) -> Circuit:
    """Apply optimization passes in order.

    Available passes:
      - "cancel": remove adjacent self-inverse gate pairs
      - "commute": reorder gates to enable more cancellations
      - "peephole": replace known multi-gate patterns

    Default sequence runs cancel twice: once before commute (to remove trivial
    pairs) and once after (to cancel pairs brought together by reordering).

    Returns a new Circuit (the original is not modified).
    """
    for p in passes:
        if p == "cancel":
            circuit = optimize_cancel(circuit)
        elif p == "commute":
            circuit = optimize_commute(circuit)
        elif p == "peephole":
            circuit = optimize_peephole(circuit)
    return circuit
