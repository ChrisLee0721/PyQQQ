# Bb84 / BB84 protocol for secure key exchange using quantum mechanics.

> **Example** / 示例

---

## 目录

- [为什么需要？](#为什么需要)
- [快速上手](#快速上手)
- [原理详解](#原理详解)
- [代码详解](#代码详解)
- [进阶用法](#进阶用法)
- [适用场景](#适用场景)
- [常见问题](#常见问题)
- [学习路径](#学习路径)
- [完整示例代码](#完整示例代码)

---

## 为什么需要？

Quantum key distribution / 量子密钥分发

BB84 protocol for secure key exchange using quantum mechanics.

---

## 快速上手

```python
import random

from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit


def bb84_round(alice_basis, alice_bit, bob_basis):
    """Run one round of BB84.

    Args:
        alice_basis: 0=Z, 1=X
        alice_bit: 0 or 1
        bob_basis: 0=Z, 1=X

    Returns:
        Bob's measurement result.
    """
    reset()

    # Alice prepares
    if alice_bit == 1:
        qgate(X, 0)
    if alice_basis == 1:  # X basis
        qgate(H, 0)

    # Bob measures
    if bob_basis == 1:  # X basis
        qgate(H, 0)

    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])


def main():
    n_rounds = 20
    alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
    alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
    bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]

    # Run protocol
    bob_results = []
    for i in range(n_rounds):
        r = bb84_round(alice_bases[i], alice_bits[i], bob_bases[i])
        bob_results.append(r)

    # Sifting: keep only matching bases
    key = []
    for i in range(n_rounds):
        if alice_bases[i] == bob_bases[i]:
            key.append(alice_bits[i])

    print("BB84 Quantum Key Distribution")
    print(f"  Rounds: {n_rounds}")
    print(f"  Alice bases: {alice_bases}")
    print(f"  Alice bits:  {alice_bits}")
    print(f"  Bob bases:   {bob_bases}")
    print(f"  Bob results: {bob_results}")
    print(f"  Matching bases: {sum(1 for i in range(n_rounds) if alice_bases[i] == bob_bases[i])}")
    print(f"  Key: {key}")


if __name__ == "__main__":
    main()
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Bb84 circuit](/images/bb84_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
import random

from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit


def bb84_round(alice_basis, alice_bit, bob_basis):
    """Run one round of BB84.

    Args:
        alice_basis: 0=Z, 1=X
        alice_bit: 0 or 1
        bob_basis: 0=Z, 1=X

    Returns:
        Bob's measurement result.
    """
    reset()

    # Alice prepares
    if alice_bit == 1:
        qgate(X, 0)
    if alice_basis == 1:  # X basis
        qgate(H, 0)

    # Bob measures
    if bob_basis == 1:  # X basis
        qgate(H, 0)

    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])


def main():
    n_rounds = 20
    alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
    alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
    bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]

    # Run protocol
    bob_results = []
    for i in range(n_rounds):
        r = bb84_round(alice_bases[i], alice_bits[i], bob_bases[i])
        bob_results.append(r)

    # Sifting: keep only matching bases
    key = []
    for i in range(n_rounds):
        if alice_bases[i] == bob_bases[i]:
            key.append(alice_bits[i])

    print("BB84 Quantum Key Distribution")
    print(f"  Rounds: {n_rounds}")
    print(f"  Alice bases: {alice_bases}")
    print(f"  Alice bits:  {alice_bits}")
    print(f"  Bob bases:   {bob_bases}")
    print(f"  Bob results: {bob_results}")
    print(f"  Matching bases: {sum(1 for i in range(n_rounds) if alice_bases[i] == bob_bases[i])}")
    print(f"  Key: {key}")


if __name__ == "__main__":
    main()
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Secure communication (安全通信)
- - Quantum cryptography (量子密码学)
- - Key distribution (密钥分发)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/bb84/bb84.py
```

### Q2: What backend is used?

The example uses the default backend. You can specify a different one:

```python
qshow(backend='qiskit')
```

---

## 学习路径

### 前置知识

- Basic quantum computing concepts
- QuoNic API basics

### 继续学习

- Other examples in this documentation
- QuoNic API reference

---

## 完整示例代码

```python
"""Quantum key distribution / 量子密钥分发

BB84 protocol for secure key exchange using quantum mechanics.
BB84 协议利用量子力学实现安全密钥交换。

## Application / 应用场景
- Secure communication (安全通信)
- Quantum cryptography (量子密码学)
- Key distribution (密钥分发)

## Output / 输出
Shared secret key between Alice and Bob.
Alice 和 Bob 共享的密钥。"""

import random

from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit


def bb84_round(alice_basis, alice_bit, bob_basis):
    """Run one round of BB84.

    Args:
        alice_basis: 0=Z, 1=X
        alice_bit: 0 or 1
        bob_basis: 0=Z, 1=X

    Returns:
        Bob's measurement result.
    """
    reset()

    # Alice prepares
    if alice_bit == 1:
        qgate(X, 0)
    if alice_basis == 1:  # X basis
        qgate(H, 0)

    # Bob measures
    if bob_basis == 1:  # X basis
        qgate(H, 0)

    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])


def main():
    n_rounds = 20
    alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
    alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
    bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]

    # Run protocol
    bob_results = []
    for i in range(n_rounds):
        r = bb84_round(alice_bases[i], alice_bits[i], bob_bases[i])
        bob_results.append(r)

    # Sifting: keep only matching bases
    key = []
    for i in range(n_rounds):
        if alice_bases[i] == bob_bases[i]:
            key.append(alice_bits[i])

    print("BB84 Quantum Key Distribution")
    print(f"  Rounds: {n_rounds}")
    print(f"  Alice bases: {alice_bases}")
    print(f"  Alice bits:  {alice_bits}")
    print(f"  Bob bases:   {bob_bases}")
    print(f"  Bob results: {bob_results}")
    print(f"  Matching bases: {sum(1 for i in range(n_rounds) if alice_bases[i] == bob_bases[i])}")
    print(f"  Key: {key}")


if __name__ == "__main__":
    main()

```

### 运行方式

```bash
python examples/bb84/bb84.py
```

---

## 下载

- [bb84.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/bb84/bb84.py)
