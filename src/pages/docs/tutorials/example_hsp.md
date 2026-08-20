# Hidden Subgroup / 隐藏子群

> **Algorithms** / 算法

## Overview / 概述

Hidden Subgroup Problem / 隐藏子群问题

General framework for Simon, Shor, and other HSP algorithms.

## Application / 应用场景

- Factoring (因式分解)
- Discrete log (离散对数)
- Graph isomorphism (图同构)

## Code / 代码

```python
from quonic.algorithms import hsp_demo

result = hsp_demo()
print(result.counts)
```

## Run / 运行

```bash
python examples/hsp/hsp.py
```

## Download / 下载

[hsp.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/hsp/hsp.py)
