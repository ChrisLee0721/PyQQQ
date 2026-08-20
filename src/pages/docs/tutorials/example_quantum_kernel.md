# Quantum Kernel / 量子核方法

> **Quantum ML** / 量子机器学习

## Overview / 概述

Quantum Kernel Estimation / 量子核估计

Compute quantum kernel matrix for ML.

## Application / 应用场景

- Kernel methods (核方法)
- SVM (支持向量机)
- Quantum ML (量子机器学习)

## Code / 代码

```python
from quonic.algorithms import quantum_kernel

X = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
result = quantum_kernel(X, n_qubits=2, shots=10000)
print(result.counts)
```

## Run / 运行

```bash
python examples/quantum_kernel/quantum_kernel.py
```

## Download / 下载

[quantum_kernel.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_kernel/quantum_kernel.py)
