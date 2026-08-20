# Phase-Flip Code / 相位翻转码

> **Error Correction** / 量子纠错

## Overview / 概述

Correct phase-flip errors / 纠正相位翻转错误

3-qubit code corrects single phase-flip errors.

## Application / 应用场景

- Quantum error correction (量子纠错)
- Phase protection (相位保护)
- NISQ algorithms (NISQ 算法)

## Code / 代码

```python
from quonic.algorithms import phase_flip_code

result = phase_flip_code(error_qubit=0, shots=100)
print(result.counts)
```

## Run / 运行

```bash
python examples/phase_flip_code/phase_flip_code.py
```

## Download / 下载

[phase_flip_code.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/phase_flip_code/phase_flip_code.py)
