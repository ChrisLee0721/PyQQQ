"""ZX-calculus optimization: circuit ↔ ZX-graph conversion and simplification.

Implements the core ZX-calculus rewrite rules:
1. Spider fusion: merge adjacent same-type spiders
2. Identity removal: remove 0-phase spiders with ≤ 2 neighbors
3. H-edge elimination: remove Hadamard edges between same-type spiders
4. Supplementarity: if two spiders of opposite type share all neighbors, simplify
5. Circuit extraction: convert simplified ZX-graph back to a circuit

Example::

    from quonic.zx import circuit_to_zx, optimize_zx, extract_circuit

    graph = circuit_to_zx(circuit)
    simplified = optimize_zx(graph)
    optimized = extract_circuit(simplified)
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from ..ir import Circuit, GateOperation
from .graph import SpiderType, ZXEdge, ZXGraph


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

    inputs = []
    outputs = []
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
                s = g.add_spider(stype, phase)
                g.add_edge(current[q], s)
                current[q] = s
            elif name == "h":
                s = g.add_spider(SpiderType.Z, 0.0)
                g.add_edge(current[q], s, hadamard=True)
                current[q] = s

        elif len(qubits) == 2:
            c, t = qubits
            if name == "cx":
                s_ctrl = g.add_spider(SpiderType.Z, 0.0)
                s_tgt = g.add_spider(SpiderType.X, 0.0)
                g.add_edge(current[c], s_ctrl)
                g.add_edge(current[t], s_tgt)
                g.add_edge(s_ctrl, s_tgt)
                current[c] = s_ctrl
                current[t] = s_tgt
            elif name == "cz":
                s1 = g.add_spider(SpiderType.Z, 0.0)
                s2 = g.add_spider(SpiderType.Z, 0.0)
                g.add_edge(current[c], s1)
                g.add_edge(current[t], s2)
                g.add_edge(s1, s2, hadamard=True)
                current[c] = s1
                current[t] = s2
            elif name == "swap":
                current[c], current[t] = current[t], current[c]

    for q in range(n):
        out = g.add_spider(SpiderType.BOUNDARY)
        g.add_edge(current[q], out)
        outputs.append(out)

    g.set_inputs(inputs)
    g.set_outputs(outputs)
    return g


def optimize_zx(graph: ZXGraph, max_rounds: int = 10) -> ZXGraph:
    """Simplify a ZX-graph using rewrite rules.

    Applies spider fusion, identity removal, H-edge elimination,
    and supplementarity until no more simplifications are possible.

    Args:
        graph: input ZX-graph
        max_rounds: maximum number of simplification rounds

    Returns:
        Simplified ZX-graph.
    """
    g = graph.copy()

    for _ in range(max_rounds):
        changed = False
        changed |= _fuse_spiders(g)
        changed |= _remove_identities(g)
        changed |= _eliminate_h_edges(g)
        changed |= _supplementarity(g)
        if not changed:
            break

    return g


def extract_circuit(graph: ZXGraph) -> Circuit:
    """Extract a quantum circuit from a simplified ZX-graph.

    Traverses the graph from inputs to outputs, emitting gates for each
    non-boundary spider. Handles both Z-type and X-type spiders, and
    entangling edges (regular and Hadamard).

    Args:
        graph: simplified ZX-graph

    Returns:
        Extracted Circuit.
    """
    n = len(graph.inputs)
    c = Circuit()
    c.allocate(n)

    # Track which spiders have been processed
    processed = set()

    for q_idx, inp_id in enumerate(graph.inputs):
        current = inp_id
        visited = {current}

        while True:
            nbs = graph.neighbors(current)
            next_sp = None
            for nb in nbs:
                if nb not in visited:
                    next_sp = nb
                    break

            if next_sp is None:
                break

            visited.add(next_sp)
            s = graph.spiders.get(next_sp)

            if s is None or s.stype == SpiderType.BOUNDARY:
                current = next_sp
                continue

            # Emit gate for this spider (only if not already processed)
            if next_sp not in processed:
                processed.add(next_sp)
                if abs(s.phase) > 1e-10:
                    if s.stype == SpiderType.Z:
                        c.add(GateOperation("rz", (q_idx,), (s.phase,)))
                    elif s.stype == SpiderType.X:
                        c.add(GateOperation("rx", (q_idx,), (s.phase,)))

            # Check for entangling edges
            for nb in graph.neighbors(next_sp):
                if nb in visited:
                    continue
                nb_sp = graph.spiders.get(nb)
                if nb_sp is not None and nb_sp.stype != SpiderType.BOUNDARY:
                    target_q = _find_qubit_for_spider(graph, nb, graph.inputs)
                    if target_q is not None and target_q != q_idx:
                        edge = _find_edge(graph, next_sp, nb)
                        if edge and edge.hadamard:
                            c.add(GateOperation("cz", (q_idx, target_q)))
                        else:
                            # CX: Z-spider connected to X-spider
                            if s.stype == SpiderType.Z and nb_sp.stype == SpiderType.X:
                                c.add(GateOperation("cx", (q_idx, target_q)))
                            elif s.stype == SpiderType.X and nb_sp.stype == SpiderType.Z:
                                c.add(GateOperation("cx", (target_q, q_idx)))
                            else:
                                c.add(GateOperation("cz", (q_idx, target_q)))

            current = next_sp

    return c


def _find_qubit_for_spider(graph: ZXGraph, sid: int, inputs: list) -> Optional[int]:
    """Find which qubit a spider belongs to by tracing back to an input."""
    visited = {sid}
    queue = [sid]
    while queue:
        current = queue.pop(0)
        for nb in graph.neighbors(current):
            if nb in inputs:
                return inputs.index(nb)
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return None


def _find_edge(graph: ZXGraph, s1: int, s2: int) -> Optional[ZXEdge]:
    """Find the edge between two spiders."""
    for e in graph.edges:
        if (e.src == s1 and e.dst == s2) or (e.src == s2 and e.dst == s1):
            return e
    return None


# ---------------------------------------------------------------------------
# Rewrite rules
# ---------------------------------------------------------------------------


def _fuse_spiders(g: ZXGraph) -> bool:
    """Merge adjacent same-type spiders."""
    changed = False
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


def _eliminate_h_edges(g: ZXGraph) -> bool:
    """Eliminate Hadamard edges between same-type spiders.

    Rule: If two same-type spiders are connected by an H-edge, and one has
    phase 0, the H-edge can be removed.
    """
    changed = False
    for eidx, e in enumerate(g.edges):
        if e.src == -1 or not e.hadamard:
            continue
        s1 = g.spiders.get(e.src)
        s2 = g.spiders.get(e.dst)
        if s1 is None or s2 is None:
            continue
        if s1.stype != s2.stype:
            continue
        if s1.stype == SpiderType.BOUNDARY:
            continue

        if abs(s1.phase) < 1e-10 or abs(s2.phase) < 1e-10:
            e.hadamard = False
            changed = True

    return changed


def _supplementarity(g: ZXGraph) -> bool:
    """Supplementarity rule: if a Z-spider and X-spider share all neighbors
    and have complementary phases, both can be removed.

    Rule: Z(α) and X(β) connected, sharing the same neighbor set N.
    If α + β = 0 (mod 2π), remove both spiders. The neighbors in N are
    already connected through the graph structure.
    """
    changed = False

    for eidx, e in enumerate(g.edges):
        if e.src == -1:
            continue
        s1 = g.spiders.get(e.src)
        s2 = g.spiders.get(e.dst)
        if s1 is None or s2 is None:
            continue
        if s1.stype == SpiderType.BOUNDARY or s2.stype == SpiderType.BOUNDARY:
            continue
        if s1.stype == s2.stype:
            continue

        # Get neighbors excluding each other
        nbs1 = set(g.neighbors(e.src)) - {e.dst}
        nbs2 = set(g.neighbors(e.dst)) - {e.src}

        # Same neighbors and complementary phases
        if nbs1 == nbs2 and abs(s1.phase + s2.phase) % (2 * np.pi) < 1e-10:
            # Connect each pair of shared neighbors directly
            nbs_list = list(nbs1)
            for i in range(len(nbs_list)):
                for j in range(i + 1, len(nbs_list)):
                    # Check if edge already exists
                    existing = False
                    for e2 in g.edges:
                        if e2.src == -1:
                            continue
                        if (e2.src == nbs_list[i] and e2.dst == nbs_list[j]) or \
                           (e2.src == nbs_list[j] and e2.dst == nbs_list[i]):
                            existing = True
                            break
                    if not existing:
                        g.add_edge(nbs_list[i], nbs_list[j])
            g.remove_spider(e.src)
            g.remove_spider(e.dst)
            changed = True
            break

    return changed


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
        return np.pi
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
