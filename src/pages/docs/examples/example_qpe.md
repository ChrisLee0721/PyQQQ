# Quantum Phase Estimation / 量子相位估计

> **Algorithms** / 算法

## Overview / 概述

Quantum Phase Estimation / 量子相位估计

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
import math

from quonic.algorithms import qpe

result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)  # dominated by "...010" (rightmost 3 bits -> j = 2)
```

## Run / 运行

```bash
python examples/qpe/qpe.py
```

## Download / 下载

[qpe.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qpe/qpe.py)
