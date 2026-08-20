# Classical If / 经典条件分支

> **Advanced** / 高级

## Overview / 概述

Classical if statement / 经典 if 语句

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic import cif, qgate, qshow
from quonic.gates import H, X, Z

qgate(H, 0)
cif(0).then(X, 1).else_(Z, 1)
qgate(H, 0)
qgate(H, 1)
qshow()
```

## Run / 运行

```bash
python examples/cif/cif.py
```

## Download / 下载

[cif.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/cif/cif.py)
