# Quantum GAN / 量子生成对抗网络

> **Quantum ML** / 量子机器学习

## Overview / 概述

Quantum GAN / 量子 GAN

Quantum generator + classical discriminator.

## Application / 应用场景

- Data generation (数据生成)
- Image synthesis (图像合成)
- Quantum ML (量子机器学习)

## Code / 代码

```python
from quonic.algorithms import qgan_demo

result = qgan_demo(n_steps=50)
print(result.counts)
```

## Run / 运行

```bash
python examples/qgan/qgan.py
```

## Download / 下载

[qgan.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qgan/qgan.py)
