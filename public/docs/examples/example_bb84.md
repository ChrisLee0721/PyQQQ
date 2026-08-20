# BB84 QKD / BB84 量子密钥分发

> **Communication** / 通信

## Overview / 概述

BB84 protocol for secure key exchange using quantum mechanics. The first and most famous quantum cryptography protocol.

BB84 协议利用量子力学进行安全密钥交换。第一个也是最著名的量子密码协议。

## Application / 应用场景

- Secure communication (安全通信)
- Quantum cryptography (量子密码学)
- Key distribution (密钥分发)
- Eavesdropping detection (窃听检测)

## How it works / 原理

BB84 uses two bases (Z and X) to encode bits / BB84 使用两个基（Z 和 X）编码比特：

```
Z basis: |0⟩ = 0,  |1⟩ = 1
X basis: |+⟩ = 0,  |-⟩ = 1
```

### Protocol steps / 协议步骤

```
Alice                              Bob
  │                                  │
  ├─ Random bit (0/1)                │
  ├─ Random basis (Z/X)              │
  ├─ Prepare qubit ──────────────► Measure in random basis
  │                                  │
  │    ◄── Classical channel ──── Announce bases
  │                                  │
  ├─ Keep matching bases             ├─ Keep matching bases
  │                                  │
  └─ Shared secret key!              └─ Shared secret key!
```

### Eavesdropping detection / 窃听检测

If Eve intercepts and measures, she introduces errors (50% when bases mismatch). Alice and Bob compare a subset of their key to detect eavesdropping.

如果 Eve 拦截并测量，会引入错误（基不匹配时 50%）。Alice 和 Bob 比较密钥子集以检测窃听。

## Code / 代码

```python
import random
from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit

def bb84_round(alice_basis, alice_bit, bob_basis):
    """Run one round of BB84 / 运行一轮 BB84"""
    reset()

    # Alice prepares / Alice 制备
    if alice_bit == 1:
        qgate(X, 0)          # Encode bit / 编码比特
    if alice_basis == 1:
        qgate(H, 0)          # Switch to X basis / 切换到 X 基

    # Bob measures / Bob 测量
    if bob_basis == 1:
        qgate(H, 0)          # Switch to X basis / 切换到 X 基

    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])

# Run 20 rounds / 运行 20 轮
n_rounds = 20
alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]

bob_results = [bb84_round(alice_bases[i], alice_bits[i], bob_bases[i])
               for i in range(n_rounds)]

# Sifting: keep only matching bases / 筛选：只保留基匹配的
key = [alice_bits[i] for i in range(n_rounds)
       if alice_bases[i] == bob_bases[i]]

print(f"Key: {key}")
```

## Expected Output / 预期输出

```
BB84 Quantum Key Distribution
  Rounds: 20
  Alice bases: [0, 1, 1, 0, 1, ...]
  Alice bits:  [1, 0, 1, 1, 0, ...]
  Bob bases:   [0, 0, 1, 1, 1, ...]
  Matching bases: ~10 (statistically ~50%)
  Key: [1, 1, 0, ...]  (only matching rounds)
```

## Security guarantee / 安全保证

- **No-cloning theorem**: Eve can't copy the qubit
  不可克隆定理：Eve 无法复制量子比特
- **Measurement disturbs**: Eve's measurement changes the state
  测量扰动：Eve 的测量改变态
- **Detectable**: Any eavesdropping introduces ~25% error rate
  可检测：任何窃听引入 ~25% 错误率

## Run / 运行

```bash
python examples/bb84/bb84.py
```

## Download / 下载

[bb84.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/bb84/bb84.py)
