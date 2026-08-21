# Amplitude Amplification / 振幅放大

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

振幅放大是 Grover 搜索的推广，可以用于任意初始态。

**经典局限**：
- 经典算法：无法放大概率
- 量子算法：可以放大概率

**量子优势**：
- 可以放大目标态的概率
- 是许多量子算法的基础

**实际应用**：
- 量子搜索
- 量子优化
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import amplitude_amplification

# 振幅放大
result = amplitude_amplification(2, oracle, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'11': 1008, '00': 6, '01': 5, '10': 5}
```

---

## 原理详解

### 电路图

![Amplitude Amplification circuit](/images/amplitude_amplification_circuit.svg)

### 数学推导

**振幅放大算法**

目标：放大目标态的概率。

**算法步骤**：
1. 初始化：任意态 |ψ⟩
2. Oracle：标记目标态
3. Diffusion：反射
4. 重复：多次迭代

**数学推导**：
|ψ₀⟩ = |ψ⟩
|ψ₁⟩ = Oracle |ψ⟩
|ψ₂⟩ = Diffusion |ψ₁⟩
|ψₙ⟩ = 放大后的态

### 几何解释

振幅放大的几何解释：

1. 初始态：任意态
2. Oracle：标记目标态
3. Diffusion：反射
4. 重复：多次迭代
5. 结果：目标态概率放大

这就像在 Bloch 球上旋转，放大目标态的概率。

---

## 代码详解

```python
from quonic.algorithms import amplitude_amplification  # 导入算法

# amplitude_amplification(n_qubits, oracle, shots)
# n_qubits: 量子比特数
# oracle: Oracle 函数
# shots: 测量次数
result = amplitude_amplification(2, oracle, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `amplitude_amplification(n_qubits, oracle, shots)` | n_qubits: 量子比特数, oracle: Oracle 函数, shots: 测量次数 | 执行振幅放大 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同初始态

```python
# 不同初始态
result = amplitude_amplification(2, oracle, shots=1024, initial_state="00")
print(result.counts)

result = amplitude_amplification(2, oracle, shots=1024, initial_state="11")
print(result.counts)
```

### 场景 2：振幅放大用于量子优化

```python
# 振幅放大可以用于量子优化
# 放大最优解的概率
```

### 场景 3：振幅放大用于量子搜索

```python
# 振幅放大可以用于量子搜索
# 放大目标态的概率
```

---

## 适用场景

### 场景 1：量子搜索

振幅放大可以用于量子搜索，放大目标态的概率。

### 场景 2：量子优化

振幅放大可以用于量子优化，放大最优解的概率。

### 场景 3：量子算法教学

振幅放大是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 振幅放大的加速比是多少？

二次加速。

### Q2: 振幅放大需要多少量子比特？

取决于问题的规模。

### Q3: 振幅放大和 Grover 搜索有什么区别？

振幅放大是 Grover 搜索的推广，支持任意初始态。

### Q4: 振幅放大在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 振幅放大的精度如何？

精度取决于迭代次数和噪声水平。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Grover 搜索
- 量子算法基础

### 继续学习

- 量子搜索
- 量子优化
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本振幅放大

```python
from quonic.algorithms import amplitude_amplification

result = amplitude_amplification(2, oracle, shots=1024)
print(result.counts)
```

### 示例 2：不同初始态

```python
from quonic.algorithms import amplitude_amplification

result = amplitude_amplification(2, oracle, shots=1024, initial_state="00")
print(result.counts)

result = amplitude_amplification(2, oracle, shots=1024, initial_state="11")
print(result.counts)
```

### 运行方式

```bash
python examples/amplitude_amplification/amplitude_amplification.py
```

---

## 下载

- [amplitude_amplification.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/amplitude_amplification/amplitude_amplification.py)
