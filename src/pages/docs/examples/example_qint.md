# Quantum Integer / 量子整数运算

> **Advanced** / 高级

## Overview / 概述

Quantum integer / 量子整数

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic import QInt, qshow

x = QInt(3, value=5)  # |5> = |101>
x += 3                # quantum addition: 5 + 3 ≡ 0 (mod 8)
qshow()
```

## Run / 运行

```bash
python examples/qint/qint.py
```

## Download / 下载

[qint.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qint/qint.py)
