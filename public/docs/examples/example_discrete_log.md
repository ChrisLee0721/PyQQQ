# Discrete Logarithm / 离散对数

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

离散对数问题用于密码学，量子算法可以指数加速。

**经典局限**：
- 经典算法：指数复杂度
- 量子算法：多项式复杂度

**量子优势**：
- 指数加速
- 是密码学的基础

**实际应用**：
- 密码学
- 数论
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import discrete_log

# 离散对数
result = discrete_log(a, b, p, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Discrete Logarithm circuit](/images/discrete_log_circuit.svg)

### 数学推导

**离散对数算法**

目标：找到 x 使得 a^x ≡ b (mod p)。

**算法步骤**：
1. 初始化：|0⟩|0⟩
2. Hadamard：创建叠加态
3. Oracle：应用指数函数
4. QFT：提取周期
5. 测量：得到离散对数

**数学推导**：
|ψ₀⟩ = |0⟩|0⟩
|ψ₁⟩ = |+⟩|0⟩
|ψ₂⟩ = (1/√p) Σ_x |x⟩|a^x mod p⟩
|ψ₃⟩ = QFT |ψ₂⟩

### 几何解释

离散对数的几何解释：

1. 初始化：均匀叠加态
2. Oracle：标记指数函数
3. QFT：提取周期
4. 测量：得到离散对数

这就像用量子干涉来找到离散对数。

---

## 代码详解

```python
from quonic.algorithms import discrete_log  # 导入算法

# discrete_log(a, b, p, shots)
# a: 底数
# b: 结果
# p: 模数
# shots: 测量次数
result = discrete_log(a, b, p, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `discrete_log(a, b, p, shots)` | a: 底数, b: 结果, p: 模数, shots: 测量次数 | 执行离散对数 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同参数

```python
# 不同参数
result = discrete_log(2, 8, 15, shots=1024)
print(result.counts)

result = discrete_log(3, 27, 15, shots=1024)
print(result.counts)
```

### 场景 2：离散对数用于密码学

```python
# 离散对数可以用于密码学
# 例如：Diffie-Hellman 密钥交换
```

### 场景 3：离散对数用于数论

```python
# 离散对数可以用于数论
# 例如：求解同余方程
```

---

## 适用场景

### 场景 1：密码学

离散对数可以用于密码学，例如 Diffie-Hellman 密钥交换。

### 场景 2：数论

离散对数可以用于数论，例如求解同余方程。

### 场景 3：量子算法教学

离散对数是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 离散对数的加速比是多少？

指数加速。

### Q2: 离散对数需要多少量子比特？

取决于参数的大小。

### Q3: 离散对数和 Shor 算法有什么区别？

离散对数是 Shor 算法的推广。

### Q4: 离散对数在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 离散对数的复杂度如何？

复杂度取决于参数的大小。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Shor 算法
- 数论基础

### 继续学习

- 密码学
- 数论
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本离散对数

```python
from quonic.algorithms import discrete_log

result = discrete_log(2, 8, 15, shots=1024)
print(result.counts)
```

### 示例 2：不同参数

```python
from quonic.algorithms import discrete_log

result = discrete_log(2, 8, 15, shots=1024)
print(result.counts)

result = discrete_log(3, 27, 15, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/discrete_log/discrete_log.py
```

---

## 下载

- [discrete_log.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/discrete_log/discrete_log.py)
