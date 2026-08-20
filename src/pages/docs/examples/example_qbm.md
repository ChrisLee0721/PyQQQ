# Quantum Boltzmann Machine / 量子玻尔兹曼机

> **Quantum ML** / 量子机器学习

## Overview / 概述

Quantum Boltzmann Machine / 量子玻尔兹曼机

Quantum version of Boltzmann machine for generative modeling.

## Application / 应用场景

- Generative models (生成模型)
- Sampling (采样)
- Machine learning (机器学习)

## Code / 代码

```python
from quonic.algorithms import qbm_demo

result = qbm_demo(temperature=1.0)
print(result.counts)
```

## Run / 运行

```bash
python examples/qbm/qbm.py
```

## Download / 下载

[qbm.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qbm/qbm.py)
