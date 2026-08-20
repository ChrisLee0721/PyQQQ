# Quantum Fourier Transform / 量子傅里叶变换

> **Algorithms** / 算法

## Overview / 概述

Quantum Fourier Transform / 量子傅里叶变换

Quantum version of DFT. Foundation for many quantum algorithms.

## Application / 应用场景

- Shor's algorithm (Shor 算法)
- Quantum phase estimation (量子相位估计)
- Quantum counting (量子计数)
- Signal processing (信号处理)

## How it works / 原理

H gates + controlled rotations create frequency-domain representation.
H 门 + 受控旋转创建频域表示。

## Code / 代码

```python
from quonic.algorithms import qft

result = qft(n_qubits=3, shots=1024)
print(result.counts)
```

## Expected Output / 预期输出

Transforms computational basis to Fourier basis.
将计算基变换到傅里叶基。

## Run / 运行

```bash
python examples/qft/qft.py
```

## Download / 下载

[qft.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qft/qft.py)
