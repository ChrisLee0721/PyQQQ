# Hamiltonian Simulation / 哈密顿模拟

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

哈密顿模拟用于模拟量子系统的时间演化。

**经典局限**：
- 经典模拟：指数复杂度
- 量子模拟：多项式复杂度

**量子优势**：
- 可以模拟量子系统的时间演化
- 是量子模拟的基础

**实际应用**：
- 量子化学
- 量子材料科学
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import hamiltonian_simulation

# 哈密顿模拟
result = hamiltonian_simulation(hamiltonian, time=1.0, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Hamiltonian Simulation circuit](/images/hamiltonian_simulation_circuit.svg)

### 数学推导

**哈密顿模拟算法**

目标：模拟 e^{-iHt}。

**算法步骤**：
1. 分解哈密顿量：H = Σᵢ Hᵢ
2. 应用 Trotter 公式
3. 重复多次

**数学推导**：
|ψ₀⟩ = |ψ⟩
|ψ₁⟩ = e^{-iHt} |ψ⟩

### 几何解释

哈密顿模拟的几何解释：

1. 分解：将哈密顿量分解为多个部分
2. 演化：每个部分独立演化
3. 重复：重复多次以提高精度

这就像将连续演化分解为离散步骤。

---

## 代码详解

```python
from quonic.algorithms import hamiltonian_simulation  # 导入算法

# hamiltonian_simulation(hamiltonian, time, shots)
# hamiltonian: 哈密顿量
# time: 演化时间
# shots: 测量次数
result = hamiltonian_simulation(hamiltonian, time=1.0, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `hamiltonian_simulation(hamiltonian, time, shots)` | hamiltonian: 哈密顿量, time: 演化时间, shots: 测量次数 | 执行哈密顿模拟 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同时间

```python
# t=0.1
result = hamiltonian_simulation(hamiltonian, time=0.1, shots=1024)
print(result.counts)

# t=1.0
result = hamiltonian_simulation(hamiltonian, time=1.0, shots=1024)
print(result.counts)

# t=10.0
result = hamiltonian_simulation(hamiltonian, time=10.0, shots=1024)
print(result.counts)
```

### 场景 2：不同哈密顿量

```python
# 不同哈密顿量
result = hamiltonian_simulation(hamiltonian1, time=1.0, shots=1024)
print(result.counts)

result = hamiltonian_simulation(hamiltonian2, time=1.0, shots=1024)
print(result.counts)
```

### 场景 3：哈密顿模拟用于量子化学

```python
# 哈密顿模拟可以用于量子化学
# 模拟分子的时间演化
```

---

## 适用场景

### 场景 1：量子化学

哈密顿模拟可以用于模拟分子的时间演化。

### 场景 2：量子材料科学

哈密顿模拟可以用于模拟材料的性质。

### 场景 3：量子算法教学

哈密顿模拟是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 哈密顿模拟的精度如何？

精度取决于 Trotter 步数。步数越多，精度越高。

### Q2: 哈密顿模拟需要多少量子比特？

取决于哈密顿量的大小。

### Q3: 哈密顿模拟和 Trotterization 有什么区别？

哈密顿模拟是更广泛的概念，Trotterization 是一种实现方法。

### Q4: 哈密顿模拟在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 哈密顿模拟的复杂度如何？

复杂度取决于哈密顿量的大小和 Trotter 步数。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 哈密顿量
- 量子模拟基础

### 继续学习

- 量子化学
- 量子材料科学
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本哈密顿模拟

```python
from quonic.algorithms import hamiltonian_simulation

result = hamiltonian_simulation(hamiltonian, time=1.0, shots=1024)
print(result.counts)
```

### 示例 2：不同时间

```python
from quonic.algorithms import hamiltonian_simulation

result = hamiltonian_simulation(hamiltonian, time=0.1, shots=1024)
print(result.counts)

result = hamiltonian_simulation(hamiltonian, time=1.0, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/hamiltonian_simulation/hamiltonian_simulation.py
```

---

## 下载

- [hamiltonian_simulation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/hamiltonian_simulation/hamiltonian_simulation.py)
