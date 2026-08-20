# Grover Search / Grover 搜索

> **Algorithms** / 算法

## Overview / 概述

Search an unsorted database / 搜索无序数据库

Find a specific item in an unsorted list. Classical: O(N) queries. Quantum: O(√N) queries.

## Application / 应用场景

- Database search (数据库搜索)
- Cryptography: searching key space (密码学：搜索密钥空间)
- Optimization: finding optimal solution (优化：寻找最优解)
- SAT solving (SAT 求解)

## How it works / 原理

Oracle marks target state, diffusion amplifies its probability.
Oracle 标记目标态，diffusion 放大概率。

## Code / 代码

```python
from quonic.algorithms import grover

result = grover("11", 2, shots=1024)
print(result.counts)
```

## Expected Output / 预期输出

Target state appears with ~99% probability after optimal iterations.
目标态在最优迭代后以 ~99% 概率出现。

## Run / 运行

```bash
python examples/grover/grover.py
```

## Download / 下载

[grover.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/grover/grover.py)
