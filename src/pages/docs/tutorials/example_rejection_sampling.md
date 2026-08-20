# Rejection Sampling / 量子拒绝采样

> **Algorithms** / 算法

## Overview / 概述

Rejection Sampling / 拒绝采样

Quantum-enhanced rejection sampling.

## Application / 应用场景

- Sampling (采样)
- Distribution generation (分布生成)
- Monte Carlo (蒙特卡洛)

## Code / 代码

```python
from quonic.algorithms import rejection_sampling_demo

result = rejection_sampling_demo(n_samples=100)
print(result.counts)
```

## Run / 运行

```bash
python examples/rejection_sampling/rejection_sampling.py
```

## Download / 下载

[rejection_sampling.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/rejection_sampling/rejection_sampling.py)
