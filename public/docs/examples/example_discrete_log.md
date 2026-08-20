# Discrete Logarithm / 离散对数

> **Algorithms** / 算法

## Overview / 概述

Discrete logarithm / 离散对数

Find x such that a^x = b mod p.

## Application / 应用场景

- Cryptography (密码学)
- RSA breaking (RSA 破解)
- Key exchange (密钥交换)

## Code / 代码

```python
from quonic.algorithms import discrete_log_demo

result = discrete_log_demo(a=2, b=8, p=11)
print(result.counts)
```

## Run / 运行

```bash
python examples/discrete_log/discrete_log.py
```

## Download / 下载

[discrete_log.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/discrete_log/discrete_log.py)
