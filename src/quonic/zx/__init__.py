"""ZX-calculus: graphical rewrite framework for quantum circuit optimization.

ZX-graphs represent quantum circuits as graphs of "spiders" (Z-type or X-type)
connected by edges. Rewrite rules simplify the graph without changing the
computed unitary, enabling circuit optimization beyond gate-level passes.

Example::

    from quonic.zx import ZXGraph, circuit_to_zx, optimize_zx

    graph = circuit_to_zx(circuit)
    simplified = optimize_zx(graph)
    optimized = simplified.to_circuit()
"""

from .graph import ZXGraph, ZXSpider
from .optimize import circuit_to_zx, extract_circuit, optimize_zx

__all__ = [
    "ZXGraph",
    "ZXSpider",
    "circuit_to_zx",
    "extract_circuit",
    "optimize_zx",
]
