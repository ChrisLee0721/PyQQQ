# Gate Decomposition / 门分解

> **Compiler** / 编译器

## Overview / 概述

Gate decomposition / 门分解

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic.compiler import decompose
from quonic.ir import Circuit, GateOperation

circuit = Circuit()
circuit.add(GateOperation("ccx", (0, 1, 2)))

expanded = decompose(circuit)
print("输入门: ccx x 1")
print(f"输出门: {expanded.gate_count()} 个基础门")
print([op.name for op in expanded.ops])
```

## Run / 运行

```bash
python examples/decompose/decompose.py
```

## Download / 下载

[decompose.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/decompose/decompose.py)
