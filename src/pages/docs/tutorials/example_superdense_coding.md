# Superdense Coding / 超密编码

> **Communication** / 通信

## Overview / 概述

Superdense Coding / 超密编码

Send 2 classical bits using 1 qubit.

## Application / 应用场景

- Quantum communication (量子通信)
- Bandwidth doubling (带宽翻倍)
- Teleportation (隐形传态)

## Code / 代码

```python
from quonic.algorithms import superdense_coding

for msg in ["00", "01", "10", "11"]:
    result = superdense_coding(message=msg, shots=100)
    # value is the decoded integer (0-3)
    decoded = f"{int(result.value):02b}"
    print(f"Sent: {msg}, Decoded: {decoded}")
```

## Run / 运行

```bash
python examples/superdense_coding/superdense_coding.py
```

## Download / 下载

[superdense_coding.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/superdense_coding/superdense_coding.py)
