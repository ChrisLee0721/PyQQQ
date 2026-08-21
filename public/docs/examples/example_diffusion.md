# Diffusion Operator / 扩散算子

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

扩散算子用于 Grover 搜索。

**经典局限**：
- 经典搜索：线性搜索
- 量子搜索：Grover 搜索

**量子优势**：
- 可以加速搜索
- 是量子算法的基础

**实际应用**：
- 量子搜索
- 量子算法
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import diffusion_operator

# 扩散算子
result = diffusion_operator(n_qubits=2, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 256, '01': 256, '10': 256, '11': 256}
```

---

## 原理详解

### 电路图

![Diffusion Operator circuit](/images/diffusion_circuit.svg)

### 数学推导

**扩散算子算法**

目标：构建扩散算子。

**算法步骤**：
1. 初始化：均匀叠加态
2. 反射：关于平均振幅反射
3. 输出：输出扩散算子

**数学推导**：
D = 2|ψ⟩⟨ψ| - I
其中 |ψ⟩ 是均匀叠加态

### 几何解释

扩散算子的几何解释：

1. 初始态：均匀叠加态
2. 反射：关于平均振幅反射
3. 输出：扩散算子

这就像在 Bloch 球上反射。

---

## 代码详解

```python
from quonic.algorithms import diffusion_operator  # 导入算法

# diffusion_operator(n_qubits, shots)
# n_qubits: 量子比特数
# shots: 测量次数
result = diffusion_operator(n_qubits=2, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `diffusion_operator(n_qubits, shots)` | n_qubits: 量子比特数, shots: 测量次数 | 执行扩散算子 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同量子比特数

```python
# 2 量子比特
result = diffusion_operator(n_qubits=2, shots=1024)
print(result.counts)

# 3 量子比特
result = diffusion_operator(n_qubits=3, shots=1024)
print(result.counts)
```

### 场景 2：扩散算子用于 Grover 搜索

```python
# 扩散算子可以用于 Grover 搜索
# 加速搜索
```

### 场景 3：扩散算子用于量子算法

```python
# 扩散算子可以用于量子算法
# 例如：振幅放大
```

---

## 适用场景

### 场景 1：量子搜索

扩散算子可以用于量子搜索。

### 场景 2：量子算法

扩散算子可以用于量子算法。

### 场景 3：量子算法教学

扩散算子是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 扩散算子的精度如何？

精度取决于量子比特数。

### Q2: 扩散算子需要多少量子比特？

取决于问题规模。

### Q3: 扩散算子和 Oracle 有什么区别？

扩散算子反射，Oracle 标记。

### Q4: 扩散算子在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 扩散算子的复杂度如何？

复杂度取决于量子比特数。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Hadamard 门
- Grover 搜索

### 继续学习

- 量子搜索
- 量子算法
- 量子算法教学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本扩散算子

```python
from quonic.algorithms import diffusion_operator

result = diffusion_operator(n_qubits=2, shots=1024)
print(result.counts)
```

### 示例 2：不同量子比特数

```python
from quonic.algorithms import diffusion_operator

result = diffusion_operator(n_qubits=2, shots=1024)
print(result.counts)

result = diffusion_operator(n_qubits=3, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/diffusion/diffusion.py
```

---

## 下载

- [diffusion.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/diffusion/diffusion.py)
