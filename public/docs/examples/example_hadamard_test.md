# Hadamard Test / Hadamard 测试

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

Hadamard 测试用于估计量子态的期望值，比经典算法快。

**经典局限**：
- 经典算法：需要指数时间
- 量子算法：只需要多项式时间

**量子优势**：
- 多项式加速
- 是量子态期望值估计的基础

**实际应用**：
- 量子态期望值估计
- 量子机器学习
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import hadamard_test

# 估计期望值
result = hadamard_test(2, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'0': 768, '1': 256}
```

---

## 原理详解

### 电路图

![Hadamard Test circuit](/images/hadamard_test_circuit.svg)

### 数学推导

**Hadamard 测试算法**

目标：估计 ⟨ψ|U|ψ⟩。

**算法步骤**：
1. 初始化：|0⟩ |ψ⟩
2. Hadamard：创建叠加态
3. 受控 U：应用受控 U 门
4. Hadamard：干涉
5. 测量：得到期望值的估计

**数学推导**：
|ψ₀⟩ = |0⟩ |ψ⟩
|ψ₁⟩ = (|0⟩+|1⟩)/√2 |ψ⟩
|ψ₂⟩ = (|0⟩|ψ⟩ + |1⟩U|ψ⟩)/√2
|ψ₃⟩ = ((|0⟩+|1⟩)|ψ⟩ + (|0⟩-|1⟩)U|ψ⟩)/2

P(0) = (1 + Re(⟨ψ|U|ψ⟩))/2

### 几何解释

Hadamard 测试的几何解释：

1. 初始态：|0⟩ |ψ⟩
2. Hadamard：创建叠加态
3. 受控 U：应用受控 U 门
4. 干涉：放大期望值信息
5. 测量：得到期望值的估计

这就像用量子干涉来估计期望值。

---

## 代码详解

```python
from quonic.algorithms import hadamard_test  # 导入算法

# hadamard_test(n_qubits, shots)
# n_qubits: 量子比特数
# shots: 测量次数
result = hadamard_test(2, shots=1024)

# result.counts: 测量结果
# P(0) = (1 + Re(⟨ψ|U|ψ⟩))/2
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `hadamard_test(n_qubits, shots)` | n_qubits: 量子比特数, shots: 测量次数 | 执行 Hadamard 测试 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同量子态

```python
# 不同量子态
result = hadamard_test(2, shots=1024)
print(result.counts)

result = hadamard_test(2, shots=1024, state="11")
print(result.counts)
```

### 场景 2：噪声下的测试

```python
# 无噪声
result = hadamard_test(2, shots=1024, noise=0)
print(result.counts)

# 5% 噪声
result = hadamard_test(2, shots=1024, noise=0.05)
print(result.counts)
```

### 场景 3：Hadamard 测试用于量子机器学习

```python
# Hadamard 测试可以用于量子机器学习
# 计算量子态的期望值
```

---

## 适用场景

### 场景 1：量子态期望值估计

Hadamard 测试可以用于估计量子态的期望值。

### 场景 2：量子机器学习

Hadamard 测试可以用于量子机器学习中的期望值计算。

### 场景 3：量子算法教学

Hadamard 测试是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: Hadamard 测试的加速比是多少？

多项式加速。

### Q2: Hadamard 测试需要多少量子比特？

需要 N+1 个量子比特，其中 N 是量子态的比特数。

### Q3: Hadamard 测试和 SWAP 测试有什么区别？

Hadamard 测试估计期望值，SWAP 测试估计重叠度。

### Q4: Hadamard 测试在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: Hadamard 测试的精度如何？

精度取决于测量次数和噪声水平。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Hadamard 门
- 受控门

### 继续学习

- SWAP 测试
- 量子机器学习
- 量子算法

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本 Hadamard 测试

```python
from quonic.algorithms import hadamard_test

result = hadamard_test(2, shots=1024)
print(result.counts)
```

### 示例 2：不同量子态

```python
from quonic.algorithms import hadamard_test

result = hadamard_test(2, shots=1024)
print(result.counts)

result = hadamard_test(2, shots=1024, state="11")
print(result.counts)
```

### 运行方式

```bash
python examples/hadamard_test/hadamard_test.py
```

---

## 下载

- [hadamard_test.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/hadamard_test/hadamard_test.py)
