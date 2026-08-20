# Classical While / 经典循环

> **Advanced** / 高级

## Overview / 概述

Classical while loop / 经典 while 循环

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic import creg, cwhile, qgate, qshow
from quonic.gates import H

flag = creg("flag")
with cwhile(flag, until=0):
    qgate(H, 0)
    flag.measure(0)

qshow(backend="native")  # cwhile 逐 shot 动态执行，仅 native 后端支持
```

## Run / 运行

```bash
python examples/cwhile/cwhile.py
```

## Download / 下载

[cwhile.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/cwhile/cwhile.py)
