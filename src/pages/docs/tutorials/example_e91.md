# E91 QKD / E91 量子密钥分发

> **Communication** / 通信

## Overview / 概述

E91 key distribution / E91 密钥分发

E91 protocol using entangled pairs and Bell inequality.

## Application / 应用场景

- Quantum key distribution (量子密钥分发)
- Entanglement verification (纠缠验证)
- Device-independent QKD (设备无关 QKD)

## Code / 代码

```python
from quonic.algorithms import e91

result = e91(n_rounds=100)
print(f"Result: {result.value}")
```

## Run / 运行

```bash
python examples/e91/e91.py
```

## Download / 下载

[e91.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/e91/e91.py)
