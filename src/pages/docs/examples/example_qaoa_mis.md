# QAOA MIS / QAOA 最大独立集

> **Algorithms** / 算法

## Overview / 概述

Maximum Independent Set / 最大独立集

QAOA for MIS: find largest set of non-adjacent vertices.

## Application / 应用场景

- Graph theory (图论)
- Scheduling (调度)
- Resource allocation (资源分配)

## Code / 代码

```python
from quonic.algorithms import qaoa_mis

edges = [(0, 1), (1, 2)]
result = qaoa_mis(edges, 3, p=1, maxiter=100)
print(f"MIS size: {result.value}")
```

## Run / 运行

```bash
python examples/qaoa_mis/qaoa_mis.py
```

## Download / 下载

[qaoa_mis.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa_mis/qaoa_mis.py)
