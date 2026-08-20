# QAOA TSP / QAOA 旅行商问题

> **Algorithms** / 算法

## Overview / 概述

Traveling Salesman Problem / 旅行商问题

QAOA for TSP: find shortest route visiting all cities.

## Application / 应用场景

- Logistics (物流)
- Route planning (路线规划)
- Circuit design (电路设计)

## Code / 代码

```python
from quonic.algorithms import qaoa_tsp

distances = {
    (0, 1): 1.0, (1, 0): 1.0,
    (1, 2): 2.0, (2, 1): 2.0,
    (0, 2): 1.5, (2, 0): 1.5,
}
result = qaoa_tsp(distances, 3, p=1, maxiter=100)
print(f"Tour cost: {result.value}")
```

## Run / 运行

```bash
python examples/qaoa_tsp/qaoa_tsp.py
```

## Download / 下载

[qaoa_tsp.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa_tsp/qaoa_tsp.py)
