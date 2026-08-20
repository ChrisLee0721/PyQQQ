# Diffusion Operator / 扩散算子

> **Algorithms** / 算法

## Overview / 概述

Diffusion operator / 扩散算子

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic import qgate, qshow
from quonic.algorithms import diffusion, mark_state
from quonic.gates import H
from quonic.stack import current_circuit

n = 2
for q in range(n):
    qgate(H, q)
mark_state("11")(current_circuit())  # 相位标记 |11>
diffusion(n)                          # 一次振幅放大
qshow()
```

## Run / 运行

```bash
python examples/diffusion/diffusion.py
```

## Download / 下载

[diffusion.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/diffusion/diffusion.py)
