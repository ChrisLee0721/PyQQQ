"""Bell state on Quantum Inspire real hardware (Tuna-9).

Generates |00> + |11> and runs it on the 9-qubit superconducting device.
Run the QX emulator first to validate the submit pipeline before using
hardware (see README).
"""

from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)

# 真机：qshow(backend="qi")；先用 QX emulator 验证提交链路：
#     from quonic.backends.qi import QuantumInspireBackend
#     QuantumInspireBackend("QX emulator").run(current_circuit(), shots=1024)
qshow(backend="qi", shots=1024)
