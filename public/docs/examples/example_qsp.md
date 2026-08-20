# Quantum Signal Processing / 量子信号处理

> **Algorithms** / 算法

## Overview / 概述

Quantum Signal Processing / 量子信号处理

Core subroutine for quantum singular value transformation.

## Application / 应用场景

- Quantum algorithms (量子算法)
- Hamiltonian simulation (哈密顿量模拟)
- Eigenvalue problems (特征值问题)

## Code / 代码

```python
from quonic.algorithms import qsp_demo

result = qsp_demo(angle=0.785)
print(result.counts)
```

## Run / 运行

```bash
python examples/qsp/qsp.py
```

## Download / 下载

[qsp.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qsp/qsp.py)
