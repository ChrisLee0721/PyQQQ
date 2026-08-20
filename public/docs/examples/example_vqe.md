# VQE / 变分量子本征求解器

> **Algorithms** / 算法 | 难度：高级 | 预计时间：15 分钟

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

VQE 是混合量子-经典算法，用于寻找分子的基态能量。

**经典局限**：
- 经典计算分子基态能量：指数复杂度 O(2ⁿ)
- 对于大分子，经典计算不可行

**量子优势**：
- VQE 使用量子计算机计算能量期望值
- 经典优化器更新参数
- 对于 NISQ 设备，VQE 是最实用的算法之一

**实际应用**：
- 量子化学：分子基态能量
- 药物发现：分子性质
- 材料科学：新材料设计

---

## 快速上手

```python
from quonic.algorithms import vqe

# 定义哈密顿量
hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]

# 运行 VQE
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)  # ≈ -2.236
```

**预期输出**：

```
-2.2360679774997894
```

---

## 原理详解

### 电路图

![VQE circuit](/images/vqe_circuit.svg)

### 数学推导

**Step 1: 定义哈密顿量**

H = ZZ + XI + IX

其中 ZZ、XI、IX 是 Pauli 算子的张量积。

**Step 2: 参数化电路**

|ψ(θ⟩ = U(θ)|00⟩

其中 U(θ) 是参数化电路（ansatz）。

**Step 3: 计算能量期望值**

E(θ) = ⟨ψ(θ)|H|ψ(θ)⟩

**Step 4: 经典优化**

使用经典优化器（如 COBYLA）最小化 E(θ)。

**Step 5: 收敛**

当 E(θ) 收敛时，得到基态能量。

### 几何解释

VQE 的几何解释：

1. 参数空间：θ = (θ₁, θ₂, θ₃, θ₄)
2. 能量曲面：E(θ) 是一个曲面
3. 优化过程：在曲面上寻找最低点
4. 收敛：到达最低点，得到基态能量

这就像在山上找最低点，每次走一步，直到到达山谷。

---

## 代码详解

```python
from quonic.algorithms import vqe  # 导入 VQE 算法

# 定义哈密顿量
# [(系数, Pauli 字符串), ...]
hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]

# vqe(hamiltonian, n_qubits, init_params, maxiter)
# hamiltonian: 哈密顿量
# n_qubits: 量子比特数
# init_params: 初始参数
# maxiter: 最大迭代次数
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)

# result.value: 基态能量
print(result.value)  # ≈ -2.236
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `vqe(hamiltonian, n_qubits, init_params, maxiter)` | hamiltonian: 哈密顿量, n_qubits: 量子比特数, init_params: 初始参数, maxiter: 最大迭代次数 | 执行 VQE |
| `result.value` | 无参数 | 基态能量 |

---

## 进阶用法

### 场景 1：不同哈密顿量

```python
# H₂ 分子哈密顿量
hamiltonian = [(-1.0523, "II"), (0.3979, "IZ"), (-0.3979, "ZI"),
               (-0.0112, "ZZ"), (0.1809, "XX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)
```

### 场景 2：不同优化器

```python
# 使用不同优化器
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200, optimizer="cobyla")
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200, optimizer="adam")
```

### 场景 3：不同 ansatz

```python
# 使用不同 ansatz
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200, ansatz="hardware_efficient")
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200, ansatz="uccsd")
```

---

## 适用场景

### 场景 1：量子化学

计算分子的基态能量，用于理解化学反应和分子性质。

### 场景 2：药物发现

计算分子的性质，用于药物设计和筛选。

### 场景 3：材料科学

设计新材料，计算材料的电子结构。

---

## 常见问题

### Q1: VQE 的收敛速度如何？

VQE 的收敛速度取决于 ansatz 和优化器。对于简单问题，通常 100-200 次迭代就能收敛。

### Q2: VQE 需要多少量子比特？

取决于分子的大小。对于 H₂ 分子，需要 2 个量子比特。对于更大的分子，需要更多。

### Q3: VQE 和 QAOA 有什么区别？

VQE 用于寻找基态能量，QAOA 用于组合优化。两者都是变分算法，但应用场景不同。

### Q4: VQE 的精度如何？

VQE 的精度取决于 ansatz 的表达能力和优化器的性能。对于化学精度（1 kcal/mol），通常需要精心设计 ansatz。

### Q5: VQE 在 NISQ 设备上能跑吗？

可以。VQE 是 NISQ 设备上最实用的算法之一，因为它对噪声有一定的鲁棒性。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 哈密顿量和能量期望值
- 经典优化器

### 继续学习

- 量子化学（分子模拟）
- QAOA（组合优化）
- 量子机器学习

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本 VQE

```python
from quonic.algorithms import vqe

hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)
```

### 示例 2：H₂ 分子 VQE

```python
from quonic.algorithms import vqe

hamiltonian = [(-1.0523, "II"), (0.3979, "IZ"), (-0.3979, "ZI"),
               (-0.0112, "ZZ"), (0.1809, "XX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)
```

### 运行方式

```bash
python examples/vqe/vqe.py
```

---

## 下载

- [vqe.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/vqe/vqe.py)
