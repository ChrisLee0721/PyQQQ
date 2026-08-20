# Backend Comparison / 后端对比

> **Backends** / 后端

## Overview / 概述

Compare backends / 比较后端

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic import QInt, qlt, qshow

x = QInt(3)
x.h()            # uniform superposition |0>..|7>
flag = qlt(x, 4) # flag = 1 iff x < 4

qshow()
```

## Run / 运行

```bash
python examples/compare/compare.py
```

## Download / 下载

[compare.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/compare/compare.py)
