# Quantum Monte Carlo / 量子蒙特卡洛

> **Algorithms** / 算法

## Overview / 概述

Quantum Monte Carlo / 量子蒙特卡洛

Quantum speedup for Monte Carlo methods.

## Application / 应用场景

- Integration (积分)
- Risk analysis (风险分析)
- Finance (金融)

## Code / 代码

```python
from quonic.algorithms import quantum_monte_carlo_demo

result = quantum_monte_carlo_demo(n_qubits=2, shots=1024)
print(f"Estimated value: {result.value}")
```

## Run / 运行

```bash
python examples/quantum_monte_carlo/quantum_monte_carlo.py
```

## Download / 下载

[quantum_monte_carlo.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_monte_carlo/quantum_monte_carlo.py)
