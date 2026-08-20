"""Quantum Inspire backend / Quantum Inspire 后端

Quantum Inspire backend / Quantum Inspire 后端

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)

# 真机：qshow(backend="qi")；先用 QX emulator 验证提交链路：
#     from quonic.backends.qi import QuantumInspireBackend
#     QuantumInspireBackend("QX emulator").run(current_circuit(), shots=1024)
qshow(backend="qi", shots=1024)
