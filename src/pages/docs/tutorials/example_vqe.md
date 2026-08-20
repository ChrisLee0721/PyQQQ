# VQE / 变分量子本征求解器

> **Algorithms** / 算法

## Overview / 概述

Find ground state energy / 寻找基态能量

Variational Quantum Eigensolver finds the lowest energy of a quantum system.

## Application / 应用场景

- Quantum chemistry: molecular ground states (量子化学：分子基态)
- Materials science: new materials (材料科学：新材料)
- Drug discovery: molecular properties (药物发现：分子性质)

## How it works / 原理

Parameterized circuit + classical optimizer minimize energy expectation.
参数化电路 + 经典优化器最小化能量期望值。

## Code / 代码

```python
from quonic.algorithms import vqe

hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)  # ≈ -2.236
```

## Expected Output / 预期输出

Energy value converges to exact ground state energy.
能量值收敛到精确基态能量。

## Run / 运行

```bash
python examples/vqe/vqe.py
```

## Download / 下载

[vqe.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/vqe/vqe.py)
