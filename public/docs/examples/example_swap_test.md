# SWAP Test / SWAP 测试

> **Algorithms** / 算法 | 难度：中级 | 预计时间：10 分钟

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

SWAP 测试用于估计两个量子态的重叠度，比经典算法快。

**经典局限**：
- 经典算法：需要指数时间
- 量子算法：只需要多项式时间

**量子优势**：
- 多项式加速
- 是量子态比较的基础

**实际应用**：
- 量子态比较
- 量子机器学习
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import swap_test

# 比较两个量子态
result = swap_test(2, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'0': 768, '1': 256}
```

---

## 原理详解

### 电路图

![SWAP Test circuit](/images/swap_test_circuit.svg)

### 数学推导

**SWAP 测试算法**

目标：估计两个量子态 |ψ⟩ 和 |φ⟩ 的重叠度 |⟨ψ|φ⟩|²。

**算法步骤**：
1. 初始化：|0⟩ |ψ⟩ |φ⟩
2. Hadamard：创建叠加态
3. CSWAP：受控 SWAP 门
4. Hadamard：干涉
5. 测量：得到重叠度的估计

**数学推导**：
|ψ₀⟩ = |0⟩ |ψ⟩ |φ⟩
|ψ₁⟩ = (|0⟩+|1⟩)/√2 |ψ⟩ |φ⟩
|ψ₂⟩ = (|0⟩|ψ⟩|φ⟩ + |1⟩|φ⟩|ψ⟩)/√2
|ψ₃⟩ = ((|0⟩+|1⟩)|ψ⟩|φ⟩ + (|0⟩-|1⟩)|φ⟩|ψ⟩)/2

P(0) = (1 + |⟨ψ|φ⟩|²)/2

### 几何解释

SWAP 测试的几何解释：

1. 初始态：|0⟩ |ψ⟩ |φ⟩
2. Hadamard：创建叠加态
3. CSWAP：交换 |ψ⟩ 和 |φ⟩
4. 干涉：放大重叠信息
5. 测量：得到重叠度的估计

这就像用量子干涉来比较两个态。

---

## 代码详解

```python
from quonic.algorithms import swap_test  # 导入算法

# swap_test(n_qubits, shots)
# n_qubits: 量子比特数（每个态的比特数）
# shots: 测量次数
result = swap_test(2, shots=1024)

# result.counts: 测量结果
# P(0) = (1 + |⟨ψ|φ⟩|²)/2
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `swap_test(n_qubits, shots)` | n_qubits: 量子比特数, shots: 测量次数 | 执行 SWAP 测试 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同量子态

```python
# 相同态
result = swap_test(2, shots=1024)
print(result.counts)

# 不同态
result = swap_test(2, shots=1024, state1="00", state2="11")
print(result.counts)
```

### 场景 2：噪声下的测试

```python
# 无噪声
result = swap_test(2, shots=1024, noise=0)
print(result.counts)

# 5% 噪声
result = swap_test(2, shots=1024, noise=0.05)
print(result.counts)
```

### 场景 3：SWAP 测试用于量子机器学习

```python
# SWAP 测试可以用于量子机器学习
# 计算两个量子态的相似度
```

---

## 适用场景

### 场景 1：量子态比较

SWAP 测试可以用于比较两个量子态的相似度。

### 场景 2：量子机器学习

SWAP 测试可以用于量子机器学习中的相似度计算。

### 场景 3：量子算法教学

SWAP 测试是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: SWAP 测试的加速比是多少？

多项式加速。

### Q2: SWAP 测试需要多少量子比特？

需要 2N+1 个量子比特，其中 N 是每个态的比特数。

### Q3: SWAP 测试和 Hadamard 测试有什么区别？

SWAP 测试估计重叠度，Hadamard 测试估计期望值。

### Q4: SWAP 测试在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: SWAP 测试的精度如何？

精度取决于测量次数和噪声水平。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Hadamard 门
- SWAP 门

### 继续学习

- Hadamard 测试
- 量子机器学习
- 量子算法

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本 SWAP 测试

```python
from quonic.algorithms import swap_test

result = swap_test(2, shots=1024)
print(result.counts)
```

### 示例 2：不同量子态

```python
from quonic.algorithms import swap_test

result = swap_test(2, shots=1024, state1="00", state2="11")
print(result.counts)
```

### 运行方式

```bash
python examples/swap_test/swap_test.py
```

---

## 下载

- [swap_test.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/swap_test/swap_test.py)
