# Gates API

QuoNic's gate system: pre-defined gate instances and parameterized gate factories.

## Pre-defined Gates / 预定义门

### Single-qubit / 单量子比特

| Gate | Matrix | Description |
|------|--------|-------------|
| `H` | Hadamard | Creates superposition (创建叠加态) |
| `X` | Pauli-X | Bit flip (比特翻转) |
| `Y` | Pauli-Y | Bit+phase flip (比特+相位翻转) |
| `Z` | Pauli-Z | Phase flip (相位翻转) |
| `I` | Identity | No operation (恒等操作) |

### Multi-qubit / 多量子比特

| Gate | Description |
|------|-------------|
| `CX` | Controlled-NOT (受控非门) |
| `CZ` | Controlled-Z (受控 Z 门) |
| `CCX` | Toffoli (Toffoli 门) |
| `SWAP` | Swap two qubits (交换两个量子比特) |

## Parameterized Gates / 参数化门

### Rx(θ), Ry(θ), Rz(θ)

Rotation gates around X, Y, Z axes.

绕 X、Y、Z 轴的旋转门。

```python
from quonic import qgate
from quonic.gates import Rx, Ry, Rz

qgate(Rx(3.14159), 0)  # π rotation around X
qgate(Ry(1.5708), 1)   # π/2 rotation around Y
qgate(Rz(0.7854), 2)   # π/4 rotation around Z
```

### CP(θ) — Controlled Phase

Controlled phase rotation. Used in QFT.

受控相位旋转。用于 QFT。

```python
from quonic.gates import CP

qgate(CP(1.5708), 0, 1)  # Controlled π/4 phase
```

## Gate Resolution / 门解析

`resolve()` converts string names to Gate objects. Supports fuzzy matching.

`resolve()` 将字符串名称转换为 Gate 对象。支持模糊匹配。

```python
from quonic.gates import resolve

resolve("h")          # → H gate
resolve("cnot")       # → CX gate (via alias)
resolve("hadamard")   # → H gate (via alias)
resolve("haddamard")  # → ValueError: Did you mean 'h'?
```

## Custom Gates / 自定义门

Create gates from matrices / 从矩阵创建门：

```python
from quonic.gates import Gate
import numpy as np

# Custom T gate
T_matrix = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
T = Gate("t", T_matrix, 1)
qgate(T, 0)
```

## Examples / 示例

### Bell state / Bell 态

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

### Rotation chain / 旋转链

```python
from quonic import qgate, qshow
from quonic.gates import CX, Ry

for i in range(4):
    qgate(Ry(0.5 * i), i)
    if i < 3:
        qgate(CX, i, i + 1)
qshow()
```
