# Shor Code / Shor 码

> **Error Correction** / 量子纠错

## Overview / 概述

Shor's 9-qubit Code / Shor 9 比特码

First quantum error correction code, corrects arbitrary errors.

## Application / 应用场景

- Quantum error correction (量子纠错)
- Fault tolerance (容错)
- Quantum memory (量子存储)

## Code / 代码

```python
from quonic.algorithms import shor_code

result = shor_code(error_qubit=0, shots=100)
print(result.counts)
```

## Run / 运行

```bash
python examples/shor_code/shor_code.py
```

## Download / 下载

[shor_code.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/shor_code/shor_code.py)
