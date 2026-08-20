# Noise Model / 噪声模型

> **Noise & Mitigation** / 噪声与缓解

## Overview / 概述

Noise model / 噪声模型

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic import NoiseModel, qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=NoiseModel(single=0.01, double=0.05))
```

## Run / 运行

```bash
python examples/noise_model/noise_model.py
```

## Download / 下载

[noise_model.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/noise_model/noise_model.py)
