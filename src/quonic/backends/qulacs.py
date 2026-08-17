"""Qulacs backend adapter."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from .._i18n import tr
from ..noise import NoiseModel
from .engine import EngineBackend


class QulacsBackend(EngineBackend):
    name = "qulacs"
    _MISSING_ERR = "err.qulacs_missing"
    _GATE_ERR = "err.qulacs_gate"
    methods = frozenset({"statevector", "density_matrix"})

    # ------------------------------------------------------------------ #
    #  Statevector path (v1)
    # ------------------------------------------------------------------ #

    def _create(self, n: int) -> Any:
        try:
            import qulacs
        except ImportError as e:
            raise ImportError(tr(self._MISSING_ERR)) from e
        return qulacs.QuantumCircuit(n)

    def _apply_one(
        self, engine: Any, name: str, qubits: list[int], params: Tuple[float, ...]
    ) -> None:
        from qulacs import gate

        if name in ("identity", "i"):
            engine.add_gate(gate.Identity(qubits[0]))
        elif name == "h":
            engine.add_gate(gate.H(qubits[0]))
        elif name == "x":
            engine.add_gate(gate.X(qubits[0]))
        elif name == "y":
            engine.add_gate(gate.Y(qubits[0]))
        elif name == "z":
            engine.add_gate(gate.Z(qubits[0]))
        elif name == "cx":
            engine.add_gate(gate.CNOT(qubits[0], qubits[1]))
        elif name == "cz":
            engine.add_gate(gate.CZ(qubits[0], qubits[1]))
        elif name == "swap":
            engine.add_gate(gate.SWAP(qubits[0], qubits[1]))
        elif name == "ccx":
            engine.add_gate(gate.TOFFOLI(qubits[0], qubits[1], qubits[2]))
        elif name == "rx":
            engine.add_gate(gate.RX(qubits[0], params[0]))
        elif name == "ry":
            engine.add_gate(gate.RY(qubits[0], params[0]))
        elif name == "rz":
            engine.add_gate(gate.RZ(qubits[0], params[0]))
        elif name == "p":
            # P(θ) = diag(1, e^{iθ}) — use DenseMatrix for exact implementation
            import numpy as np

            mat = np.array([[1.0, 0.0], [0.0, np.exp(1j * params[0])]])
            engine.add_gate(gate.DenseMatrix(qubits[0], mat))
        elif name == "cp":
            # CP(θ) = diag(1, 1, 1, e^{iθ}) — decompose into CNOT + P + CNOT
            import numpy as np

            p_mat = np.array([[1.0, 0.0], [0.0, np.exp(1j * params[0])]])
            engine.add_gate(gate.CNOT(qubits[0], qubits[1]))
            engine.add_gate(gate.DenseMatrix(qubits[1], p_mat))
            engine.add_gate(gate.CNOT(qubits[0], qubits[1]))
        elif name == "mcz":
            self._apply_mcz(engine, qubits)
        elif name == "measure":
            pass  # handled in _sample
        else:
            raise ValueError(tr(self._GATE_ERR, name=name))

    @staticmethod
    def _apply_mcz(engine: Any, qubits: list[int]) -> None:
        from qulacs import gate

        if len(qubits) == 2:
            engine.add_gate(gate.CZ(qubits[0], qubits[1]))
        elif len(qubits) == 3:
            engine.add_gate(gate.TOFFOLI(qubits[0], qubits[1], qubits[2]))
            engine.add_gate(gate.Z(qubits[2]))
            engine.add_gate(gate.TOFFOLI(qubits[0], qubits[1], qubits[2]))
        else:
            n = len(qubits)
            target = qubits[-1]
            engine.add_gate(gate.H(target))
            for i in range(n - 1):
                engine.add_gate(gate.CNOT(qubits[i], target))
            engine.add_gate(gate.H(target))

    def _sample(self, engine: Any, shots: int, n: int) -> Dict[str, int]:
        from qulacs import QuantumState

        state = QuantumState(n)
        engine.update_quantum_state(state)
        raw = state.sampling(shots)
        counts: Dict[str, int] = {}
        for val in raw:
            bs = format(val, f"0{n}b")[::-1]
            counts[bs] = counts.get(bs, 0) + 1
        return counts

    # ------------------------------------------------------------------ #
    #  Density-matrix path (v2)
    # ------------------------------------------------------------------ #

    def _create_dm(self, n: int) -> Any:
        """Create a (circuit, density_matrix) tuple."""
        try:
            import qulacs
        except ImportError as e:
            raise ImportError(tr(self._MISSING_ERR)) from e
        return (qulacs.QuantumCircuit(n), qulacs.DensityMatrix(n))

    def _apply_one_dm(
        self, engine: Any, name: str, qubits: list[int], params: Tuple[float, ...]
    ) -> None:
        circuit, _dm = engine
        self._apply_one(circuit, name, qubits, params)

    def _sample_dm(self, engine: Any, shots: int, n: int) -> Dict[str, int]:
        circuit, dm = engine
        dm.set_zero_state()
        circuit.update_quantum_state(dm)
        raw = dm.sampling(shots)
        counts: Dict[str, int] = {}
        for val in raw:
            bs = format(val, f"0{n}b")[::-1]
            counts[bs] = counts.get(bs, 0) + 1
        return counts

    def _apply_noise_after_gate(
        self, engine: Any, qubits: list[int], nm: NoiseModel
    ) -> None:
        from qulacs import gate

        circuit, _dm = engine
        p = nm.single if len(qubits) == 1 else nm.double
        if p > 0:
            for q in qubits:
                circuit.add_gate(gate.DepolarizingNoise(q, p))

    def _measure_qubit(self, engine: Any, qubit: int) -> int:
        """Mid-circuit measurement: compute P(1) from statevector or density matrix."""
        import numpy as np

        from qulacs import QuantumState

        # Handle both tuple (circuit, dm) and plain circuit
        if isinstance(engine, tuple):
            circuit, dm = engine
            n = dm.get_qubit_count()
            # Execute circuit on density matrix to get current state
            dm.set_zero_state()
            circuit.update_quantum_state(dm)
            data = dm.get_matrix()
            diag = np.real(np.diag(data))
        else:
            # Plain QuantumCircuit — use statevector
            n = engine.get_qubit_count()
            state = QuantumState(n)
            engine.update_quantum_state(state)
            sv = state.get_vector()
            diag = np.abs(sv) ** 2

        idx = np.arange(2**n)
        bit = (idx >> qubit) & 1
        p0 = float(np.sum(diag[bit == 0]))
        return 0 if np.random.random() < p0 else 1
