# Syndrome Measurement / 伴随式测量

> **Error Correction** / 量子纠错

## Overview / 概述

Syndrome Measurement / Syndrome 测量

Extract error syndromes without disturbing encoded state.

## Application / 应用场景

- Error detection (错误检测)
- QEC decoding (QEC 解码)
- Fault tolerance (容错)

## Code / 代码

```python
from quonic.algorithms import syndrome_demo

result = syndrome_demo(n_data=3, shots=100)
print(result.counts)
```

## Run / 运行

```bash
python examples/syndrome/syndrome.py
```

## Download / 下载

[syndrome.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/syndrome/syndrome.py)
