# Quantum If / 量子条件分支

> **Advanced** / 高级

## Overview / 概述

Quantum if / 量子 if

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic import qgate, qif, qshow
from quonic.gates import H, I, X

qgate(H, 0)
qif(0).then(X, 1).else_(I, 1)
qshow()
```

## Run / 运行

```bash
python examples/qif/qif.py
```

## Download / 下载

[qif.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qif/qif.py)
