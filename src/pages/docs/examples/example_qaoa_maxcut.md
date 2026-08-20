# QAOA MaxCut / QAOA 最大割

> **Algorithms** / 算法

## Overview / 概述

QAOA for MaxCut / QAOA 求解 MaxCut

Reproduce Farhi et al. (2014) MaxCut optimization.

## Application / 应用场景

- Combinatorial optimization (组合优化)
- Graph partitioning (图划分)
- Benchmark (基准测试)

## Code / 代码

```python
from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, p=1, maxiter=100)
print(f"Max cut: {result.value}")
```

## Run / 运行

```bash
python examples/qaoa_maxcut/qaoa_maxcut.py
```

## Download / 下载

[qaoa_maxcut.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa_maxcut/qaoa_maxcut.py)
