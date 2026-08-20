# Quantum ODE / 量子微分方程

> **Algorithms** / 算法

## Overview / 概述

ODE Solver / ODE 求解器

Quantum algorithm for ordinary differential equations.

## Application / 应用场景

- Physics simulation (物理模拟)
- Engineering (工程)
- Dynamics (动力学)

## Code / 代码

```python
from quonic.algorithms import quantum_ode_demo

result = quantum_ode_demo(shots=1024)
print(result.counts)
```

## Run / 运行

```bash
python examples/quantum_ode/quantum_ode.py
```

## Download / 下载

[quantum_ode.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_ode/quantum_ode.py)
