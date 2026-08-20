# Shor's Algorithm / Shor 算法

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

Shor 算法可以在多项式时间内分解整数，威胁 RSA 加密。

**经典局限**：
- 经典因式分解：亚指数复杂度
- RSA-2048：经典计算机需要数千年

**量子优势**：
- Shor 算法：多项式复杂度 O((log N)³)
- RSA-2048：量子计算机需要数小时

**实际应用**：
- 密码学（破解 RSA）
- 数论（整数分解）
- 后量子密码学（推动新算法）

---

## 快速上手

```python
from quonic.algorithms import shor

# 分解 15
result = shor(15, a=7, t=6, shots=256)
print(result.value)  # 3 或 5
print(result.metadata["period"])  # 4
```

**预期输出**：

```
3
4
```

---

## 原理详解

### 电路图

![Shor's Algorithm circuit](/images/shor_circuit.svg)

### 数学推导

**Step 1: 选择随机数**

选择 a < N，gcd(a, N) = 1。
例如：N=15, a=7

**Step 2: 量子周期查找**

找到 r 使得 a^r ≡ 1 (mod N)。
7^1 = 7 (mod 15)
7^2 = 4 (mod 15)
7^3 = 13 (mod 15)
7^4 = 1 (mod 15)
所以 r = 4

**Step 3: 计算因数**

如果 r 是偶数：
gcd(a^{r/2} ± 1, N) 是 N 的因数。
gcd(7^2 + 1, 15) = gcd(50, 15) = 5
gcd(7^2 - 1, 15) = gcd(48, 15) = 3

**Step 4: 验证**

15 = 3 × 5

### 几何解释

Shor 算法的几何解释：

1. 经典部分：选择随机数 a
2. 量子部分：找到周期 r
3. 后处理：计算因数

量子计算机负责找周期，这是经典计算机做不好的。

---

## 代码详解

```python
from quonic.algorithms import shor  # 导入 Shor 算法

# shor(N, a, t, shots)
# N: 要分解的数
# a: 随机数
# t: 量子比特数
# shots: 测量次数
result = shor(15, a=7, t=6, shots=256)

# result.value: 因数
print(result.value)  # 3 或 5

# result.metadata["period"]: 周期
print(result.metadata["period"])  # 4
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `shor(N, a, t, shots)` | N: 要分解的数, a: 随机数, t: 量子比特数, shots: 测量次数 | 执行 Shor 算法 |
| `result.value` | 无参数 | 因数 |
| `result.metadata["period"]` | 无参数 | 周期 |

---

## 进阶用法

### 场景 1：分解不同数

```python
# 分解 21
result = shor(21, a=2, t=8, shots=256)
print(result.value)  # 3 或 7

# 分解 35
result = shor(35, a=2, t=8, shots=256)
print(result.value)  # 5 或 7
```

### 场景 2：不同随机数

```python
# 使用不同随机数
result = shor(15, a=2, t=6, shots=256)
print(result.value)

result = shor(15, a=4, t=6, shots=256)
print(result.value)
```

### 场景 3：Shor 算法用于密码学

```python
# Shor 算法威胁 RSA 加密
# RSA-2048 需要约 4000 个量子比特
# 目前最大的量子计算机约 1000 个量子比特
```

---

## 适用场景

### 场景 1：密码学

Shor 算法可以破解 RSA 加密，推动后量子密码学的发展。

### 场景 2：数论

Shor 算法可以用于整数分解，解决数论问题。

### 场景 3：后量子密码学

Shor 算法推动了后量子密码学的发展，新的加密算法需要抵抗量子攻击。

---

## 常见问题

### Q1: Shor 算法能分解多大的数？

取决于量子计算机的大小。目前最大的量子计算机约 1000 个量子比特，可以分解较小的数。

### Q2: Shor 算法的复杂度是多少？

O((log N)³)，多项式复杂度。

### Q3: Shor 算法能破解 RSA-2048 吗？

理论上可以，但需要约 4000 个量子比特。目前的量子计算机还不够大。

### Q4: Shor 算法和经典因式分解有什么区别？

Shor 算法是多项式复杂度，经典因式分解是亚指数复杂度。

### Q5: Shor 算法在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。需要纠错量子计算机来跑大规模的。

---

## 学习路径

### 前置知识

- 量子傅里叶变换
- 量子相位估计
- 数论基础

### 继续学习

- 后量子密码学
- 量子计算复杂性
- 量子纠错

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：分解 15

```python
from quonic.algorithms import shor

result = shor(15, a=7, t=6, shots=256)
print(result.value)
print(result.metadata["period"])
```

### 示例 2：分解 21

```python
from quonic.algorithms import shor

result = shor(21, a=2, t=8, shots=256)
print(result.value)
print(result.metadata["period"])
```

### 运行方式

```bash
python examples/shor/shor.py
```

---

## 下载

- [shor.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/shor/shor.py)
