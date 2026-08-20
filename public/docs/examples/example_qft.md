# Quantum Fourier Transform / 量子傅里叶变换

> **Algorithms** / 算法

## Overview / 概述

Quantum version of the Discrete Fourier Transform. Foundation for many quantum algorithms including Shor's and QPE.

离散傅里叶变换的量子版本。是 Shor 算法和量子相位估计等许多量子算法的基础。

## Application / 应用场景

- Shor's algorithm for factoring (Shor 因式分解算法)
- Quantum phase estimation (量子相位估计)
- Quantum counting (量子计数)
- Signal processing (信号处理)

## How it works / 原理

QFT transforms computational basis states to Fourier basis / QFT 将计算基态变换到傅里叶基态：

```
|j⟩ → (1/√N) Σ_k e^{2πijk/N} |k⟩
```

The circuit uses H gates + controlled phase rotations / 电路使用 H 门 + 受控相位旋转：

```
q₀: ─H──R₂──R₃──R₄──×──
           │    │    │
q₁: ──────H────R₂──R₃─×──
                  │    │
q₂: ────────────H────R₂──
```

Where R_k = phase rotation by 2π/2^k / 其中 R_k = 相位旋转 2π/2^k

## Step-by-step for 3 qubits / 3 量子比特逐步解析

### Input: |010⟩ (decimal 2) / 输入：|010⟩（十进制 2）

**Step 1**: H on qubit 0 → creates superposition
对 qubit 0 施加 H → 创建叠加态

**Step 2**: Controlled rotations encode frequency information
受控旋转编码频率信息

**Step 3**: Swap qubits to correct ordering
交换量子比特以修正顺序

### Output: Fourier coefficients / 输出：傅里叶系数

The amplitudes encode the frequency components of the input state.
振幅编码了输入态的频率分量。

## Code / 代码

```python
from quonic.algorithms import qft

# 3-qubit QFT
# 3 量子比特 QFT
result = qft(n_qubits=3, shots=1024)
print(result.counts)
```

### Manual QFT / 手动构造 QFT

```python
from quonic import qgate, qshow
from quonic.gates import H

# 3-qubit QFT circuit
qgate(H, 0)
# Controlled rotations (simplified)
qgate(H, 1)
qgate(H, 2)
qshow()
```

## Classical vs Quantum / 经典 vs 量子

| | FFT (Classical) | QFT (Quantum) |
|---|---|---|
| Complexity | O(N log N) | O(log²N) |
| N=1024 | 10,240 ops | ~100 ops |
| N=10⁶ | 20M ops | ~400 ops |

QFT provides **exponential speedup** over classical FFT.

QFT 相对于经典 FFT 提供**指数加速**。

## Expected Output / 预期输出

Transforms computational basis to Fourier basis / 将计算基变换到傅里叶基：

```
backend: native | shots: 1024
Result:
  |000>    128  (12.5%)  ####
  |001>    128  (12.5%)  ####
  |010>    128  (12.5%)  ####
  ...
```

## Run / 运行

```bash
python examples/qft/qft.py
```

## Download / 下载

[qft.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qft/qft.py)
