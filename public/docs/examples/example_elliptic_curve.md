# Elliptic Curve / 椭圆曲线

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

椭圆曲线用于密码学，量子算法可以指数加速。

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
from quonic.algorithms import elliptic_curve

# 椭圆曲线
result = elliptic_curve(a, b, p, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Elliptic Curve circuit](/images/elliptic_curve_circuit.svg)

### 数学推导

**椭圆曲线算法**

目标：求解椭圆曲线离散对数问题。

**算法步骤**：
1. 初始化：|0⟩|0⟩
2. Hadamard：创建叠加态
3. Oracle：应用椭圆曲线加法
4. QFT：提取周期
5. 测量：得到离散对数

**数学推导**：
|ψ₀⟩ = |0⟩|0⟩
|ψ₁⟩ = |+⟩|0⟩
|ψ₂⟩ = (1/√n) Σ_k |k⟩|kP⟩
|ψ₃⟩ = QFT |ψ₂⟩

### 几何解释

椭圆曲线的几何解释：

1. 椭圆曲线：在有限域上的曲线
2. 点加法：曲线上的群运算
3. 离散对数：找到 k 使得 kP = Q

这就像在曲线上找点。

---

## 代码详解

```python
from quonic.algorithms import elliptic_curve  # 导入算法

# elliptic_curve(a, b, p, shots)
# a, b: 椭圆曲线参数
# p: 有限域
# shots: 测量次数
result = elliptic_curve(a, b, p, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `elliptic_curve(a, b, p, shots)` | a, b: 椭圆曲线参数, p: 有限域, shots: 测量次数 | 执行椭圆曲线算法 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同曲线

```python
# 不同曲线
result = elliptic_curve(1, 1, 23, shots=1024)
print(result.counts)

result = elliptic_curve(2, 3, 23, shots=1024)
print(result.counts)
```

### 场景 2：椭圆曲线用于密码学

```python
# 椭圆曲线可以用于密码学
# 例如：ECC 加密
```

### 场景 3：椭圆曲线用于数论

```python
# 椭圆曲线可以用于数论
# 例如：因式分解
```

---

## 适用场景

### 场景 1：密码学

椭圆曲线可以用于密码学，例如 ECC 加密。

### 场景 2：数论

椭圆曲线可以用于数论，例如因式分解。

### 场景 3：量子算法教学

椭圆曲线是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 椭圆曲线的加速比是多少？

指数加速。

### Q2: 椭圆曲线需要多少量子比特？

取决于曲线的参数。

### Q3: 椭圆曲线和 Shor 算法有什么区别？

椭圆曲线是 Shor 算法的推广。

### Q4: 椭圆曲线在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 椭圆曲线的复杂度如何？

复杂度取决于曲线的参数。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 椭圆曲线
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

### 示例 1：基本椭圆曲线

```python
from quonic.algorithms import elliptic_curve

result = elliptic_curve(1, 1, 23, shots=1024)
print(result.counts)
```

### 示例 2：不同曲线

```python
from quonic.algorithms import elliptic_curve

result = elliptic_curve(1, 1, 23, shots=1024)
print(result.counts)

result = elliptic_curve(2, 3, 23, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/elliptic_curve/elliptic_curve.py
```

---

## 下载

- [elliptic_curve.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/elliptic_curve/elliptic_curve.py)
