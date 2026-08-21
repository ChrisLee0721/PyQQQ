# Superdense Coding / 超密编码

> **Communication** / 通信 | 难度：中级 | 预计时间：10 分钟

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

超密编码可以用 1 个量子比特传输 2 个经典比特。

**经典局限**：
- 经典通信：1 个比特传输 1 个信息
- 量子通信：1 个量子比特传输 2 个信息

**量子优势**：
- 信息密度翻倍
- 是量子通信的基础

**实际应用**：
- 量子通信
- 量子网络
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import superdense_coding

# 传输 2 个经典比特
result = superdense_coding("11", shots=1024)
print(result.counts)  # {'11': 1024}
```

**预期输出**：

```
{'11': 1024}
```

---

## 原理详解

### 电路图

![Superdense Coding circuit](/images/superdense_coding_circuit.svg)

### 数学推导

**超密编码算法**

目标：用 1 个量子比特传输 2 个经典比特。

**算法步骤**：
1. 初始化：Bell 态 (|00⟩+|11⟩)/√2
2. 编码：根据要传输的信息选择操作
3. 传输：发送 1 个量子比特
4. 解码：Bell 测量
5. 测量：得到 2 个经典比特

**编码方式**：
- 00：不操作
- 01：X 门
- 10：Z 门
- 11：ZX 门

**数学推导**：
|ψ₀⟩ = (|00⟩+|11⟩)/√2
|ψ₁⟩ = (|00⟩+|11⟩)/√2 (00)
|ψ₁⟩ = (|10⟩+|01⟩)/√2 (01)
|ψ₁⟩ = (|00⟩-|11⟩)/√2 (10)
|ψ₁⟩ = (|10⟩-|01⟩)/√2 (11)

### 几何解释

超密编码的几何解释：

1. 初始态：Bell 态
2. 编码：在 Bloch 球上旋转
3. 传输：发送 1 个量子比特
4. 解码：Bell 测量
5. 测量：得到 2 个经典比特

这就像用量子纠缠来压缩信息。

---

## 代码详解

```python
from quonic.algorithms import superdense_coding  # 导入算法

# superdense_coding(message, shots)
# message: 要传输的 2 比特信息
# shots: 测量次数
result = superdense_coding("11", shots=1024)

# result.counts: 测量结果
print(result.counts)  # {'11': 1024}
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `superdense_coding(message, shots)` | message: 要传输的 2 比特信息, shots: 测量次数 | 执行超密编码 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同信息

```python
# 传输 00
result = superdense_coding("00", shots=1024)
print(result.counts)

# 传输 01
result = superdense_coding("01", shots=1024)
print(result.counts)

# 传输 10
result = superdense_coding("10", shots=1024)
print(result.counts)

# 传输 11
result = superdense_coding("11", shots=1024)
print(result.counts)
```

### 场景 2：噪声下的编码

```python
# 无噪声
result = superdense_coding("11", shots=1024, noise=0)
print(result.counts)

# 5% 噪声
result = superdense_coding("11", shots=1024, noise=0.05)
print(result.counts)
```

### 场景 3：超密编码用于量子通信

```python
# 超密编码可以用于量子通信
# 用 1 个量子比特传输 2 个经典比特
```

---

## 适用场景

### 场景 1：量子通信

超密编码可以用于量子通信，提高通信效率。

### 场景 2：量子网络

超密编码可以用于量子网络，提高网络吞吐量。

### 场景 3：量子算法教学

超密编码是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 超密编码的加速比是多少？

信息密度翻倍：1 个量子比特传输 2 个经典比特。

### Q2: 超密编码需要多少量子比特？

需要 2 个量子比特：1 个用于编码，1 个用于传输。

### Q3: 超密编码和隐形传态有什么区别？

超密编码传输经典信息，隐形传态传输量子态。

### Q4: 超密编码在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 超密编码的精度如何？

理想情况下精度为 100%。实际中受噪声影响，精度会降低。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Bell 态
- 量子测量

### 继续学习

- 量子隐形传态
- 量子通信
- 量子网络

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本超密编码

```python
from quonic.algorithms import superdense_coding

result = superdense_coding("11", shots=1024)
print(result.counts)
```

### 示例 2：不同信息

```python
from quonic.algorithms import superdense_coding

result = superdense_coding("00", shots=1024)
print(result.counts)

result = superdense_coding("01", shots=1024)
print(result.counts)

result = superdense_coding("10", shots=1024)
print(result.counts)

result = superdense_coding("11", shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/superdense_coding/superdense_coding.py
```

---

## 下载

- [superdense_coding.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/superdense_coding/superdense_coding.py)
