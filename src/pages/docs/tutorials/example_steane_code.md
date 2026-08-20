# Steane Code / Steane 码

> **Error Correction** / 量子纠错

## Overview / 概述

Steane Code / Steane 码

[[7,1,3]] CSS code, corrects arbitrary single-qubit errors.

## Application / 应用场景

- Quantum error correction (量子纠错)
- Fault tolerance (容错)
- Logical gates (逻辑门)

## Code / 代码

```python
from quonic.algorithms import steane_code

result = steane_code(error_qubit=0, shots=100)
print(result.counts)
```

## Run / 运行

```bash
python examples/steane_code/steane_code.py
```

## Download / 下载

[steane_code.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/steane_code/steane_code.py)
