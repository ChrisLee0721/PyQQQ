# Noise Model / 噪声模型

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

噪声模型用于模拟量子噪声。

**经典局限**：
- 经典噪声：无
- 量子噪声：有

**量子优势**：
- 可以模拟量子噪声
- 是量子计算的基础

**实际应用**：
- 量子计算
- 量子算法
- 量子算法教学

---

## 快速上手

```python
from quonic.noise import NoiseModel

# 噪声模型
model = NoiseModel()
model.add_depolarizing("h", p=0.01)
model.add_depolarizing("cx", p=0.02)
print(model)
```

**预期输出**：

```
NoiseModel with 2 noise channels
```

---

## 原理详解

### 电路图

![Noise Model circuit](/images/noise_model_circuit.svg)

### 数学推导

**噪声模型算法**

目标：模拟量子噪声。

**算法步骤**：
1. 定义：定义噪声模型
2. 添加：添加噪声通道
3. 应用：应用噪声模型

**数学推导**：
ρ → (1-p)ρ + p/3(XρX + YρY + ZρZ)
其中 p 是噪声强度

### 几何解释

噪声模型的几何解释：

1. 纯态：在 Bloch 球表面
2. 噪声：向球心移动
3. 混合态：在球心附近

这就像在 Bloch 球上添加噪声。

---

## 代码详解

```python
from quonic.noise import NoiseModel  # 导入噪声模型

# NoiseModel()
model = NoiseModel()

# add_depolarizing(gate, p)
# gate: 门名称
# p: 噪声强度
model.add_depolarizing("h", p=0.01)
model.add_depolarizing("cx", p=0.02)

# model: 噪声模型
print(model)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `NoiseModel()` | 无参数 | 创建噪声模型 |
| `model.add_depolarizing(gate, p)` | gate: 门名称, p: 噪声强度 | 添加去极化噪声 |
| `model.add_readout_error(p0given1, p1given0)` | p0given1: 错误率, p1given0: 错误率 | 添加读出错误 |

---

## 进阶用法

### 场景 1：不同噪声强度

```python
# 不同噪声强度
model1 = NoiseModel()
model1.add_depolarizing("h", p=0.01)
print(model1)

model2 = NoiseModel()
model2.add_depolarizing("h", p=0.05)
print(model2)
```

### 场景 2：噪声模型用于量子计算

```python
# 噪声模型可以用于量子计算
# 模拟噪声
```

### 场景 3：噪声模型用于量子算法

```python
# 噪声模型可以用于量子算法
# 测试算法鲁棒性
```

---

## 适用场景

### 场景 1：量子计算

噪声模型可以用于量子计算。

### 场景 2：量子算法

噪声模型可以用于量子算法。

### 场景 3：量子算法教学

噪声模型是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 噪声模型的精度如何？

精度取决于噪声强度。

### Q2: 噪声模型需要多少量子比特？

取决于电路规模。

### Q3: 噪声模型和噪声有什么区别？

噪声模型是噪声的数学描述。

### Q4: 噪声模型在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 噪声模型的复杂度如何？

复杂度取决于噪声强度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 噪声基础

### 继续学习

- 量子计算
- 量子算法
- 量子算法教学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本噪声模型

```python
from quonic.noise import NoiseModel

model = NoiseModel()
model.add_depolarizing("h", p=0.01)
model.add_depolarizing("cx", p=0.02)
print(model)
```

### 示例 2：不同噪声强度

```python
from quonic.noise import NoiseModel

model1 = NoiseModel()
model1.add_depolarizing("h", p=0.01)
print(model1)

model2 = NoiseModel()
model2.add_depolarizing("h", p=0.05)
print(model2)
```

### 运行方式

```bash
python examples/noise_model/noise_model.py
```

---

## 下载

- [noise_model.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/noise_model/noise_model.py)
