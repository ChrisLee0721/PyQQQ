# Bernstein-Vazirani / Bernstein-Vazirani 算法

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

Bernstein-Vazirani 算法用于找到隐藏的比特串，比经典算法快指数倍。

**经典局限**：
- 经典算法：需要 N 次查询
- 量子算法：只需要 1 次查询

**量子优势**：
- 指数加速：O(1) vs O(N)
- 是量子算法的经典例子

**实际应用**：
- 密码学
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import bernstein_vazirani

# 找到隐藏的比特串 "101"
result = bernstein_vazirani("101", shots=1024)
print(result.counts)  # {'101': 1024}
```

**预期输出**：

```
{'101': 1024}
```

---

## 原理详解

### 电路图

![Bernstein-Vazirani circuit](/images/bernstein_vazirani_circuit.svg)

### 数学推导

**Bernstein-Vazirani 算法**

目标：找到隐藏的比特串 s。

Oracle：f(x) = s·x (mod 2)

**算法步骤**：
1. 初始化：所有量子比特处于 |+⟩ 态
2. Oracle：应用 Oracle
3. 测量：得到 s

**数学推导**：
|ψ₀⟩ = |+⟩^n
|ψ₁⟩ = (1/√N) Σ_x (-1)^{s·x} |x⟩
|ψ₂⟩ = |s⟩

### 几何解释

Bernstein-Vazirani 的几何解释：

1. 初始态：均匀叠加态
2. Oracle：标记隐藏的比特串
3. 干涉：放大隐藏比特串的概率
4. 测量：得到隐藏比特串

这就像在叠加态中找到被标记的态。

---

## 代码详解

```python
from quonic.algorithms import bernstein_vazirani  # 导入算法

# bernstein_vazirani(secret, shots)
# secret: 隐藏的比特串
# shots: 测量次数
result = bernstein_vazirani("101", shots=1024)

# result.counts: 测量结果
print(result.counts)  # {'101': 1024}
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `bernstein_vazirani(secret, shots)` | secret: 隐藏的比特串, shots: 测量次数 | 执行算法 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同比特串

```python
# 2 比特
result = bernstein_vazirani("10", shots=1024)
print(result.counts)

# 3 比特
result = bernstein_vazirani("101", shots=1024)
print(result.counts)

# 4 比特
result = bernstein_vazirani("1010", shots=1024)
print(result.counts)
```

### 场景 2：噪声下的算法

```python
# 无噪声
result = bernstein_vazirani("101", shots=1024, noise=0)
print(result.counts)

# 5% 噪声
result = bernstein_vazirani("101", shots=1024, noise=0.05)
print(result.counts)
```

### 场景 3：算法比较

```python
# Bernstein-Vazirani vs 经典算法
# 经典：需要 N 次查询
# 量子：只需要 1 次查询
```

---

## 适用场景

### 场景 1：密码学

Bernstein-Vazirani 算法可以用于破解某些密码系统。

### 场景 2：量子算法教学

Bernstein-Vazirani 算法是量子算法的经典例子，用于教学。

### 场景 3：量子优势演示

Bernstein-Vazirani 算法展示了量子计算的优势。

---

## 常见问题

### Q1: Bernstein-Vazirani 算法的加速比是多少？

指数加速：O(1) vs O(N)。

### Q2: Bernstein-Vazirani 算法需要多少量子比特？

需要 N 个量子比特，其中 N 是隐藏比特串的长度。

### Q3: Bernstein-Vazirani 算法和 Simon 算法有什么区别？

Bernstein-Vazirani 找隐藏比特串，Simon 找隐藏周期。

### Q4: Bernstein-Vazirani 算法在 NISQ 设备上能跑吗？

可以。Bernstein-Vazirani 算法对噪声有一定的鲁棒性。

### Q5: Bernstein-Vazirani 算法的精度如何？

理想情况下精度为 100%。实际中受噪声影响，精度会降低。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Hadamard 门
- 量子测量

### 继续学习

- Simon 算法
- Deutsch-Jozsa 算法
- 量子密码学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本 Bernstein-Vazirani

```python
from quonic.algorithms import bernstein_vazirani

result = bernstein_vazirani("101", shots=1024)
print(result.counts)
```

### 示例 2：不同比特串

```python
from quonic.algorithms import bernstein_vazirani

result = bernstein_vazirani("10", shots=1024)
print(result.counts)

result = bernstein_vazirani("101", shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/bernstein_vazirani/bernstein_vazirani.py
```

---

## 下载

- [bernstein_vazirani.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/bernstein_vazirani/bernstein_vazirani.py)
