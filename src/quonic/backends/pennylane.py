"""PennyLane backend adapter."""

from __future__ import annotations

from typing import Any, List, Optional, Union

from .._i18n import tr
from ..ir import Circuit, GateOperation
from ..noise import NoiseModel, resolve_noise
from ..result import Result
from .base import Backend


def _two_qubit_depolarizing_kraus(p: float) -> List[Any]:
    """The 16 Kraus operators of the two-qubit depolarizing channel (consistent with Qiskit's depolarizing_error(p, 2))."""
    import numpy as np

    I2 = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    paulis = (I2, X, Y, Z)
    kraus = [np.sqrt(1 - 15 * p / 16) * np.kron(I2, I2)]
    s = np.sqrt(p / 16)
    for a in paulis:
        for b in paulis:
            if a is I2 and b is I2:
                continue
            kraus.append(s * np.kron(a, b))
    return kraus


def _set_shots(qml: Any, qnode: Any, shots: int) -> Any:
    """Set shots across versions.

    In PennyLane 0.44+ set_shots is a transform (set_shots(qnode, shots=...));
    in earlier versions (0.36–0.42) it is a decorator (@set_shots(shots=...)). Older
    versions support Python 3.9/3.10 while newer ones require 3.11+, so we do runtime
    compatibility here.
    """
    try:
        return qml.set_shots(qnode, shots=shots)
    except TypeError:
        return qml.set_shots(shots=shots)(qnode)


class PennyLaneBackend(Backend):
    name = "pennylane"
    methods = frozenset({"statevector"})

    def run(
        self,
        circuit: Circuit,
        shots: int = 1024,
        noise: Optional[Union[NoiseModel, float, int]] = None,
        method: str = "statevector",
    ) -> Result:
        try:
            import pennylane as qml
        except ImportError as e:
            raise ImportError(tr("err.pennylane_missing")) from e

        nm = resolve_noise(noise)
        n = circuit.num_qubits
        device_name = "default.mixed" if nm.enabled else "default.qubit"
        dev = qml.device(device_name, wires=n)

        two_qubit_kraus = None
        if nm.enabled and nm.double > 0.0:
            two_qubit_kraus = _two_qubit_depolarizing_kraus(nm.double)

        @qml.qnode(dev)
        def qnode() -> Any:
            for op in circuit.ops:
                self._apply(qml, op)
                if nm.enabled and op.name != "measure":
                    if len(op.qubits) == 1 and nm.single > 0.0:
                        qml.DepolarizingChannel(nm.single, wires=op.qubits[0])
                    elif len(op.qubits) == 2 and two_qubit_kraus is not None:
                        qml.QubitChannel(two_qubit_kraus, wires=list(op.qubits))
            return qml.counts()

        qnode = _set_shots(qml, qnode, shots)

        raw = qnode()
        # PennyLane's bitstring has wire0 at the most significant position; reverse it to the Qiskit convention (qubit0 at the least significant position)
        counts = {}
        for bitstring, count in raw.items():
            key = str(bitstring)[::-1]
            counts[key] = counts.get(key, 0) + count
        return Result.from_counts(counts, shots)

    @staticmethod
    def _apply(qml: Any, op: GateOperation) -> None:
        name, qubits = op.name, op.qubits
        if name == "i":
            qml.Identity(wires=qubits[0])
        elif name == "h":
            qml.Hadamard(wires=qubits[0])
        elif name == "x":
            qml.PauliX(wires=qubits[0])
        elif name == "y":
            qml.PauliY(wires=qubits[0])
        elif name == "z":
            qml.PauliZ(wires=qubits[0])
        elif name == "cx":
            qml.CNOT(wires=[qubits[0], qubits[1]])
        elif name == "cz":
            qml.CZ(wires=[qubits[0], qubits[1]])
        elif name == "ccx":
            qml.Toffoli(wires=[qubits[0], qubits[1], qubits[2]])
        elif name == "swap":
            qml.SWAP(wires=[qubits[0], qubits[1]])
        elif name == "mcz":
            target = qubits[-1]
            qml.Hadamard(wires=target)
            qml.MultiControlledX(wires=list(qubits))
            qml.Hadamard(wires=target)
        elif name == "rx":
            qml.RX(op.params[0], wires=qubits[0])
        elif name == "ry":
            qml.RY(op.params[0], wires=qubits[0])
        elif name == "rz":
            qml.RZ(op.params[0], wires=qubits[0])
        elif name == "cp":
            qml.ControlledPhaseShift(op.params[0], wires=[qubits[0], qubits[1]])
        elif name == "p":
            qml.PhaseShift(op.params[0], wires=qubits[0])
        elif name == "measure":
            return  # qml.counts() measures all wires, so an explicit measure needs no extra operation
        elif name in ("cif", "cmeasure", "cwhile"):
            raise NotImplementedError(tr("err.pennylane_ctrl"))
        else:
            raise ValueError(tr("err.pennylane_gate", name=name))
