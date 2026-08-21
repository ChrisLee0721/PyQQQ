# Quantum ODE / 量子微分方程

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

量子 ODE 用于求解微分方程。

**经典局限**：
- 经典算法：指数复杂度
- 量子算法：多项式复杂度

**量子优势**：
- 可以求解微分方程
- 是量子模拟的基础

**实际应用**：
- 量子模拟
- 量子化学
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import quantum_ode

# 量子 ODE
result = quantum_ode(equation, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Quantum ODE circuit](/images/quantum_ode_circuit.svg)

### 数学推导

**量子 ODE 算法**

目标：求解微分方程。

**算法步骤**：
1. 初始化：初始条件
2. 演化：时间演化
3. 测量：得到解

**数学推导**：
dy/dt = f(y, t)
y(t) = e^{∫f dt} y(0)

### 几何解释

量子 ODE 的几何解释：

1. 初始条件：在相空间中的点
2. 演化：沿轨迹演化
3. 结果：演化后的点

这就像在相空间中跟踪轨迹。

---

## 代码详解

```python
from quonic.algorithms import quantum_ode  # 导入算法

# quantum_ode(equation, shots)
# equation: 微分方程
# shots: 测量次数
result = quantum_ode(equation, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_ode(equation, shots)` | equation: 微分方程, shots: 测量次数 | 执行量子 ODE |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同方程

```python
# 不同方程
result = quantum_ode(equation1, shots=1024)
print(result.counts)

result = quantum_ode(equation2, shots=1024)
print(result.counts)
```

### 场景 2：量子 ODE 用于量子模拟

```python
# 量子 ODE 可以用于量子模拟
# 模拟量子系统的时间演化
```

### 场景 3：量子 ODE 用于量子化学

```python
# 量子 ODE 可以用于量子化学
# 模拟分子的时间演化
```

---

## 适用场景

### 场景 1：量子模拟

量子 ODE 可以用于量子模拟，模拟量子系统的时间演化。

### 场景 2：量子化学

量子 ODE 可以用于量子化学，模拟分子的时间演化。

### 场景 3：量子算法教学

量子 ODE 是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 量子 ODE 的精度如何？

精度取决于 Trotter 步数。

### Q2: 量子 ODE 需要多少量子比特？

取决于方程的复杂度。

### Q3: 量子 ODE 和经典 ODE 有什么区别？

量子 ODE 有指数加速。

### Q4: 量子 ODE 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子 ODE 的复杂度如何？

复杂度取决于方程的复杂度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 微分方程
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

### 示例 1：基本量子 ODE

```python
from quonic.algorithms import quantum_ode

result = quantum_ode(equation, shots=1024)
print(result.counts)
```

### 示例 2：不同方程

```python
from quonic.algorithms import quantum_ode

result = quantum_ode(equation1, shots=1024)
print(result.counts)

result = quantum_ode(equation2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/quantum_ode/quantum_ode.py
```

---

## 下载

- [quantum_ode.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_ode/quantum_ode.py)
