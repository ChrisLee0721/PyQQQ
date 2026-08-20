# Oracle Construction / Oracle 构造

> **Algorithms** / 算法

## Overview / 概述

Oracle construction / 预言机构造

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic.algorithms import grover, oracle


@oracle(3)
def is_five(x):
    return x == 5


result = grover(is_five, 3, shots=1024)
print(result.counts)  # dominated by |101>
```

## Run / 运行

```bash
python examples/oracle/oracle.py
```

## Download / 下载

[oracle.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/oracle/oracle.py)
