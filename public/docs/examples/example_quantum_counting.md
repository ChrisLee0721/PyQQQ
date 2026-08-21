# Quantum Counting / 量子计数

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

量子计数用于计算满足条件的解的数量，比经典算法快。

**经典局限**：
- 经典算法：需要 O(N) 次查询
- 量子算法：只需要 O(√N) 次查询

**量子优势**：
- 二次加速：O(√N) vs O(N)
- 是 Grover 搜索的扩展

**实际应用**：
- 优化问题
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import quantum_counting

# 计算满足条件的解的数量
result = quantum_counting(3, "101", shots=1024)
print(result.counts)
```

**预期输出**：

```
{'000': 512, '101': 512}
```

---

## 原理详解

### 电路图

![Quantum Counting circuit](/images/quantum_counting_circuit.svg)

### 数学推导

**量子计数算法**

目标：计算满足条件的解的数量 M。

Oracle：标记满足条件的解

**算法步骤**：
1. 初始化：|0⟩^n |0⟩
2. Hadamard：创建叠加态
3. Grover 迭代：重复 Oracle + Diffusion
4. QFT：提取迭代次数
5. 测量：得到 M 的估计

**数学推导**：
|ψ₀⟩ = |0⟩^n |0⟩
|ψ₁⟩ = |+⟩^n |0⟩
|ψ₂⟩ = Grover^k |+⟩^n
|ψ₃⟩ = QFT |ψ₂⟩

### 几何解释

量子计数的几何解释：

1. 初始态：均匀叠加态
2. Grover 迭代：旋转角度与 M 相关
3. QFT：提取旋转角度
4. 测量：得到 M 的估计

这就像用量子干涉来计数。

---

## 代码详解

```python
from quonic.algorithms import quantum_counting  # 导入算法

# quantum_counting(n_qubits, target, shots)
# n_qubits: 量子比特数
# target: 目标态
# shots: 测量次数
result = quantum_counting(3, "101", shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_counting(n_qubits, target, shots)` | n_qubits: 量子比特数, target: 目标态, shots: 测量次数 | 执行算法 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同目标态

```python
# 1 个目标
result = quantum_counting(3, "101", shots=1024)
print(result.counts)

# 2 个目标
result = quantum_counting(3, ["101", "010"], shots=1024)
print(result.counts)
```

### 场景 2：噪声下的算法

```python
# 无噪声
result = quantum_counting(3, "101", shots=1024, noise=0)
print(result.counts)

# 5% 噪声
result = quantum_counting(3, "101", shots=1024, noise=0.05)
print(result.counts)
```

### 场景 3：算法比较

```python
# 量子计数 vs 经典计数
# 经典：需要 O(N) 次查询
# 量子：只需要 O(√N) 次查询
```

---

## 适用场景

### 场景 1：优化问题

量子计数可以用于计算优化问题的解的数量。

### 场景 2：量子算法教学

量子计数是量子算法的经典例子，用于教学。

### 场景 3：Grover 搜索的扩展

量子计数是 Grover 搜索的扩展。

---

## 常见问题

### Q1: 量子计数的加速比是多少？

二次加速：O(√N) vs O(N)。

### Q2: 量子计数需要多少量子比特？

需要 N+1 个量子比特，其中 N 是搜索空间的大小。

### Q3: 量子计数和 Grover 搜索有什么区别？

量子计数计算解的数量，Grover 搜索找到一个解。

### Q4: 量子计数在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子计数的精度如何？

精度取决于迭代次数和噪声水平。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Grover 搜索
- 量子傅里叶变换

### 继续学习

- 振幅估计
- 量子优化
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本量子计数

```python
from quonic.algorithms import quantum_counting

result = quantum_counting(3, "101", shots=1024)
print(result.counts)
```

### 示例 2：不同目标态

```python
from quonic.algorithms import quantum_counting

result = quantum_counting(3, "101", shots=1024)
print(result.counts)

result = quantum_counting(3, ["101", "010"], shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/quantum_counting/quantum_counting.py
```

---

## 下载

- [quantum_counting.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_counting/quantum_counting.py)
