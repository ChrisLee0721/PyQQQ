# Quantum Bayesian / 量子贝叶斯

> **Quantum ML** / 量子机器学习

## Overview / 概述

Quantum Bayesian Inference / 量子贝叶斯推断

Quantum version of Bayesian updating.

## Application / 应用场景

- Inference (推断)
- Decision making (决策)
- Statistics (统计)

## Code / 代码

```python
from quonic.algorithms import quantum_bayesian_demo

result = quantum_bayesian_demo(prior_h0=0.5, likelihood_h0=0.8, likelihood_h1=0.3)
print(result.counts)
```

## Run / 运行

```bash
python examples/quantum_bayesian/quantum_bayesian.py
```

## Download / 下载

[quantum_bayesian.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_bayesian/quantum_bayesian.py)
