# QAOA / 量子近似优化算法

> **Algorithms** / 算法

## Overview / 概述

QAOA algorithm / QAOA 算法

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)
print(result.value)  # ≈ 2.0
```

## Run / 运行

```bash
python examples/qaoa/qaoa.py
```

## Download / 下载

[qaoa.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa/qaoa.py)
