# Shor's Algorithm / Shor 算法

> **Algorithms** / 算法

## Overview / 概述

Shor's algorithm / Shor 算法

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic.algorithms import shor

result = shor(15, a=7, t=6, shots=256)
print(result.value)                    # 3 or 5
print(result.metadata["period"])       # 4 (the order of 7 mod 15)
```

## Run / 运行

```bash
python examples/shor/shor.py
```

## Download / 下载

[shor.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/shor/shor.py)
