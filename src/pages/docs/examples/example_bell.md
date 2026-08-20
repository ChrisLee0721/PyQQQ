# Bell State / Bell 态

> **Foundational** / 基础

## Overview / 概述

Create a maximally entangled state — the simplest quantum entanglement.

创建最大纠缠态——最简单的量子纠缠。

## Application / 应用场景

- Quantum teleportation (隐形传态)
- Superdense coding (超密编码)
- Quantum key distribution (量子密钥分发)
- Testing quantum hardware (测试量子硬件)
- EPR paradox demonstration (EPR 悖论演示)

## How it works / 原理

Two gates create entanglement / 两个门创建纠缠：

```
|0⟩ ─H──●──  →  (|00⟩ + |11⟩) / √2
|0⟩ ────X──
```

**Step 1**: H gate puts qubit 0 in superposition: (|0⟩ + |1⟩)/√2
H 门将量子比特 0 置于叠加态：(|0⟩ + |1⟩)/√2

**Step 2**: CX gate entangles qubit 1 with qubit 0
CX 门将量子比特 1 与量子比特 0 纠缠

**Result**: Measuring one qubit instantly determines the other
结果：测量一个量子比特立即确定另一个

## Why it's special / 为什么特殊

Bell state violates Bell's inequality — proving quantum mechanics is non-local.

Bell 态违反 Bell 不等式——证明量子力学是非局域的。

```
Classical limit: S ≤ 2
Quantum (Bell):  S = 2√2 ≈ 2.83
```

This means **no local hidden variable theory** can explain quantum correlations.

这意味着**没有局域隐变量理论**能解释量子关联。

## Code / 代码

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)      # Superposition / 叠加态
qgate(CX, 0, 1)  # Entanglement / 纠缠
qshow()
```

## Expected Output / 预期输出

Roughly 50% |00⟩ and 50% |11⟩. **No |01⟩ or |10⟩** — this proves entanglement.

约 50% |00⟩ 和 50% |11⟩。**没有 |01⟩ 或 |10⟩**——这证明了纠缠。

```
backend: native | shots: 1024
Result:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################
```

If the qubits were independent, you'd see |01⟩ and |10⟩ too. Their absence proves correlation.

如果量子比特是独立的，你会看到 |01⟩ 和 |10⟩。它们的缺失证明了关联。

## All 4 Bell states / 全部 4 个 Bell 态

| State | Circuit | Notation |
|-------|---------|----------|
| Φ⁺ | H, CX | (\|00⟩ + \|11⟩)/√2 |
| Φ⁻ | H, X, CX | (\|00⟩ - \|11⟩)/√2 |
| Ψ⁺ | H, CX, X | (\|01⟩ + \|10⟩)/√2 |
| Ψ⁻ | H, X, CX, X | (\|01⟩ - \|10⟩)/√2 |

## Run / 运行

```bash
python examples/bell/bell.py
```

## Download / 下载

[bell.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/bell/bell.py)
