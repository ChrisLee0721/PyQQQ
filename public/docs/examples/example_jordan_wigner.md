# Jordan-Wigner / Jordan-Wigner 变换

> **Quantum Chemistry** / 量子化学

## Overview / 概述

Jordan-Wigner transform / Jordan-Wigner 变换

Map fermionic Hamiltonian to qubit Hamiltonian.

## Application / 应用场景

- Quantum chemistry (量子化学)
- Fermionic systems (费米子系统)
- Hubbard model (Hubbard 模型)

## Code / 代码

```python
from quonic.algorithms import jordan_wigner_2site

result = jordan_wigner_2site(t=1.0, U=2.0)
print(result.counts)
```

## Run / 运行

```bash
python examples/jordan_wigner/jordan_wigner.py
```

## Download / 下载

[jordan_wigner.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/jordan_wigner/jordan_wigner.py)
