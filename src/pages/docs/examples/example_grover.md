# Grover Search / Grover 搜索

> **Algorithms** / 算法

## Overview / 概述

Search an unsorted database in O(√N) queries instead of O(N).

在无序数据库中以 O(√N) 次查询找到目标，经典算法需要 O(N)。

## Application / 应用场景

- Database search (数据库搜索)
- Cryptography: searching key space (密码学：搜索密钥空间)
- Optimization: finding optimal solution (优化：寻找最优解)
- SAT solving (SAT 求解)

## How it works / 原理

Grover's algorithm has two key components / Grover 算法有两个核心组件：

**1. Oracle (神谕)** — marks the target state by flipping its phase / 标记目标态（翻转相位）:
```
|target⟩ → -|target⟩
|other⟩  →  |other⟩
```

**2. Diffusion operator (扩散算子)** — reflects all amplitudes about the mean / 关于平均振幅反射:
```
a_i → 2⟨a⟩ - a_i
```

This amplifies the marked state's probability. After ~√N iterations, measuring gives the target with near-certainty.

经过 ~√N 次迭代，测量几乎必然给出目标态。

## Step-by-step walkthrough / 逐步解析

### Step 1: Initialize superposition / 初始化叠加态

Apply Hadamard to all qubits to create equal superposition:

对所有量子比特施加 Hadamard 门，创建等权叠加：

```
|00⟩ → (|00⟩ + |01⟩ + |10⟩ + |11⟩) / 2
```

### Step 2: Oracle marks target / Oracle 标记目标

For target `|11⟩`, the oracle flips its phase:

对于目标 `|11⟩`，Oracle 翻转其相位：

```
|11⟩ → -|11⟩
```

### Step 3: Diffusion amplifies / 扩散放大

The diffusion operator reflects about the average amplitude. Since `|11⟩` now has negative amplitude, the average drops, and reflection boosts `|11⟩`.

扩散算子关于平均振幅反射。由于 `|11⟩` 的振幅为负，平均值下降，反射后 `|11⟩` 的振幅被放大。

### Step 4: Measure / 测量

After optimal iterations, measure to get the target state with ~99% probability.

最优迭代后测量，以 ~99% 概率获得目标态。

## Code / 代码

```python
from quonic.algorithms import grover

# Search for |11⟩ among 2 qubits
# 在 2 个量子比特中搜索 |11⟩
result = grover("11", 2, shots=1024)
print(result.counts)
# Output: {'11': ~1000, '00': ~8, '01': ~8, '10': ~8}
```

### Manual construction / 手动构造

```python
from quonic import qgate, qshow
from quonic.gates import CX, CZ, H

# Step 1: Superposition / 叠加态
qgate(H, 0)
qgate(H, 1)

# Step 2: Oracle (mark |11⟩) / Oracle 标记 |11⟩
qgate(CZ, 0, 1)  # Phase flip when both qubits are 1

# Step 3: Diffusion / 扩散
qgate(H, 0)
qgate(H, 1)
qgate(CZ, 0, 1)
qgate(H, 0)
qgate(H, 1)

qshow()
```

## Expected Output / 预期输出

Target state appears with ~99% probability after optimal iterations.

目标态在最优迭代后以 ~99% 概率出现。

```
backend: native | shots: 1024
Result:
  |11>    1008  ( 98.4%)  ####################
  |00>       6  (  0.6%)
  |01>       5  (  0.5%)
  |10>       5  (  0.5%)
```

## Classical vs Quantum / 经典 vs 量子

| N | Classical / 经典 | Quantum / 量子 |
|---|---|---|
| 4 | 3 queries | 1 query |
| 1024 | 512 queries | 25 queries |
| 10⁶ | 500,000 queries | 500 queries |

## Run / 运行

```bash
python examples/grover/grover.py
```

## Download / 下载

[grover.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/grover/grover.py)
