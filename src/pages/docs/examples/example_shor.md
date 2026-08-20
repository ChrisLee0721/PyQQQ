# Shor's Algorithm / Shor 算法

> **Algorithms** / 算法

## Overview / 概述

Factor integers in polynomial time using quantum period finding. Breaks RSA encryption.

使用量子周期查找在多项式时间内分解整数。能破解 RSA 加密。

## Application / 应用场景

- Cryptography: break RSA encryption (密码学：破解 RSA 加密)
- Number theory: integer factorization (数论：整数分解)
- Security: motivate post-quantum cryptography (安全：推动后量子密码学)

## How it works / 原理

Shor's algorithm has two parts / Shor 算法分两部分：

```
┌─────────────────────────────────────────────────┐
│ Classical part / 经典部分                         │
│ 1. Pick random a < N                             │
│ 2. Compute gcd(a, N) — if >1, done!             │
│ 3. Find period r of a^x mod N ← quantum part    │
│ 4. Compute gcd(a^{r/2} ± 1, N) → factors        │
└─────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│ Quantum part / 量子部分                          │
│ Quantum Period Finding:                          │
│ 1. Superposition of all x                        │
│ 2. Compute a^x mod N                             │
│ 3. QFT to extract period                         │
│ 4. Measure → get period r                        │
└─────────────────────────────────────────────────┘
```

### Example: Factor 15 / 示例：分解 15

1. Pick a=7, N=15
2. Compute 7^x mod 15: 7, 4, 13, 1, 7, 4, ... (period r=4)
3. gcd(7^{4/2} ± 1, 15) = gcd(48, 15) = 3, gcd(50, 15) = 5
4. **15 = 3 × 5**

## Code / 代码

```python
from quonic.algorithms import shor

# Factor 15 using a=7, 6 qubits for period estimation
# 用 a=7 分解 15，6 个量子比特用于周期估计
result = shor(15, a=7, t=6, shots=256)
print(result.value)                    # 3 or 5
print(result.metadata["period"])       # 4 (the order of 7 mod 15)
```

## Expected Output / 预期输出

```
Factor found: 3
Period: 4
Verification: 15 / 3 = 5
```

## Why it matters / 为什么重要

- **Exponential speedup**: Classical factorization is sub-exponential; Shor's is polynomial
  指数加速：经典分解是亚指数的；Shor 是多项式的
- **Threatens RSA**: A sufficiently large quantum computer breaks RSA-2048
  威胁 RSA：足够大的量子计算机能破解 RSA-2048
- **Motivates post-quantum crypto**: NIST is standardizing quantum-resistant algorithms
  推动后量子密码：NIST 正在标准化抗量子算法

## Run / 运行

```bash
python examples/shor/shor.py
```

## Download / 下载

[shor.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/shor/shor.py)
