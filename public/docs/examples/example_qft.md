# Quantum Fourier Transform / 量子傅里叶变换

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

QFT 是量子版的离散傅里叶变换，是许多量子算法的基础。

**经典局限**：
- 经典 FFT：O(N log N) 复杂度
- 对于 N=2ⁿ，经典需要 O(n 2ⁿ) 次操作

**量子优势**：
- 量子 QFT：O(n²) 复杂度
- 指数加速：O(n²) vs O(n 2ⁿ)
- 是 Shor 算法、量子相位估计的基础

**实际应用**：
- Shor 算法（因式分解）
- 量子相位估计
- 量子计数
- 信号处理

---

## 快速上手

```python
from quonic.algorithms import qft

# 3 量子比特 QFT
result = qft(n_qubits=3, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'000': 128, '001': 128, '010': 128, '011': 128, '100': 128, '101': 128, '110': 128, '111': 128}
```

---

## 原理详解

### 电路图

![Quantum Fourier Transform circuit](/images/qft_circuit.svg)

### 数学推导

**Step 1: 定义**

QFT 将计算基态变换到傅里叶基态：
|j⟩ → (1/√N) Σₖ e^{2πijk/N} |k⟩

**Step 2: 电路实现**

QFT 电路由 H 门和受控相位旋转组成：
- H 门：创建叠加态
- 受控相位旋转：编码频率信息

**Step 3: 3 量子比特 QFT**

|000⟩ → (|000⟩+|001⟩+|010⟩+|011⟩+|100⟩+|101⟩+|110⟩+|111⟩)/√8

**Step 4: 测量**

测量结果均匀分布，每个状态概率 = 1/8。

### 几何解释

QFT 的几何解释：

1. 计算基态：在 z 轴上的点
2. 傅里叶基态：在 xy 平面上的点
3. QFT：将 z 轴上的点旋转到 xy 平面

这就像将时域信号变换到频域。

---

## 代码详解

```python
from quonic.algorithms import qft  # 导入 QFT 算法

# qft(n_qubits, shots)
# n_qubits: 量子比特数
# shots: 测量次数
result = qft(n_qubits=3, shots=1024)

# result.counts: 测量结果的统计
# 例如：{'000': 128, '001': 128, ...}
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qft(n_qubits, shots)` | n_qubits: 量子比特数, shots: 测量次数 | 执行 QFT |
| `result.counts` | 无参数 | 测量结果的统计 |

---

## 进阶用法

### 场景 1：不同量子比特数

```python
# 2 量子比特 QFT
result = qft(n_qubits=2, shots=1024)
print(result.counts)

# 4 量子比特 QFT
result = qft(n_qubits=4, shots=1024)
print(result.counts)
```

### 场景 2：QFT 用于相位估计

```python
# QFT 是量子相位估计的核心
# 用于估计酉算子的本征值
```

### 场景 3：逆 QFT

```python
# 逆 QFT 用于从傅里叶基态变换回计算基态
# 在 Shor 算法中使用
```

---

## 适用场景

### 场景 1：Shor 算法

QFT 是 Shor 算法的核心，用于从周期性态中提取周期信息。

### 场景 2：量子相位估计

QFT 用于估计酉算子的本征值，是量子化学和量子模拟的基础。

### 场景 3：信号处理

QFT 可以用于量子信号处理，实现量子版的傅里叶变换。

---

## 常见问题

### Q1: QFT 和经典 FFT 有什么区别？

QFT 是量子版的 FFT，复杂度 O(n²) vs O(n 2ⁿ)，指数加速。

### Q2: QFT 需要多少量子比特？

取决于问题规模。对于 N=2ⁿ 个数据点，需要 n 个量子比特。

### Q3: QFT 的输出是什么？

QFT 的输出是傅里叶系数，测量结果均匀分布。

### Q4: QFT 在 Shor 算法中怎么用？

Shor 算法使用 QFT 从周期性态中提取周期信息，用于因式分解。

### Q5: QFT 的精度如何？

QFT 的精度取决于量子比特数。量子比特越多，精度越高。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Hadamard 门和受控相位旋转
- 傅里叶变换的基本概念

### 继续学习

- 量子相位估计
- Shor 算法
- 量子计数

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本 QFT

```python
from quonic.algorithms import qft

result = qft(n_qubits=3, shots=1024)
print(result.counts)
```

### 示例 2：4 量子比特 QFT

```python
from quonic.algorithms import qft

result = qft(n_qubits=4, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/qft/qft.py
```

---

## 下载

- [qft.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qft/qft.py)
