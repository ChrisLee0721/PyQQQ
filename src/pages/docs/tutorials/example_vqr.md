# VQR / 变分量子回归器

> **Quantum ML** / 量子机器学习

## Overview / 概述

Variational Quantum Regressor / 变分量子回归器

Quantum model for regression tasks.

## Application / 应用场景

- Regression (回归)
- Prediction (预测)
- Function fitting (函数拟合)

## Code / 代码

```python
from quonic.algorithms import vqr

X = [[0.0], [0.5], [1.0], [1.5]]
y = [0.0, 0.479, 0.841, 0.997]
result = vqr(X, y, n_params=2, maxiter=100)
print(f"Final loss: {result.value}")
```

## Run / 运行

```bash
python examples/vqr/vqr.py
```

## Download / 下载

[vqr.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/vqr/vqr.py)
