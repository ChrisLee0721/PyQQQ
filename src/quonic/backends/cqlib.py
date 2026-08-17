"""Cqlib backend adapter."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from .._i18n import tr
from ..noise import NoiseModel
from .engine import EngineBackend


class CqlibBackend(EngineBackend):
    name = "cqlib"
    _MISSING_ERR = "err.cqlib_missing"
    _GATE_ERR = "err.cqlib_gate"
    methods = frozenset({"statevector", "density_matrix"})

    # ------------------------------------------------------------------ #
    #  Statevector path (v1, unchanged)
    # ------------------------------------------------------------------ #

    def _create(self, n: int) -> Any:
        try:
            from cqlib import Circuit
        except ImportError as e:
            raise ImportError(tr(self._MISSING_ERR)) from e
        return Circuit(n)

    def _apply_one(
        self, engine: Any, name: str, qubits: list[int], params: Tuple[float, ...]
    ) -> None:
        if name == "identity":
            pass
        elif name == "h":
            engine.h(qubits[0])
        elif name == "x":
            engine.x(qubits[0])
        elif name == "y":
            engine.y(qubits[0])
        elif name == "z":
            engine.z(qubits[0])
        elif name == "cx":
            engine.cx(qubits[0], qubits[1])
        elif name == "cz":
            engine.cz(qubits[0], qubits[1])
        elif name == "swap":
            engine.swap(qubits[0], qubits[1])
        elif name == "ccx":
            engine.ccx(qubits[0], qubits[1], qubits[2])
        elif name == "rx":
            engine.rx(qubits[0], params[0])
        elif name == "ry":
            engine.ry(qubits[0], params[0])
        elif name == "rz":
            engine.rz(qubits[0], params[0])
        elif name == "p":
            engine.u1(qubits[0], params[0])
        elif name == "cp":
            engine.cp(qubits[0], qubits[1], params[0])
        elif name == "mcz":
            self._apply_mcz(engine, qubits)
        elif name == "measure":
            pass
        else:
            raise ValueError(tr(self._GATE_ERR, name=name))

    @staticmethod
    def _apply_mcz(engine: Any, qubits: list[int]) -> None:
        if len(qubits) == 2:
            engine.cz(qubits[0], qubits[1])
        else:
            target = qubits[-1]
            engine.h(target)
            for c in qubits[:-1]:
                engine.cx(c, target)
            engine.h(target)

    def _sample(self, engine: Any, shots: int, n: int) -> Dict[str, int]:
        """Cqlib is a circuit construction library for cloud execution.
        Local simulation is not supported — use TianYanPlatform for cloud execution.
        """
        raise NotImplementedError(
            "cqlib does not have a local simulator; use TianYanPlatform for cloud execution"
        )

    # ------------------------------------------------------------------ #
    #  Density-matrix path (v2)
    # ------------------------------------------------------------------ #

    def _sample_dm(self, engine: Any, shots: int, n: int) -> Dict[str, int]:
        """Cqlib has no local simulator."""
        raise NotImplementedError(
            "cqlib does not have a local simulator; use TianYanPlatform for cloud execution"
        )

    def _apply_noise_after_gate(
        self, engine: Any, qubits: list[int], nm: NoiseModel
    ) -> None:
        """Cqlib noise injection — uses native depolarizing if available."""
        p = nm.single if len(qubits) == 1 else nm.double
        if p > 0:
            for q in qubits:
                # Cqlib may expose depolarizing as a method on the circuit
                if hasattr(engine, "depolarizing"):
                    engine.depolarizing(q, p)

    def _measure_qubit(self, engine: Any, qubit: int) -> int:
        """Mid-circuit measurement — manual probability extraction."""
        import numpy as np

        if hasattr(engine, "get_probability"):
            prob = engine.get_probability(qubit, 1)
            return 1 if np.random.random() < prob else 0
        # Fallback: run statevector, compute P(1)
        raw = engine.sample(1)
        bs = next(iter(raw))
        return int(bs[qubit]) if isinstance(bs, str) else int(bs)
