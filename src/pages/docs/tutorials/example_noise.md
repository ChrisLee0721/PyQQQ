# Noise Simulation / 噪声模拟

> **Noise & Mitigation** / 噪声与缓解

## Overview / 概述

Noise simulation / 噪声模拟

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
qshow(noise=0.05)
```

## Run / 运行

```bash
python examples/noise/noise.py
```

## Download / 下载

[noise.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/noise/noise.py)
