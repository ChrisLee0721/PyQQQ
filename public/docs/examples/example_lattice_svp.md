# Lattice SVP / 格最短向量

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

格最短向量问题用于密码学，量子算法可以加速。

**经典局限**：
- 经典算法：指数复杂度
- 量子算法：多项式复杂度

**量子优势**：
- 可以加速格问题
- 是后量子密码学的基础

**实际应用**：
- 后量子密码学
- 格密码学
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import lattice_svp

# 格最短向量
result = lattice_svp(lattice, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Lattice SVP circuit](/images/lattice_svp_circuit.svg)

### 数学推导

**格最短向量算法**

目标：找到格中的最短向量。

**算法步骤**：
1. 初始化：格基
2. 量子搜索：搜索最短向量
3. 测量：得到最短向量

**数学推导**：
L = {Σᵢ xᵢ bᵢ : xᵢ ∈ Z}
找到 v ∈ L 使得 ||v|| 最小

### 几何解释

格最短向量的几何解释：

1. 格：在空间中的离散点集
2. 最短向量：格中最短的非零向量
3. 搜索：在格中搜索最短向量

这就像在点阵中找最近的点。

---

## 代码详解

```python
from quonic.algorithms import lattice_svp  # 导入算法

# lattice_svp(lattice, shots)
# lattice: 格基
# shots: 测量次数
result = lattice_svp(lattice, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `lattice_svp(lattice, shots)` | lattice: 格基, shots: 测量次数 | 执行格最短向量算法 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同格

```python
# 不同格
result = lattice_svp(lattice1, shots=1024)
print(result.counts)

result = lattice_svp(lattice2, shots=1024)
print(result.counts)
```

### 场景 2：格最短向量用于密码学

```python
# 格最短向量可以用于密码学
# 例如：格密码学
```

### 场景 3：格最短向量用于后量子密码学

```python
# 格最短向量可以用于后量子密码学
# 例如：LWE 问题
```

---

## 适用场景

### 场景 1：后量子密码学

格最短向量可以用于后量子密码学，例如 LWE 问题。

### 场景 2：格密码学

格最短向量可以用于格密码学。

### 场景 3：量子算法教学

格最短向量是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 格最短向量的加速比是多少？

多项式加速。

### Q2: 格最短向量需要多少量子比特？

取决于格的维度。

### Q3: 格最短向量和 Shor 算法有什么区别？

格最短向量用于格问题，Shor 算法用于因式分解。

### Q4: 格最短向量在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 格最短向量的复杂度如何？

复杂度取决于格的维度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 格理论
- 后量子密码学

### 继续学习

- 后量子密码学
- 格密码学
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本格最短向量

```python
from quonic.algorithms import lattice_svp

result = lattice_svp(lattice, shots=1024)
print(result.counts)
```

### 示例 2：不同格

```python
from quonic.algorithms import lattice_svp

result = lattice_svp(lattice1, shots=1024)
print(result.counts)

result = lattice_svp(lattice2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/lattice_svp/lattice_svp.py
```

---

## 下载

- [lattice_svp.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/lattice_svp/lattice_svp.py)
