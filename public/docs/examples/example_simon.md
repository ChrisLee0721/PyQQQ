# Simon's Algorithm / Simon 算法

> **Algorithms** / 算法

## Overview / 概述

Simon's Algorithm / Simon 算法

Find hidden period of 2-to-1 function. Precursor to Shor.

## Application / 应用场景

- Cryptography (密码学)
- Period finding (周期查找)
- Quantum advantage (量子优势)

## Code / 代码

```python
from quonic import qgate
from quonic.algorithms import simon
from quonic.gates import CX

# Hidden period s = "101" (decimal 5)
S = 5
N = 3

def simon_oracle(circuit, n):
    """Oracle for f(x) = f(x XOR s)."""
    for i in range(n):
        qgate(CX, i, i + n)
    for i in range(n):
        if (S >> i) & 1:
            qgate(CX, 0, i + n)

result = simon(N, simon_oracle, shots=200)
print(result.counts)
```

## Run / 运行

```bash
python examples/simon/simon.py
```

## Download / 下载

[simon.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/simon/simon.py)
