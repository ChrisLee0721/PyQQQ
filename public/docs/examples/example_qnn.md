# Quantum Neural Network / 量子神经网络

> **Quantum ML** / 量子机器学习

## Overview / 概述

Quantum Neural Network / 量子神经网络

Variational quantum circuit as neural network.

## Application / 应用场景

- Classification (分类)
- Regression (回归)
- Function approximation (函数逼近)

## Code / 代码

```python
from quonic.algorithms import qnn_demo

result = qnn_demo(n_qubits=2, depth=2)
print(result.counts)
```

## Run / 运行

```bash
python examples/qnn/qnn.py
```

## Download / 下载

[qnn.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qnn/qnn.py)
