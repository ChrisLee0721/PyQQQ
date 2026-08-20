# Noise Simulation / 噪声模拟

> **Noise** / 噪声 | 难度：中级 | 预计时间：10 分钟

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

噪声模拟是理解量子硬件缺陷的关键。

**经典局限**：
- 经典计算机：没有噪声问题
- 量子计算机：噪声是主要挑战

**量子优势**：
- 噪声模拟可以帮助理解量子硬件的局限
- 噪声模拟可以用于测试纠错算法
- 噪声模拟可以用于优化量子电路

**实际应用**：
- 量子硬件测试
- 量子纠错算法验证
- 量子电路优化

---

## 快速上手

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

# 创建 Bell 态
qgate(H, 0)
qgate(CX, 0, 1)

# 无噪声
qshow(noise=0)

# 5% 噪声
qshow(noise=0.05)

# 20% 噪声
qshow(noise=0.20)
```

**预期输出**：

```
noise=0:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################

noise=0.05:
  |00>     480  ( 46.9%)  ##################
  |11>     480  ( 46.9%)  ##################
  |01>      32  (  3.1%)  #
  |10>      32  (  3.1%)  #

noise=0.20:
  |00>     320  ( 31.3%)  ############
  |11>     320  ( 31.3%)  ############
  |01>     192  ( 18.8%)  #######
  |10>     192  ( 18.8%)  #######
```

---

## 原理详解

### 电路图

![Noise Simulation circuit](/images/noise_circuit.svg)

### 数学推导

**去极化噪声模型**

噪声信道：
ρ → (1-p)ρ + p/3(XρX + YρY + ZρZ)

其中 p 是噪声强度。

**效果**

- p=0：无噪声
- p=0.05：5% 噪声
- p=0.20：20% 噪声

**测量结果**

无噪声：只有 |00⟩ 和 |11⟩
有噪声：出现 |01⟩ 和 |10⟩

### 几何解释

噪声的几何解释（Bloch 球）：

1. 无噪声：态在 Bloch 球表面
2. 有噪声：态向球心移动
3. 噪声越大：态越接近球心（混合态）

这就像信号被噪声干扰，纯态变成混合态。

---

## 代码详解

```python
from quonic import qgate, qshow  # 导入核心 API
from quonic.gates import CX, H   # 导入门定义

# 创建 Bell 态
qgate(H, 0)      # Hadamard 门
qgate(CX, 0, 1)  # CNOT 门

# 噪声模拟
qshow(noise=0)    # 无噪声
qshow(noise=0.05) # 5% 噪声
qshow(noise=0.20) # 20% 噪声
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qshow(noise=0)` | noise: 噪声强度 (0-1) | 无噪声模拟 |
| `qshow(noise=0.05)` | noise: 噪声强度 (0-1) | 5% 噪声模拟 |
| `qshow(noise=0.20)` | noise: 噪声强度 (0-1) | 20% 噪声模拟 |

---

## 进阶用法

### 场景 1：不同噪声强度

```python
# 0% 噪声
qshow(noise=0)

# 1% 噪声
qshow(noise=0.01)

# 5% 噪声
qshow(noise=0.05)

# 10% 噪声
qshow(noise=0.10)

# 20% 噪声
qshow(noise=0.20)
```

### 场景 2：不同电路的噪声影响

```python
# Bell 态
qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=0.05)

# GHZ 态
qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow(noise=0.05)
```

### 场景 3：噪声下的算法

```python
# Grover 搜索在噪声下
from quonic.algorithms import grover
result = grover("11", 2, shots=1024, noise=0.05)
print(result.counts)
```

---

## 适用场景

### 场景 1：量子硬件测试

噪声模拟可以帮助理解量子硬件的局限，优化电路设计。

### 场景 2：量子纠错算法验证

噪声模拟可以用于测试纠错算法的有效性。

### 场景 3：量子电路优化

噪声模拟可以用于优化量子电路，减少噪声影响。

---

## 常见问题

### Q1: 噪声强度 0.05 是什么意思？

表示 5% 的概率发生错误。每个量子比特有 5% 的概率被翻转或相位翻转。

### Q2: 噪声会影响所有量子比特吗？

是的。噪声模型对每个量子比特独立施加噪声。

### Q3: 如何减少噪声影响？

可以使用量子纠错码、误差缓解技术、或优化电路设计。

### Q4: 噪声模型有哪些类型？

常见的有去极化噪声、振幅阻尼、相位阻尼等。

### Q5: 噪声模拟的精度如何？

噪声模拟的精度取决于噪声模型的准确性。去极化噪声模型是简化的模型。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 密度矩阵（可选）

### 继续学习

- 量子纠错
- 误差缓解
- 噪声模型

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本噪声模拟

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=0.05)
```

### 示例 2：不同噪声强度

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=0)
qshow(noise=0.05)
qshow(noise=0.20)
```

### 运行方式

```bash
python examples/noise/noise.py
```

---

## 下载

- [noise.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/noise/noise.py)
