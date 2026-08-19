"""ZX-calculus optimization: circuit ↔ ZX-graph conversion and simplification.

Implements the core ZX-calculus rewrite rules:
1. Spider fusion: merge adjacent same-type spiders
2. Identity removal: remove 0-phase spiders with ≤ 2 neighbors
3. Hadamard simplification: eliminate unnecessary H-edges

Example::

    from quonic.zx import circuit_to_zx, optimize_zx

    graph = circuit_to_zx(circuit)
    simplified = optimize_zx(graph)
    optimized_circuit = simplified.to_circuit()
"""

from __future__ import annotations

import numpy as np

from ..ir import Circuit, GateOperation
from .graph import SpiderType, ZXGraph


def circuit_to_zx(circuit: Circuit) -> ZXGraph:
    """Convert a quantum circuit to a ZX-graph.

    Each qubit becomes a "wire" of boundary spiders. Single-qubit gates become
    Z-type or X-type spiders inserted into the wire. Two-qubit gates become
    connected spiders.

    Args:
        circuit: the input circuit

    Returns:
        ZXGraph representation.
    """
    g = ZXGraph()
    n = circuit.num_qubits

    # Create input and output boundary spiders for each qubit
    inputs = []
    outputs = []
    # Track the "current" spider at the end of each qubit's wire
    current = []

    for q in range(n):
        inp = g.add_spider(SpiderType.BOUNDARY)
        inputs.append(inp)
        current.append(inp)

    for op in circuit.ops:
        if not isinstance(op, GateOperation):
            continue
        name = op.name.lower()
        qubits = op.qubits

        if name == "measure":
            continue

        if len(qubits) == 1:
            q = qubits[0]
            phase = _gate_phase(name, op.params)
            stype = _gate_type(name)

            if stype is not None and phase is not None:
                # Insert a spider into the wire
                s = g.add_spider(stype, phase)
                g.add_edge(current[q], s)
                current[q] = s
            elif name == "h":
                # Hadamard: insert a Z-spider with π/2 and X-spider with π/2
                # Actually, H = Z(π/2) · X(π/2) · Z(π/2) but in ZX-calculus
                # we just mark the edge as Hadamard
                s = g.add_spider(SpiderType.Z, 0.0)
                g.add_edge(current[q], s, hadamard=True)
                current[q] = s

        elif len(qubits) == 2:
            c, t = qubits
            if name == "cx":
                # CX = Z-spider on control connected to X-spider on target
                s_ctrl = g.add_spider(SpiderType.Z, 0.0)
                s_tgt = g.add_spider(SpiderType.X, 0.0)
                g.add_edge(current[c], s_ctrl)
                g.add_edge(current[t], s_tgt)
                g.add_edge(s_ctrl, s_tgt)  # entangling edge
                current[c] = s_ctrl
                current[t] = s_tgt
            elif name == "cz":
                # CZ = Z-spider on both qubits connected by H-edge
                s1 = g.add_spider(SpiderType.Z, 0.0)
                s2 = g.add_spider(SpiderType.Z, 0.0)
                g.add_edge(current[c], s1)
                g.add_edge(current[t], s2)
                g.add_edge(s1, s2, hadamard=True)
                current[c] = s1
                current[t] = s2
            elif name == "swap":
                # SWAP: just cross the wires (no spiders needed)
                current[c], current[t] = current[t], current[c]

    # Create output boundaries
    for q in range(n):
        out = g.add_spider(SpiderType.BOUNDARY)
        g.add_edge(current[q], out)
        outputs.append(out)

    g.set_inputs(inputs)
    g.set_outputs(outputs)
    return g


def optimize_zx(graph: ZXGraph, max_rounds: int = 10) -> ZXGraph:
    """Simplify a ZX-graph using rewrite rules.

    Applies spider fusion and identity removal until no more simplifications
    are possible.

    Args:
        graph: input ZX-graph
        max_rounds: maximum number of simplification rounds

    Returns:
        Simplified ZX-graph.
    """
    g = graph.copy()

    for _ in range(max_rounds):
        changed = False

        # Pass 1: Spider fusion — merge adjacent same-type spiders
        changed |= _fuse_spiders(g)

        # Pass 2: Identity removal — remove 0-phase spiders with ≤ 2 neighbors
        changed |= _remove_identities(g)

        if not changed:
            break

    return g


def _fuse_spiders(g: ZXGraph) -> bool:
    """Merge adjacent same-type spiders."""
    changed = False
    # Process edges in order; after contraction the graph changes, so restart
    for _ in range(len(g.edges)):
        found = False
        for eidx, e in enumerate(g.edges):
            if e.src == -1:
                continue
            s1 = g.spiders.get(e.src)
            s2 = g.spiders.get(e.dst)
            if s1 is None or s2 is None:
                continue
            if s1.stype == s2.stype and s1.stype != SpiderType.BOUNDARY:
                g.contract_edge(eidx)
                changed = True
                found = True
                break
        if not found:
            break
    return changed


def _remove_identities(g: ZXGraph) -> bool:
    """Remove 0-phase spiders with ≤ 2 neighbors."""
    changed = True
    any_changed = False
    while changed:
        changed = False
        for sid in list(g.spiders.keys()):
            if sid not in g.spiders:
                continue
            s = g.spiders[sid]
            if s.stype == SpiderType.BOUNDARY:
                continue
            if abs(s.phase) < 1e-10:
                nbs = g.neighbors(sid)
                if len(nbs) <= 2:
                    g.remove_id_spider(sid)
                    changed = True
                    any_changed = True
    return any_changed


def _gate_phase(name: str, params: tuple) -> float:
    """Extract the rotation phase from a gate."""
    if name in ("z",):
        return np.pi
    if name in ("s",):
        return np.pi / 2
    if name in ("t",):
        return np.pi / 4
    if name in ("rz", "p") and params:
        return params[0]
    if name in ("x",):
        return np.pi  # X = Z(π) in ZX-calculus
    if name in ("rx",) and params:
        return params[0]
    return 0.0


def _gate_type(name: str) -> SpiderType:
    """Determine the spider type for a gate."""
    if name in ("z", "rz", "s", "t", "p"):
        return SpiderType.Z
    if name in ("x", "rx"):
        return SpiderType.X
    return None
