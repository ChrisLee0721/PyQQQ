# Amplitude Amplification / 振幅放大

> **Algorithms** / 算法

## Overview / 概述

Amplify probability of target state / 放大目标态概率

Like Grover but with custom state preparation. Boosts success probability.

## Application / 应用场景

- Quantum algorithms (量子算法)
- State preparation (态制备)
- Error mitigation (错误缓解)

## Code / 代码

```python
from quonic.algorithms import amplitude_amplification, mark_state

oracle_fn = mark_state("11")
result = amplitude_amplification(2, oracle_fn, shots=1024)
print(result.counts)
```

## Run / 运行

```bash
python examples/amplitude_amplification/amplitude_amplification.py
```

## Download / 下载

[amplitude_amplification.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/amplitude_amplification/amplitude_amplification.py)
