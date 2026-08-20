# Hadamard Test / Hadamard 测试

> **Algorithms** / 算法

## Overview / 概述

Estimate Re(<ψ|U|ψ>) / 估计 Re(<ψ|U|ψ>)

Primitive for inner product estimation.

## Application / 应用场景

- Quantum algorithms (量子算法)
- State overlap (态重叠)
- Expectation values (期望值)

## Code / 代码

```python
from quonic import qgate
from quonic.algorithms import hadamard_test
from quonic.gates import X


# prepare_psi(circuit, qubit_index, n_qubits)
def prep_psi(circuit, q, n):
    qgate(X, q)  # |1>

# apply_u(circuit, qubit_index)
def apply_u(circuit, q):
    pass  # Identity

result = hadamard_test(1, prep_psi, apply_u, shots=10000)
print(result.counts)
```

## Run / 运行

```bash
python examples/hadamard_test/hadamard_test.py
```

## Download / 下载

[hadamard_test.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/hadamard_test/hadamard_test.py)
