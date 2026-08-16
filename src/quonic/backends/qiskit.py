"""Qiskit backend adapter."""

from __future__ import annotations

import math
from typing import Any, Optional, Union

from .._i18n import tr
from ..ir import Circuit, GateOperation
from ..noise import NoiseModel, resolve_noise
from ..result import Result
from .base import Backend


class QiskitBackend(Backend):
    name = "qiskit"
    methods = frozenset(
        {"statevector", "stabilizer", "matrix_product_state", "density_matrix"}
    )

    def run(
        self,
        circuit: Circuit,
        shots: int = 1024,
        noise: Optional[Union[NoiseModel, float, int]] = None,
        method: str = "statevector",
    ) -> Result:
        try:
            from qiskit import QuantumCircuit
            from qiskit_aer import AerSimulator
        except ImportError as e:
            raise ImportError(tr("err.qiskit_missing")) from e

        nm = resolve_noise(noise)
        qc = QuantumCircuit(circuit.num_qubits, circuit.num_qubits)
        # A named classical bit is an alias for some qubit's measurement result: map it
        # to that bit's own classical bit, so get_counts outputs a flat bitstring (with
        # no named registers) consistent with the native backend.
        creg_map = {}

        for op in circuit.ops:
            if op.name == "cif":
                # Classical control flow: measure first when control is a qubit; read the classical bit directly when it is a creg
                if isinstance(op.control, int):
                    qc.measure(op.control, op.control)
                    clbit = qc.clbits[op.control]
                else:
                    clbit = qc.clbits[creg_map.get(op.control, 0)]
                with qc.if_test((clbit, 1)):
                    self._apply(qc, op.then_op)
                with qc.if_test((clbit, 0)):
                    self._apply(qc, op.else_op)
            elif op.name == "cmeasure":
                qc.measure(op.qubit, op.qubit)
                creg_map[op.creg] = op.qubit
            elif op.name == "cwhile":
                raise NotImplementedError(tr("err.qiskit_cwhile"))
            else:
                self._apply(qc, op)

        # Auto-complete: any qubit without an explicit measure is measured at the end
        for q in circuit.unmeasured_qubits():
            qc.measure(q, q)

        # Noise simulation requires the density-matrix method; stabilizer / MPS do not support general noise models
        if nm.enabled:
            method = "density_matrix"

        simulator = AerSimulator(method=method)
        run_kwargs = {}
        if nm.enabled:
            from qiskit_aer.noise import NoiseModel as QiskitNoiseModel
            from qiskit_aer.noise import depolarizing_error

            qnm = QiskitNoiseModel()
            single_gates = ["h", "x", "y", "z", "rx", "ry", "rz"]
            double_gates = ["cx", "cz", "swap"]
            if nm.single > 0.0:
                qnm.add_all_qubit_quantum_error(
                    depolarizing_error(nm.single, 1), single_gates
                )
            if nm.double > 0.0:
                qnm.add_all_qubit_quantum_error(
                    depolarizing_error(nm.double, 2), double_gates
                )
            run_kwargs["noise_model"] = qnm

        result = simulator.run(qc, shots=shots, **run_kwargs).result()
        counts = result.get_counts()
        return Result.from_counts(counts, shots)

    @staticmethod
    def _apply(qc: Any, op: GateOperation) -> None:
        name, qubits = op.name, op.qubits
        if name == "i":
            qc.id(qubits[0])
        elif name == "h":
            qc.h(qubits[0])
        elif name == "x":
            qc.x(qubits[0])
        elif name == "y":
            qc.y(qubits[0])
        elif name == "z":
            qc.z(qubits[0])
        elif name == "cx":
            qc.cx(qubits[0], qubits[1])
        elif name == "cz":
            qc.cz(qubits[0], qubits[1])
        elif name == "ccx":
            qc.ccx(qubits[0], qubits[1], qubits[2])
        elif name == "swap":
            qc.swap(qubits[0], qubits[1])
        elif name == "mcz":
            qc.mcp(math.pi, list(qubits[:-1]), qubits[-1])
        elif name == "rx":
            qc.rx(op.params[0], qubits[0])
        elif name == "ry":
            qc.ry(op.params[0], qubits[0])
        elif name == "rz":
            qc.rz(op.params[0], qubits[0])
        elif name == "cp":
            qc.cp(op.params[0], qubits[0], qubits[1])
        elif name == "p":
            qc.p(op.params[0], qubits[0])
        elif name == "measure":
            qc.measure(qubits[0], qubits[0])
        else:
            raise ValueError(tr("err.qiskit_gate", name=name))
