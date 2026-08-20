# Quantum Teleportation / 量子隐形传态

> **Communication** / 通信

## Overview / 概述

Transfer a quantum state from one qubit to another using entanglement and classical communication.

利用纠缠和经典通信将量子态从一个量子比特传输到另一个。

## Application / 应用场景

- Quantum communication (量子通信)
- Quantum networking (量子网络)
- Distributed quantum computing (分布式量子计算)
- Quantum key distribution (量子密钥分发)

## How it works / 原理

Teleportation uses 3 qubits and 2 classical bits / 隐形传态使用 3 个量子比特和 2 个经典比特：

![Quantum Teleportation Circuit](/images/teleportation_circuit.svg)

```
Alice                          Bob
  q₀ (state to send)           q₂ (receives state)
         │
         ▼
  ┌──────────────┐
  │ Bell pair    │
  │ q₁ ─── q₂   │
  └──────────────┘
         │
    Measure q₀, q₁
         │
    Send 2 classical bits ──────► Apply corrections
                                    X, Z gates
```

## Step-by-step walkthrough / 逐步解析

### Step 1: Prepare state to teleport / 准备要传输的态

Alice has qubit 0 in state |ψ⟩ = cos(π/6)|0⟩ + sin(π/6)|1⟩

Alice 的量子比特 0 处于态 |ψ⟩ = cos(π/6)|0⟩ + sin(π/6)|1⟩

```python
qgate(Ry(math.pi / 3), 0)  # Ry(π/3)|0⟩ = cos(π/6)|0⟩ + sin(π/6)|1⟩
```

### Step 2: Create Bell pair / 创建 Bell 对

Alice and Bob share an entangled pair (qubits 1 and 2):

Alice 和 Bob 共享一对纠缠态（量子比特 1 和 2）：

```python
qgate(H, 1)       # q₁ → (|0⟩ + |1⟩)/√2
qgate(CX, 1, 2)   # q₁,q₂ → (|00⟩ + |11⟩)/√2
```

### Step 3: Alice's operations / Alice 的操作

Alice performs CNOT(q₀,q₁) then H(q₀):

Alice 执行 CNOT(q₀,q₁) 然后 H(q₀)：

```python
qgate(CX, 0, 1)   # Entangle state with Bell pair
qgate(H, 0)        # Create interference
```

### Step 4: Measure and communicate / 测量和通信

Alice measures q₀ and q₁, sends 2 classical bits to Bob.

Alice 测量 q₀ 和 q₁，发送 2 个经典比特给 Bob。

### Step 5: Bob's corrections / Bob 的校正

Bob applies corrections based on Alice's measurement:

Bob 根据 Alice 的测量结果应用校正：

| q₀ | q₁ | Bob applies |
|----|----|----|
| 0 | 0 | Nothing (I) |
| 0 | 1 | X gate |
| 1 | 0 | Z gate |
| 1 | 1 | ZX gates |

## Code / 代码

```python
import math
from quonic import qgate, qshow, reset
from quonic.gates import CX, CZ, H, Ry

# Step 1: Prepare state / 准备态
qgate(Ry(math.pi / 3), 0)

# Step 2: Bell pair / Bell 对
qgate(H, 1)
qgate(CX, 1, 2)

# Step 3: Alice's operations / Alice 的操作
qgate(CX, 0, 1)
qgate(H, 0)

# Step 4-5: Corrections (simplified) / 校正（简化）
qgate(CX, 1, 2)
qgate(CX, 0, 2)
qgate(CZ, 0, 2)

qshow()
```

## Expected Output / 预期输出

After teleportation, qubit 2 has the same state as qubit 0 originally had.

隐形传态后，量子比特 2 拥有与量子比特 0 原来相同的态。

```
backend: native | shots: 1024
Result:
  |000>    256  ( 25.0%)  ##########
  |010>    256  ( 25.0%)  ##########
  |100>    256  ( 25.0%)  ##########
  |110>    256  ( 25.0%)  ##########
```

The state is teleported to qubit 2 (rightmost bit).

态被传输到量子比特 2（最右边的比特）。

## Key insight / 关键洞察

**No faster-than-light communication**: Alice must send 2 classical bits to Bob. The quantum state is destroyed at Alice's end.

**没有超光速通信**：Alice 必须发送 2 个经典比特给 Bob。量子态在 Alice 端被销毁。

## Run / 运行

```bash
python examples/teleportation/teleportation.py
```

## Download / 下载

[teleportation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/teleportation/teleportation.py)
