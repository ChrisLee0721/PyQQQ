# Lattice SVP / 格最短向量

> **Algorithms** / 算法

## Overview / 概述

Shortest Vector Problem / 最短向量问题

Quantum approach to lattice-based cryptography.

## Application / 应用场景

- Post-quantum cryptography (后量子密码学)
- Lattice-based crypto (格密码)
- Security analysis (安全分析)

## Code / 代码

```python
from quonic.algorithms import lattice_svp_demo

result = lattice_svp_demo()
print(result.counts)
```

## Run / 运行

```bash
python examples/lattice_svp/lattice_svp.py
```

## Download / 下载

[lattice_svp.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/lattice_svp/lattice_svp.py)
