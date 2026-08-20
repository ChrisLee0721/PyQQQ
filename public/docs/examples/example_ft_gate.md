# Fault-Tolerant Gates / 容错门

> **Error Correction** / 量子纠错

## Overview / 概述

Fault-tolerant gates / 容错门

Gates implemented with error detection/correction.

## Application / 应用场景

- Fault-tolerant computing (容错计算)
- Quantum error correction (量子纠错)
- Logical gates (逻辑门)

## Code / 代码

```python
from quonic.algorithms import ft_gate_demo

result = ft_gate_demo(shots=100)
print(result.counts)
```

## Run / 运行

```bash
python examples/ft_gate/ft_gate.py
```

## Download / 下载

[ft_gate.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/ft_gate/ft_gate.py)
