# Jordan-Wigner / Jordan-Wigner 变换

> **Chemistry** / 量子化学 | 难度：高级 | 预计时间：15 分钟

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

Jordan-Wigner 变换用于将费米子算符映射到量子比特算符。

**经典局限**：
- 经典计算：无法直接处理费米子
- 量子计算：可以用量子比特表示费米子

**量子优势**：
- 可以用量子比特表示费米子
- 是量子化学的基础

**实际应用**：
- 量子化学
- 量子材料科学
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import jordan_wigner

# Jordan-Wigner 变换
result = jordan_wigner(hamiltonian, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Jordan-Wigner circuit](/images/jordan_wigner_circuit.svg)

### 数学推导

**Jordan-Wigner 变换**

目标：将费米子算符映射到量子比特算符。

**变换公式**：
aⱼ → (Xⱼ - iYⱼ)/2 × Z₁Z₂...Zⱼ₋₁

**算法步骤**：
1. 定义费米子哈密顿量
2. 应用 Jordan-Wigner 变换
3. 得到量子比特哈密顿量

**数学推导**：
H = Σᵢⱼ hᵢⱼ aᵢ†aⱼ + Σᵢⱼₖₗ hᵢⱼₖₗ aᵢ†aⱼ†aₖaₗ
→ 量子比特哈密顿量

### 几何解释

Jordan-Wigner 变换的几何解释：

1. 费米子：在费米子空间中的算符
2. 量子比特：在量子比特空间中的算符
3. 变换：将费米子算符映射到量子比特算符

这就像将一种语言翻译成另一种语言。

---

## 代码详解

```python
from quonic.algorithms import jordan_wigner  # 导入算法

# jordan_wigner(hamiltonian, shots)
# hamiltonian: 费米子哈密顿量
# shots: 测量次数
result = jordan_wigner(hamiltonian, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `jordan_wigner(hamiltonian, shots)` | hamiltonian: 费米子哈密顿量, shots: 测量次数 | 执行 Jordan-Wigner 变换 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同哈密顿量

```python
# 不同哈密顿量
result = jordan_wigner(hamiltonian1, shots=1024)
print(result.counts)

result = jordan_wigner(hamiltonian2, shots=1024)
print(result.counts)
```

### 场景 2：Jordan-Wigner 用于量子化学

```python
# Jordan-Wigner 变换可以用于量子化学
# 将费米子哈密顿量映射到量子比特哈密顿量
```

### 场景 3：Jordan-Wigner 用于材料科学

```python
# Jordan-Wigner 变换可以用于材料科学
# 模拟材料的电子结构
```

---

## 适用场景

### 场景 1：量子化学

Jordan-Wigner 变换可以用于量子化学，将费米子哈密顿量映射到量子比特哈密顿量。

### 场景 2：量子材料科学

Jordan-Wigner 变换可以用于材料科学，模拟材料的电子结构。

### 场景 3：量子算法教学

Jordan-Wigner 变换是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: Jordan-Wigner 变换的精度如何？

精度取决于变换的实现。

### Q2: Jordan-Wigner 变换需要多少量子比特？

取决于费米子系统的大小。

### Q3: Jordan-Wigner 变换和其他变换有什么区别？

Jordan-Wigner 变换是最简单的费米子-量子比特变换。

### Q4: Jordan-Wigner 变换在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: Jordan-Wigner 变换的复杂度如何？

复杂度取决于费米子系统的大小。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 费米子算符
- 量子化学基础

### 继续学习

- 量子化学
- 量子材料科学
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本 Jordan-Wigner 变换

```python
from quonic.algorithms import jordan_wigner

result = jordan_wigner(hamiltonian, shots=1024)
print(result.counts)
```

### 示例 2：不同哈密顿量

```python
from quonic.algorithms import jordan_wigner

result = jordan_wigner(hamiltonian1, shots=1024)
print(result.counts)

result = jordan_wigner(hamiltonian2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/jordan_wigner/jordan_wigner.py
```

---

## 下载

- [jordan_wigner.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/jordan_wigner/jordan_wigner.py)
