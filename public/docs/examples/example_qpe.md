# Quantum Phase Estimation / 量子相位估计

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

QPE 用于估计酉算子的本征值，是许多量子算法的基础。

**经典局限**：
- 经典估计本征值：需要对角化，复杂度 O(N³)
- 对于大矩阵，经典计算不可行

**量子优势**：
- QPE 使用量子计算机估计本征值
- 复杂度 O(N log N)
- 是 Shor 算法、量子化学的基础

**实际应用**：
- Shor 算法（周期查找）
- 量子化学（分子能量）
- 量子模拟（哈密顿量模拟）

---

## 快速上手

```python
import math
from quonic.algorithms import qpe

# 估计 e^{iπ} 的相位
result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)  # 主导：...010
```

**预期输出**：

```
{'010': 1024}
```

---

## 原理详解

### 电路图

![Quantum Phase Estimation circuit](/images/qpe_circuit.svg)

### 数学推导

**Step 1: 定义**

QPE 估计酉算子 U 的本征值 e^{2πiθ}。

**Step 2: 初始化**

控制量子比特处于叠加态，目标量子比特处于本征态。

**Step 3: 受控 U 操作**

对控制量子比特施加受控 U^{2^k} 操作。

**Step 4: 逆 QFT**

对控制量子比特施加逆 QFT。

**Step 5: 测量**

测量控制量子比特，得到 θ 的二进制表示。

### 几何解释

QPE 的几何解释：

1. 控制量子比特：在 xy 平面上旋转
2. 目标量子比特：在 z 轴上
3. 受控 U 操作：旋转角度与 θ 相关
4. 逆 QFT：提取相位信息

这就像用量子干涉来精确测量相位。

---

## 代码详解

```python
import math
from quonic.algorithms import qpe  # 导入 QPE 算法

# qpe(phase, n_precision, shots)
# phase: 要估计的相位
# n_precision: 精度量子比特数
# shots: 测量次数
result = qpe(math.pi, n_precision=3, shots=1024)

# result.counts: 测量结果的统计
# 例如：{'010': 1024}
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qpe(phase, n_precision, shots)` | phase: 要估计的相位, n_precision: 精度量子比特数, shots: 测量次数 | 执行 QPE |
| `result.counts` | 无参数 | 测量结果的统计 |

---

## 进阶用法

### 场景 1：不同精度

```python
# 3 量子比特精度
result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)

# 4 量子比特精度
result = qpe(math.pi, n_precision=4, shots=1024)
print(result.counts)
```

### 场景 2：不同相位

```python
# 估计 π/2
result = qpe(math.pi/2, n_precision=3, shots=1024)
print(result.counts)

# 估计 π/4
result = qpe(math.pi/4, n_precision=3, shots=1024)
print(result.counts)
```

### 场景 3：QPE 用于分子能量

```python
# QPE 可以用于估计分子的基态能量
# 需要构建分子的哈密顿量
# 然后使用 QPE 估计能量
```

---

## 适用场景

### 场景 1：Shor 算法

QPE 是 Shor 算法的核心，用于从周期性态中提取周期信息。

### 场景 2：量子化学

QPE 可以用于估计分子的基态能量，用于理解化学反应。

### 场景 3：量子模拟

QPE 可以用于模拟量子系统的时间演化。

---

## 常见问题

### Q1: QPE 的精度如何？

精度取决于量子比特数。n 个量子比特可以提供 n 位精度。

### Q2: QPE 需要多少量子比特？

取决于精度要求。对于 n 位精度，需要 n 个控制量子比特 + 1 个目标量子比特。

### Q3: QPE 和 VQE 有什么区别？

QPE 用于精确估计本征值，VQE 用于变分估计。QPE 需要更多量子比特，但精度更高。

### Q4: QPE 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响精度。需要纠错量子计算机来跑大规模的。

### Q5: QPE 的复杂度是多少？

O(N log N)，其中 N 是矩阵大小。

---

## 学习路径

### 前置知识

- 量子傅里叶变换
- 受控量子门
- 本征值和本征态

### 继续学习

- Shor 算法
- 量子化学
- 量子模拟

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本 QPE

```python
import math
from quonic.algorithms import qpe

result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)
```

### 示例 2：4 量子比特精度 QPE

```python
import math
from quonic.algorithms import qpe

result = qpe(math.pi, n_precision=4, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/qpe/qpe.py
```

---

## 下载

- [qpe.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qpe/qpe.py)
