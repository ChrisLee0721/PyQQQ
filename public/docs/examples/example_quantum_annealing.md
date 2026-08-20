# Quantum Annealing / 量子退火

> **Algorithms** / 算法

## Overview / 概述

Quantum Annealing / 量子退火

Hybrid classical-quantum annealing for optimization.

## Application / 应用场景

- Optimization (优化)
- Combinatorial problems (组合问题)
- Sampling (采样)

## Code / 代码

```python
from quonic.algorithms import quantum_annealing_hybrid_demo

result = quantum_annealing_hybrid_demo(n_spins=4, n_steps=100)
print(result.counts)
```

## Run / 运行

```bash
python examples/quantum_annealing/quantum_annealing.py
```

## Download / 下载

[quantum_annealing.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_annealing/quantum_annealing.py)
