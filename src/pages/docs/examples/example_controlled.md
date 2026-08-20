# Controlled Gates / 受控门

> **Foundational** / 基础

## Overview / 概述

Controlled gates / 受控门

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic import controlled, qgate, qshow
from quonic.gates import H, Ry

qgate(H, 0)
controlled(Ry(0.7), 0, 1)
qshow()
```

## Run / 运行

```bash
python examples/controlled/controlled.py
```

## Download / 下载

[controlled.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/controlled/controlled.py)
