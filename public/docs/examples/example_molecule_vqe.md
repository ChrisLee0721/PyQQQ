# Molecular VQE / 分子 VQE

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

分子 VQE 用于计算分子的基态能量。

**经典局限**：
- 经典计算：指数复杂度
- 量子计算：多项式复杂度

**量子优势**：
- 可以计算分子的基态能量
- 是量子化学的基础

**实际应用**：
- 量子化学
- 药物发现
- 材料科学

---

## 快速上手

```python
from quonic.algorithms import molecule_vqe

# 分子 VQE
result = molecule_vqe("H2", shots=1024)
print(result.value)  # 基态能量
```

**预期输出**：

```
-1.137
```

---

## 原理详解

### 电路图

![Molecular VQE circuit](/images/molecule_vqe_circuit.svg)

### 数学推导

**分子 VQE 算法**

目标：计算分子的基态能量。

**算法步骤**：
1. 构建分子哈密顿量
2. 设计 ansatz
3. 运行 VQE
4. 得到基态能量

**数学推导**：
E = ⟨ψ(θ)|H|ψ(θ)⟩
minimize E over θ

### 几何解释

分子 VQE 的几何解释：

1. 参数空间：θ = (θ₁, θ₂, ...)
2. 能量曲面：E(θ)
3. 优化：找到最低点
4. 结果：基态能量

这就像在山上找最低点。

---

## 代码详解

```python
from quonic.algorithms import molecule_vqe  # 导入算法

# molecule_vqe(molecule, shots)
# molecule: 分子名称
# shots: 测量次数
result = molecule_vqe("H2", shots=1024)

# result.value: 基态能量
print(result.value)  # -1.137
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `molecule_vqe(molecule, shots)` | molecule: 分子名称, shots: 测量次数 | 执行分子 VQE |
| `result.value` | 无参数 | 基态能量 |

---

## 进阶用法

### 场景 1：不同分子

```python
# H₂ 分子
result = molecule_vqe("H2", shots=1024)
print(result.value)

# LiH 分子
result = molecule_vqe("LiH", shots=1024)
print(result.value)
```

### 场景 2：不同 ansatz

```python
# 不同 ansatz
result = molecule_vqe("H2", shots=1024, ansatz="uccsd")
print(result.value)

result = molecule_vqe("H2", shots=1024, ansatz="hardware_efficient")
print(result.value)
```

### 场景 3：分子 VQE 用于药物发现

```python
# 分子 VQE 可以用于药物发现
# 计算分子的性质
```

---

## 适用场景

### 场景 1：量子化学

分子 VQE 可以用于计算分子的基态能量。

### 场景 2：药物发现

分子 VQE 可以用于计算分子的性质，用于药物设计。

### 场景 3：材料科学

分子 VQE 可以用于设计新材料。

---

## 常见问题

### Q1: 分子 VQE 的精度如何？

精度取决于 ansatz 和优化器。对于化学精度（1 kcal/mol），通常需要精心设计 ansatz。

### Q2: 分子 VQE 需要多少量子比特？

取决于分子的大小。对于 H₂ 分子，需要 2 个量子比特。

### Q3: 分子 VQE 和 VQE 有什么区别？

分子 VQE 是 VQE 在量子化学中的应用。

### Q4: 分子 VQE 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 分子 VQE 的复杂度如何？

复杂度取决于分子的大小和 ansatz 的设计。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- VQE 算法
- 量子化学基础

### 继续学习

- 量子化学
- 药物发现
- 材料科学

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本分子 VQE

```python
from quonic.algorithms import molecule_vqe

result = molecule_vqe("H2", shots=1024)
print(result.value)
```

### 示例 2：不同分子

```python
from quonic.algorithms import molecule_vqe

result = molecule_vqe("H2", shots=1024)
print(result.value)

result = molecule_vqe("LiH", shots=1024)
print(result.value)
```

### 运行方式

```bash
python examples/molecule_vqe/molecule_vqe.py
```

---

## 下载

- [molecule_vqe.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/molecule_vqe/molecule_vqe.py)
