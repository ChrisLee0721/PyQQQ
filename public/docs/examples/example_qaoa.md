# QAOA / 量子近似优化算法

> **Algorithms** / 算法

## Overview / 概述

Quantum Approximate Optimization Algorithm for combinatorial optimization problems.

量子近似优化算法（QAOA）用于组合优化问题。

## Application / 应用场景

- MaxCut: partition graph vertices (最大割：分割图顶点)
- Traveling salesman (旅行商问题)
- Portfolio optimization (投资组合优化)
- Scheduling problems (调度问题)

## How it works / 原理

QAOA alternates between two operators / QAOA 在两个算子之间交替：

```
|ψ⟩ = e^{-iβ_p H_M} e^{-iγ_p H_C} ... e^{-iβ₁ H_M} e^{-iγ₁ H_C} |+⟩
         ↑                    ↑
      Mixer              Cost
    (探索)             (评估)
```

**Cost Hamiltonian H_C**: encodes the problem (edges to cut)
成本哈密顿量：编码问题（要割的边）

**Mixer Hamiltonian H_M**: explores solution space
混合哈密顿量：探索解空间

**Parameters γ, β**: optimized classically
参数 γ, β：经典优化

## Step-by-step for MaxCut / MaxCut 逐步解析

### Problem / 问题

Graph with edges [(0,1), (1,2), (0,2)]. Find partition that maximizes edges between groups.

图有边 [(0,1), (1,2), (0,2)]。找到使组间边数最大化的分割。

### Step 1: Initialize / 初始化

Apply H to all qubits → equal superposition of all partitions.

对所有量子比特施加 H → 所有分割的等权叠加。

### Step 2: Cost unitary / 成本酉算子

Phase rotation proportional to number of cut edges.

相位旋转与割边数成正比。

### Step 3: Mixer unitary / 混合酉算子

X rotations to explore neighboring solutions.

X 旋转探索邻近解。

### Step 4: Optimize / 优化

Classical optimizer finds best γ, β → highest cut value.

经典优化器找到最佳 γ, β → 最高割值。

## Code / 代码

```python
from quonic.algorithms import qaoa_maxcut

# Triangle graph: edges (0,1), (1,2), (0,2)
# 三角形图：边 (0,1), (1,2), (0,2)
edges = [(0, 1), (1, 2), (0, 2)]

# Run QAOA with 3 qubits, 2 layers
# 运行 QAOA，3 量子比特，2 层
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)
print(result.value)  # ≈ 2.0 (max cut value / 最大割值)
```

## Expected Output / 预期输出

```
Optimization converged.
Max cut value: 2.0
Best partition: {0} | {1, 2}  (or equivalent)
```

The optimal cut puts one vertex in one group and two in the other, cutting 2 edges.

最优分割将一个顶点放在一组，两个放在另一组，割 2 条边。

## Run / 运行

```bash
python examples/qaoa/qaoa.py
```

## Download / 下载

[qaoa.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa/qaoa.py)
