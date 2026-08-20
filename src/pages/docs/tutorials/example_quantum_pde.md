# Quantum PDE / 量子偏微分方程

> **Algorithms** / 算法

## Overview / 概述

PDE Solver / PDE 求解器

Quantum algorithm for partial differential equations.

## Application / 应用场景

- Fluid dynamics (流体力学)
- Heat transfer (热传导)
- Electromagnetics (电磁学)

## Code / 代码

```python
from quonic.algorithms import quantum_pde_demo

result = quantum_pde_demo(shots=1024)
print(result.counts)
```

## Run / 运行

```bash
python examples/quantum_pde/quantum_pde.py
```

## Download / 下载

[quantum_pde.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_pde/quantum_pde.py)
