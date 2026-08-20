# Quantum Phase Estimation / 量子相位估计

> **Algorithms** / 算法

## Overview / 概述

Estimate the eigenvalue of a unitary operator. Foundation for Shor's algorithm and quantum chemistry.

估计酉算子的本征值。是 Shor 算法和量子化学的基础。

## Application / 应用场景

- Shor's algorithm: period finding (Shor 算法：周期查找)
- Quantum chemistry: energy eigenvalues (量子化学：能量本征值)
- Quantum counting: number of solutions (量子计数：解的数量)
- HHL algorithm: linear systems (HHL 算法：线性系统)

## How it works / 原理

QPE estimates θ in U|ψ⟩ = e^{2πiθ}|ψ⟩ / QPE 估计 U|ψ⟩ = e^{2πiθ}|ψ⟩ 中的 θ：

```
Control qubits          Target
  |0⟩ ─H─●──●──●──QFT†──Measure → θ
  |0⟩ ─H─┼──●──┼───────
  |0⟩ ─H─┼──┼──●───────
              │
         U^{2^0} U^{2^1} U^{2^2}
              │
         |ψ⟩ ─U──────────────────
```

### Steps / 步骤

1. **Initialize**: Put control qubits in superposition
   初始化：将控制量子比特置于叠加态

2. **Controlled-U**: Apply U^{2^k} controlled by qubit k
   受控 U：应用由量子比特 k 控制的 U^{2^k}

3. **Inverse QFT**: Extract phase information
   逆 QFT：提取相位信息

4. **Measure**: Read out the phase as a binary fraction
   测量：读出相位的二进制小数

## Code / 代码

```python
import math
from quonic.algorithms import qpe

# Estimate phase of e^{iπ} = e^{2πi·0.5} → θ = 0.5
# 估计 e^{iπ} = e^{2πi·0.5} 的相位 → θ = 0.5
result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)
# Dominant: "...100" → binary 0.100 = 0.5 ✓
```

### Understanding the output / 理解输出

The measurement gives a binary fraction / 测量给出二进制小数：

```
n_precision=3, θ=0.5
Binary: 0.100 = 1/2 = 0.5 ✓

n_precision=4, θ=0.25
Binary: 0.0100 = 1/4 = 0.25 ✓
```

## Expected Output / 预期输出

```
backend: native | shots: 1024
Result:
  |010>    1024  (100.0%)  ####################
```

Rightmost 3 bits = `010` → binary 0.10 = 0.5 → phase = π ✓

## Run / 运行

```bash
python examples/qpe/qpe.py
```

## Download / 下载

[qpe.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qpe/qpe.py)
