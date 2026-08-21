# Hidden Subgroup / 隐藏子群

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

隐藏子群问题是许多量子算法的统一框架。

**经典局限**：
- 经典算法：指数复杂度
- 量子算法：多项式复杂度

**量子优势**：
- 可以解决许多问题
- 是量子算法的基础

**实际应用**：
- 密码学
- 数论
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import hsp

# 隐藏子群问题
result = hsp(group, function, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Hidden Subgroup circuit](/images/hsp_circuit.svg)

### 数学推导

**隐藏子群问题**

目标：找到隐藏的子群 H。

**算法步骤**：
1. 初始化：|0⟩|0⟩
2. Hadamard：创建叠加态
3. Oracle：应用函数
4. Hadamard：干涉
5. 测量：得到子群信息

**数学推导**：
|ψ₀⟩ = |0⟩|0⟩
|ψ₁⟩ = |+⟩|0⟩
|ψ₂⟩ = (1/√|G|) Σ_g |g⟩|f(g)⟩
|ψ₃⟩ = 测量得到子群信息

### 几何解释

隐藏子群问题的几何解释：

1. 初始化：均匀叠加态
2. Oracle：标记子群
3. 干涉：放大子群信息
4. 测量：得到子群

这就像在群中找到隐藏的子群。

---

## 代码详解

```python
from quonic.algorithms import hsp  # 导入算法

# hsp(group, function, shots)
# group: 群
# function: 函数
# shots: 测量次数
result = hsp(group, function, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `hsp(group, function, shots)` | group: 群, function: 函数, shots: 测量次数 | 执行隐藏子群问题 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同群

```python
# 不同群
result = hsp(group1, function, shots=1024)
print(result.counts)

result = hsp(group2, function, shots=1024)
print(result.counts)
```

### 场景 2：隐藏子群用于密码学

```python
# 隐藏子群问题可以用于密码学
# 例如：Shor 算法
```

### 场景 3：隐藏子群用于数论

```python
# 隐藏子群问题可以用于数论
# 例如：因式分解
```

---

## 适用场景

### 场景 1：密码学

隐藏子群问题可以用于密码学，例如 Shor 算法。

### 场景 2：数论

隐藏子群问题可以用于数论，例如因式分解。

### 场景 3：量子算法教学

隐藏子群问题是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 隐藏子群问题的加速比是多少？

指数加速。

### Q2: 隐藏子群问题需要多少量子比特？

取决于群的大小。

### Q3: 隐藏子群问题和 Shor 算法有什么区别？

Shor 算法是隐藏子群问题的特例。

### Q4: 隐藏子群问题在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 隐藏子群问题的复杂度如何？

复杂度取决于群的大小和函数的复杂度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 群论
- 量子算法基础

### 继续学习

- Shor 算法
- 量子密码学
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本隐藏子群问题

```python
from quonic.algorithms import hsp

result = hsp(group, function, shots=1024)
print(result.counts)
```

### 示例 2：不同群

```python
from quonic.algorithms import hsp

result = hsp(group1, function, shots=1024)
print(result.counts)

result = hsp(group2, function, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/hsp/hsp.py
```

---

## 下载

- [hsp.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/hsp/hsp.py)
