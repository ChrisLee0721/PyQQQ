# Bell State / Bell 态

> **Foundational** / 基础

## Overview / 概述

Create a maximally entangled state / 创建最大纠缠态

Bell state is the simplest quantum entanglement. Two qubits become correlated: measuring one instantly determines the other.

## Application / 应用场景

- Quantum teleportation (隐形传态)
- Superdense coding (超密编码)
- Quantum key distribution (量子密钥分发)
- Testing quantum hardware (测试量子硬件)

## How it works / 原理

H gate creates superposition, CX gate creates entanglement.
H 门创建叠加态，CX 门创建纠缠。

## Code / 代码

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

## Expected Output / 预期输出

Roughly 50% |00⟩ and 50% |11⟩. No |01⟩ or |10⟩ (proves entanglement).
约 50% |00⟩ 和 50% |11⟩。没有 |01⟩ 或 |10⟩（证明纠缠）。

## Run / 运行

```bash
python examples/bell/bell.py
```

## Download / 下载

[bell.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/bell/bell.py)
