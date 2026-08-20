# Deutsch-Jozsa / Deutsch-Jozsa 算法

> **Algorithms** / 算法

## Overview / 概述

Constant or balanced function? / 常数还是平衡函数？

Determine if f is constant or balanced in one query.

## Application / 应用场景

- Oracle complexity (预言机复杂度)
- Quantum advantage (量子优势)
- Function analysis (函数分析)

## Code / 代码

```python
from quonic import qgate
from quonic.algorithms import deutsch_jozsa
from quonic.gates import CX

N = 3

def balanced_oracle(circuit, n):
    """Balanced oracle: flip last qubit if first qubit is |1>."""
    qgate(CX, 0, n)

result = deutsch_jozsa(N, balanced_oracle, shots=100)
print(f"Counts: {result.counts}")
```

## Run / 运行

```bash
python examples/deutsch_jozsa/deutsch_jozsa.py
```

## Download / 下载

[deutsch_jozsa.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/deutsch_jozsa/deutsch_jozsa.py)
