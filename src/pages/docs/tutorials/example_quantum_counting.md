# Quantum Counting / 量子计数

> **Algorithms** / 算法

## Overview / 概述

Quantum Counting / 量子计数

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic.algorithms import oracle, quantum_counting


@oracle(3)
def even(x):
    return x & 1 == 0


result = quantum_counting(even, 3, shots=2048)
print(result.value)  # ~ 4
```

## Run / 运行

```bash
python examples/quantum_counting/quantum_counting.py
```

## Download / 下载

[quantum_counting.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_counting/quantum_counting.py)
