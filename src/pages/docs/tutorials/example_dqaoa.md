# Dynamic QAOA / 动态 QAOA

> **Algorithms** / 算法

## Overview / 概述

Dynamic QAOA / 动态 QAOA

Adaptive layer QAOA that adds layers until convergence.

## Application / 应用场景

- Combinatorial optimization (组合优化)
- MaxCut (最大割)
- Scheduling (调度)

## Code / 代码

```python
from quonic.algorithms import dqaoa_demo

result = dqaoa_demo()
print(result.counts)
```

## Run / 运行

```bash
python examples/dqaoa/dqaoa.py
```

## Download / 下载

[dqaoa.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/dqaoa/dqaoa.py)
