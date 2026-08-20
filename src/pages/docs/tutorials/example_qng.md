# Quantum Natural Gradient / 量子自然梯度

> **Quantum ML** / 量子机器学习

## Overview / 概述

Quantum Natural Gradient / 量子自然梯度

Uses quantum Fisher information for better optimization.

## Application / 应用场景

- Variational algorithms (变分算法)
- VQE optimization (VQE 优化)
- Quantum ML (量子机器学习)

## Code / 代码

```python
from quonic.algorithms import qng_demo

result = qng_demo(n_params=2, maxiter=50)
print(f"Final loss: {result.value}")
```

## Run / 运行

```bash
python examples/qng/qng.py
```

## Download / 下载

[qng.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qng/qng.py)
