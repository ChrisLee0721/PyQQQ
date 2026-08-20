# VQE / 变分量子本征求解器

> **Algorithms** / 算法

## Overview / 概述

Variational Quantum Eigensolver finds the lowest energy of a quantum system.

变分量子本征求解器（VQE）找到量子系统的最低能量。这是目前量子计算最实用的算法之一。

## Application / 应用场景

- Quantum chemistry: molecular ground states (量子化学：分子基态)
- Materials science: new materials (材料科学：新材料)
- Drug discovery: molecular properties (药物发现：分子性质)
- Optimization: combinatorial problems (优化：组合问题)

## How it works / 原理

VQE is a hybrid quantum-classical algorithm / VQE 是混合量子-经典算法：

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│ Parameterized   │ ──► │ Measure energy   │ ──► │ Classical   │
│ quantum circuit │     │ ⟨ψ(θ)|H|ψ(θ)⟩   │     │ optimizer   │
│                 │ ◄── │                  │ ◄── │ (COBYLA)    │
└─────────────────┘     └──────────────────┘     └─────────────┘
```

**Step 1**: Prepare a parameterized quantum state |ψ(θ)⟩ (ansatz)
准备参数化量子态 |ψ(θ)⟩（拟设）

**Step 2**: Measure the energy expectation ⟨ψ(θ)|H|ψ(θ)⟩
测量能量期望值 ⟨ψ(θ)|H|ψ(θ)⟩

**Step 3**: Classical optimizer updates θ to minimize energy
经典优化器更新 θ 以最小化能量

**Step 4**: Repeat until convergence (ground state found)
重复直到收敛（找到基态）

## Code / 代码

```python
from quonic.algorithms import vqe

# Define Hamiltonian: H = ZZ + XI + IX
# 定义哈密顿量
hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]

# Run VQE with 4 parameters, max 200 iterations
# 运行 VQE，4 个参数，最多 200 次迭代
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)  # ≈ -2.236 (ground state energy / 基态能量)
```

### Understanding the Hamiltonian / 理解哈密顿量

The Pauli operators represent physical interactions / Pauli 算子表示物理相互作用：

| Term | Meaning / 含义 |
|------|---------------|
| `ZZ` | Two-qubit interaction (ZZ 相互作用) |
| `XI` | X-field on qubit 0 (量子比特 0 的 X 场) |
| `IX` | X-field on qubit 1 (量子比特 1 的 X 场) |

## Expected Output / 预期输出

Energy converges to the ground state energy / 能量收敛到基态能量：

```
Iteration   0: energy = -1.234
Iteration  50: energy = -2.198
Iteration 100: energy = -2.234
Iteration 150: energy = -2.236  ← converged
Final energy: -2.236
```

## Why VQE matters / 为什么 VQE 重要

- **NISQ-ready**: Works on today's noisy quantum computers
  适用于当今的含噪声量子计算机
- **Hybrid**: Quantum computer does the hard part, classical does the rest
  混合：量子计算机做困难的部分，经典做其余
- **Scalable**: Can handle molecules too large for classical simulation
  可扩展：能处理经典模拟无法处理的大分子

## Run / 运行

```bash
python examples/vqe/vqe.py
```

## Download / 下载

[vqe.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/vqe/vqe.py)
