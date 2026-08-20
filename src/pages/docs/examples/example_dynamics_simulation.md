# Dynamics Simulation / 动力学模拟

> **Algorithms** / 算法

## Overview / 概述

Quantum dynamics simulation / 量子动力学模拟

Simulate time evolution of quantum systems.

## Application / 应用场景

- Quantum chemistry (量子化学)
- Material science (材料科学)
- Condensed matter (凝聚态)

## Code / 代码

```python
from quonic.algorithms import dynamics_simulation_demo

result = dynamics_simulation_demo(n_steps=10, shots=1024)
print(result.counts)
```

## Run / 运行

```bash
python examples/dynamics_simulation/dynamics_simulation.py
```

## Download / 下载

[dynamics_simulation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/dynamics_simulation/dynamics_simulation.py)
