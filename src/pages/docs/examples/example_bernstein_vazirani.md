# Bernstein-Vazirani / Bernstein-Vazirani 算法

> **Algorithms** / 算法

## Overview / 概述

Find hidden bitstring / 找到隐藏比特串

Find secret s in f(x) = s·x mod 2. One query suffices.

## Application / 应用场景

- Oracle problems (预言机问题)
- Cryptography (密码学)
- Learning parity (学习奇偶性)

## Code / 代码

```python
from quonic import qgate
from quonic.algorithms import bernstein_vazirani
from quonic.gates import CZ

# Hidden string s = "1010" (decimal 10)
S = 10
N = 4

def bv_oracle(circuit, n):
    """Phase oracle for f(x) = s·x mod 2."""
    for i in range(n):
        if (S >> i) & 1:
            qgate(CZ, i, n)

result = bernstein_vazirani(N, bv_oracle, shots=1024)
print(result.counts)
```

## Run / 运行

```bash
python examples/bernstein_vazirani/bernstein_vazirani.py
```

## Download / 下载

[bernstein_vazirani.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/bernstein_vazirani/bernstein_vazirani.py)
