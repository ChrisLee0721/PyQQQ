# Quantum Walk / 量子行走

> **Algorithms** / 算法

## Overview / 概述

Quantum Walk / 量子行走

Quantum analogue of random walk, spreads quadratically faster.

## Application / 应用场景

- Search algorithms (搜索算法)
- Graph algorithms (图算法)
- Transport phenomena (输运现象)

## Code / 代码

```python
from quonic.algorithms import quantum_walk

result = quantum_walk(n_positions=5, steps=10, shots=1024)
print(result.counts)
```

## Run / 运行

```bash
python examples/quantum_walk/quantum_walk.py
```

## Download / 下载

[quantum_walk.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_walk/quantum_walk.py)
