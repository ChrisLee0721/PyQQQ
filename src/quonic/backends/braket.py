"""AWS Braket backend adapter.

⚠️  UNTESTED: This backend has not been tested on real hardware.
   Code is provided as-is. Use at your own risk.

Submits circuits to Amazon Braket (SV1, TN1, DM1 simulators or real hardware).

Prerequisites:
    pip install 'quonic[braket]'
    # or: pip install amazon-braket-sdk

Usage:
    qshow(backend='braket', device='arn:aws:braket:...:device/quantum-simulator/amazon/sv1')
"""

from __future__ import annotations

from typing import Any, Optional, Union

from .._i18n import tr
from ..ir import Circuit
from ..noise import NoiseModel
from ..result import Result
from .base import Backend


class BraketBackend(Backend):
    name = "braket"
    methods = frozenset({"statevector", "density_matrix"})
    _CAPABILITIES = {"noise": False, "ctrl": False, "mid_measure": False, "gpu": False}

    def __init__(self, device: str = "arn:aws:braket:::device/quantum-simulator/amazon/sv1") -> None:
        self.device = device

    def run(
        self,
        circuit: Circuit,
        shots: int = 1024,
        noise: Optional[Union[NoiseModel, float, int]] = None,
        method: str = "statevector",
        return_state: bool = False,
    ) -> Any:
        if noise is not None:
            raise ValueError(tr("err.braket_noise"))
        if return_state:
            raise NotImplementedError(tr("err.engine_no_sv", name=self.name))

        try:
            from braket.aws import AwsDevice
            from braket.circuits import Circuit as BraketCircuit
            from braket.circuits import gates as BG
        except ImportError as e:
            raise ImportError(tr("err.braket_missing")) from e

        # Build Braket circuit
        bc = BraketCircuit()
        for op in circuit.ops:
            if op.name == "measure":
                continue
            _translate_gate(bc, BG, op)

        # Auto-measure all qubits
        for q in range(circuit.num_qubits):
            bc.measure(q)

        # Submit to Braket
        device = AwsDevice(self.device)
        task = device.run(bc, shots=shots)
        result = task.result()
        counts = result.measurement_counts

        return Result.from_counts(counts, shots)


def _translate_gate(bc, BG, op):
    """Translate a QuoNic gate to a Braket gate."""
    name = op.name
    q = op.qubits

    if name == "h":
        bc.h(q[0])
    elif name == "x":
        bc.x(q[0])
    elif name == "y":
        bc.y(q[0])
    elif name == "z":
        bc.z(q[0])
    elif name == "cx":
        bc.cnot(q[0], q[1])
    elif name == "cz":
        bc.cz(q[0], q[1])
    elif name == "rx":
        bc.rx(q[0], op.params[0])
    elif name == "ry":
        bc.ry(q[0], op.params[0])
    elif name == "rz":
        bc.rz(q[0], op.params[0])
    elif name == "swap":
        bc.swap(q[0], q[1])
    elif name == "ccx":
        bc.ccx(q[0], q[1], q[2])
    elif name == "measure":
        pass
    else:
        raise ValueError(tr("err.braket_gate", name=name))
