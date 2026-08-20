# Mark State / 标记态

> **Algorithms** / 算法

## Overview / 概述

Mark state / 标记态

## Application / 应用场景

- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Code / 代码

```python
from quonic.algorithms import grover, mark_state

result = grover(mark_state("10"), 2, shots=1024)
print(result.counts)  # dominated by |10>
```

## Run / 运行

```bash
python examples/mark_state/mark_state.py
```

## Download / 下载

[mark_state.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/mark_state/mark_state.py)
