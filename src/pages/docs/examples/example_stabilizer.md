# Stabilizer Formalism / 稳定子形式

> **Error Correction** / 量子纠错

## Overview / 概述

Stabilizer Formalism / 稳定子形式

Clifford group simulation via stabilizer tableau.

## Application / 应用场景

- Error correction (纠错)
- Clifford simulation (Clifford 模拟)
- Quantum circuits (量子电路)

## Code / 代码

```python
from quonic.algorithms import stabilizer_demo

result = stabilizer_demo(n_qubits=3, shots=100)
print(result.counts)
```

## Run / 运行

```bash
python examples/stabilizer/stabilizer.py
```

## Download / 下载

[stabilizer.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/stabilizer/stabilizer.py)
