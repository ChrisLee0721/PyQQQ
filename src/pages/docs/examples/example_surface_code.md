# Surface Code / 表面码

> **Error Correction** / 量子纠错

## Overview / 概述

Surface Code / 表面码

Leading candidate for fault-tolerant quantum computing.

## Application / 应用场景

- Fault tolerance (容错)
- Quantum memory (量子存储)
- Logical qubits (逻辑比特)

## Code / 代码

```python
from quonic.algorithms import surface_code_demo

result = surface_code_demo(distance=3, shots=100)
print(result.counts)
```

## Run / 运行

```bash
python examples/surface_code/surface_code.py
```

## Download / 下载

[surface_code.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/surface_code/surface_code.py)
