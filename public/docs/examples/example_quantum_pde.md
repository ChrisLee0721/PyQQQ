# Quantum PDE / 量子偏微分方程

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

量子 PDE 用于求解偏微分方程。

**经典局限**：
- 经典算法：指数复杂度
- 量子算法：多项式复杂度

**量子优势**：
- 可以求解偏微分方程
- 是量子模拟的基础

**实际应用**：
- 量子模拟
- 量子化学
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import quantum_pde

# 量子 PDE
result = quantum_pde(equation, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Quantum PDE circuit](/images/quantum_pde_circuit.svg)

### 数学推导

**量子 PDE 算法**

目标：求解偏微分方程。

**算法步骤**：
1. 初始化：初始条件
2. 演化：时间演化
3. 测量：得到解

**数学推导**：
∂u/∂t = Lu
u(x,t) = e^{Lt} u(x,0)

### 几何解释

量子 PDE 的几何解释：

1. 初始条件：在函数空间中的点
2. 演化：沿轨迹演化
3. 结果：演化后的函数

这就像在函数空间中跟踪轨迹。

---

## 代码详解

```python
from quonic.algorithms import quantum_pde  # 导入算法

# quantum_pde(equation, shots)
# equation: 偏微分方程
# shots: 测量次数
result = quantum_pde(equation, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_pde(equation, shots)` | equation: 偏微分方程, shots: 测量次数 | 执行量子 PDE |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同方程

```python
# 不同方程
result = quantum_pde(equation1, shots=1024)
print(result.counts)

result = quantum_pde(equation2, shots=1024)
print(result.counts)
```

### 场景 2：量子 PDE 用于量子模拟

```python
# 量子 PDE 可以用于量子模拟
# 模拟量子系统的时间演化
```

### 场景 3：量子 PDE 用于量子化学

```python
# 量子 PDE 可以用于量子化学
# 模拟分子的时间演化
```

---

## 适用场景

### 场景 1：量子模拟

量子 PDE 可以用于量子模拟，模拟量子系统的时间演化。

### 场景 2：量子化学

量子 PDE 可以用于量子化学，模拟分子的时间演化。

### 场景 3：量子算法教学

量子 PDE 是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 量子 PDE 的精度如何？

精度取决于 Trotter 步数。

### Q2: 量子 PDE 需要多少量子比特？

取决于方程的复杂度。

### Q3: 量子 PDE 和经典 PDE 有什么区别？

量子 PDE 有指数加速。

### Q4: 量子 PDE 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子 PDE 的复杂度如何？

复杂度取决于方程的复杂度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 偏微分方程
- 量子模拟基础

### 继续学习

- 量子模拟
- 量子化学
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本量子 PDE

```python
from quonic.algorithms import quantum_pde

result = quantum_pde(equation, shots=1024)
print(result.counts)
```

### 示例 2：不同方程

```python
from quonic.algorithms import quantum_pde

result = quantum_pde(equation1, shots=1024)
print(result.counts)

result = quantum_pde(equation2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/quantum_pde/quantum_pde.py
```

---

## 下载

- [quantum_pde.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_pde/quantum_pde.py)
