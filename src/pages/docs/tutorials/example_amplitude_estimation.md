# Amplitude Estimation / 振幅估计

> **Algorithms** / 算法

## Overview / 概述

Estimate success probability / 估计成功概率

Quantum algorithm to estimate the amplitude of a marked state.

## Application / 应用场景

- Monte Carlo integration (蒙特卡洛积分)
- Risk analysis (风险分析)
- Option pricing (期权定价)

## Code / 代码

```python
from quonic.algorithms import amplitude_estimation_demo

result = amplitude_estimation_demo(n_qubits=2, n_precision=3, shots=1024)
print(result.counts)
```

## Run / 运行

```bash
python examples/amplitude_estimation/amplitude_estimation.py
```

## Download / 下载

[amplitude_estimation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/amplitude_estimation/amplitude_estimation.py)
