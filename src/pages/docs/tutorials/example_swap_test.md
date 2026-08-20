# SWAP Test / SWAP 测试

> **Algorithms** / 算法

## Overview / 概述

SWAP Test / SWAP 测试

Estimate overlap between two quantum states.

## Application / 应用场景

- State comparison (态比较)
- Kernel estimation (核估计)
- Fidelity measurement (保真度测量)

## Code / 代码

```python
from quonic import qgate
from quonic.algorithms import swap_test
from quonic.gates import X


# prepare(circuit, qubit_index, n_qubits)
def prep_a(circuit, q, n):
    pass  # |0>

def prep_b(circuit, q, n):
    qgate(X, q)  # |1> — orthogonal to |0>

result = swap_test(1, prep_a, prep_b, shots=10000)
print(result.counts)
```

## Run / 运行

```bash
python examples/swap_test/swap_test.py
```

## Download / 下载

[swap_test.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/swap_test/swap_test.py)
