# Molecular VQE / 分子 VQE

> **Quantum Chemistry** / 量子化学

## Overview / 概述

Molecular ground state / 分子基态

Compute ground state energy of molecules.

## Application / 应用场景

- Drug discovery (药物发现)
- Material design (材料设计)
- Chemical reactions (化学反应)

## Code / 代码

```python
from quonic.algorithms import molecule_vqe_demo

result = molecule_vqe_demo(maxiter=200)
print(f"Ground state energy: {result.value}")
```

## Run / 运行

```bash
python examples/molecule_vqe/molecule_vqe.py
```

## Download / 下载

[molecule_vqe.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/molecule_vqe/molecule_vqe.py)
