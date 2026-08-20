# Hamiltonian Simulation / 哈密顿模拟

> **Algorithms** / 算法

## Overview / 概述

Hamiltonian simulation / 哈密顿量模拟

Simulate e^{-iHt} for given Hamiltonian.

## Application / 应用场景

- Quantum chemistry (量子化学)
- Material science (材料科学)
- Quantum simulation (量子模拟)

## Code / 代码

```python
from quonic.algorithms import hamiltonian_simulation_demo

result = hamiltonian_simulation_demo()
print(result.counts)
```

## Run / 运行

```bash
python examples/hamiltonian_simulation/hamiltonian_simulation.py
```

## Download / 下载

[hamiltonian_simulation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/hamiltonian_simulation/hamiltonian_simulation.py)
