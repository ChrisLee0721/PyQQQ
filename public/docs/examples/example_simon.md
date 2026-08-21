# Simon's Algorithm / Simon 算法

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

Simon 算法用于找到隐藏的周期，比经典算法快指数倍。

**经典局限**：
- 经典算法：需要 O(2^{n/2}) 次查询
- 量子算法：只需要 O(n) 次查询

**量子优势**：
- 指数加速：O(n) vs O(2^{n/2})
- 是 Shor 算法的前身

**实际应用**：
- 密码学
- 量子算法教学
- Shor 算法的基础

---

## 快速上手

```python
from quonic.algorithms import simon

# 找到隐藏的周期 "101"
result = simon("101", shots=1024)
print(result.counts)
```

**预期输出**：

```
{'000': 256, '101': 256, '010': 256, '111': 256}
```

---

## 原理详解

### 电路图

![Simon's Algorithm circuit](/images/simon_circuit.svg)

### 数学推导

**Simon 算法**

目标：找到隐藏的周期 s，使得 f(x) = f(x ⊕ s)。

Oracle：f(x) = f(x ⊕ s)

**算法步骤**：
1. 初始化：|0⟩^n |0⟩^n
2. Hadamard：创建叠加态
3. Oracle：应用 Oracle
4. Hadamard：干涉
5. 测量：得到线性方程
6. 重复：得到足够方程
7. 求解：得到 s

**数学推导**：
|ψ₀⟩ = |0⟩^n |0⟩^n
|ψ₁⟩ = |+⟩^n |0⟩^n
|ψ₂⟩ = (1/√N) Σ_x |x⟩ |f(x)⟩
|ψ₃⟩ = (1/√N) Σ_x (-1)^{y·x} |y⟩

### 几何解释

Simon 算法的几何解释：

1. 初始态：|0⟩^n |0⟩^n
2. Hadamard：创建叠加态
3. Oracle：标记周期
4. 干涉：放大周期信息
5. 测量：得到线性方程
6. 求解：得到周期

这就像用量子干涉来找到隐藏的周期。

---

## 代码详解

```python
from quonic.algorithms import simon  # 导入算法

# simon(period, shots)
# period: 隐藏的周期
# shots: 测量次数
result = simon("101", shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `simon(period, shots)` | period: 隐藏的周期, shots: 测量次数 | 执行算法 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同周期

```python
# 2 比特周期
result = simon("10", shots=1024)
print(result.counts)

# 3 比特周期
result = simon("101", shots=1024)
print(result.counts)

# 4 比特周期
result = simon("1010", shots=1024)
print(result.counts)
```

### 场景 2：噪声下的算法

```python
# 无噪声
result = simon("101", shots=1024, noise=0)
print(result.counts)

# 5% 噪声
result = simon("101", shots=1024, noise=0.05)
print(result.counts)
```

### 场景 3：算法比较

```python
# Simon vs 经典算法
# 经典：需要 O(2^{n/2}) 次查询
# 量子：只需要 O(n) 次查询
```

---

## 适用场景

### 场景 1：密码学

Simon 算法可以用于破解某些密码系统。

### 场景 2：量子算法教学

Simon 算法是量子算法的经典例子，用于教学。

### 场景 3：Shor 算法的基础

Simon 算法是 Shor 算法的前身。

---

## 常见问题

### Q1: Simon 算法的加速比是多少？

指数加速：O(n) vs O(2^{n/2})。

### Q2: Simon 算法需要多少量子比特？

需要 2N 个量子比特，其中 N 是周期的长度。

### Q3: Simon 算法和 Shor 算法有什么区别？

Simon 找隐藏周期，Shor 找整数的周期。

### Q4: Simon 算法在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: Simon 算法的精度如何？

理想情况下精度为 100%。实际中受噪声影响，精度会降低。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Hadamard 门
- 量子测量

### 继续学习

- Shor 算法
- 量子密码学
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本 Simon 算法

```python
from quonic.algorithms import simon

result = simon("101", shots=1024)
print(result.counts)
```

### 示例 2：不同周期

```python
from quonic.algorithms import simon

result = simon("10", shots=1024)
print(result.counts)

result = simon("101", shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/simon/simon.py
```

---

## 下载

- [simon.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/simon/simon.py)
