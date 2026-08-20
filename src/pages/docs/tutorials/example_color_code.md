# Color Code / 颜色码

> **Error Correction** / 量子纠错

## Overview / 概述

Color code error correction / 颜色码纠错

Topological error correction code with transversal gates.

## Application / 应用场景

- Fault-tolerant quantum computing (容错量子计算)
- Topological codes (拓扑码)
- Quantum memory (量子存储)

## Code / 代码

```python
from quonic.algorithms import color_code_demo

result = color_code_demo(shots=100)
print(result.counts)
```

## Run / 运行

```bash
python examples/color_code/color_code.py
```

## Download / 下载

[color_code.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/color_code/color_code.py)
