# GHZ State / GHZ 态

> **Foundational** / 基础

## Overview / 概述

GHZ state / GHZ 态

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()
```

## Run / 运行

```bash
python examples/ghz/ghz.py
```

## Download / 下载

[ghz.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/ghz/ghz.py)
