# Bell State / Bell 态

> 两个量子比特，一个 Hadamard 门，一个 CNOT 门 — 量子纠缠的起点

---

## 目录

- [为什么需要 Bell 态？](#为什么需要-bell-态)
- [快速上手](#快速上手)
- [原理详解](#原理详解)
- [全部 4 个 Bell 态](#全部-4-个-bell-态)
- [进阶用法](#进阶用法)
- [适用场景](#适用场景)
- [常见问题](#常见问题)
- [学习路径](#学习路径)
- [完整示例代码](#完整示例代码)

---

## 为什么需要 Bell 态？

在经典物理中，两个物体的状态是**独立的** — 测量一个不会影响另一个。

但在量子世界中，两个量子比特可以进入一种**纠缠态**：测量其中一个，**瞬间**确定另一个的状态。爱因斯坦称之为"鬼魅般的超距作用"（spooky action at a distance）。

**Bell 态**是最简单的纠缠态，也是量子计算的"Hello World"：

```
经典（独立）:          量子（纠缠）:
  q₀: |0⟩ 或 |1⟩       q₀ 和 q₁ 总是相同
  q₁: |0⟩ 或 |1⟩       要么都是 |0⟩，要么都是 |1⟩

测量 q₀ = |0⟩          测量 q₀ = |0⟩
  → q₁ 仍然是随机的       → q₁ 必定是 |0⟩
```

**Bell 态的意义**：
- 是量子隐形传态的基础
- 是超密编码的基础
- 是量子密钥分发的基础
- 违反 Bell 不等式 — 证明量子力学是非局域的

---

## 快速上手

### 最小示例（2 行核心代码）

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)      # Hadamard: 把 q₀ 变成叠加态
qgate(CX, 0, 1)  # CNOT:    让 q₁ 跟着 q₀ 纠缠
qshow()           # 测量并显示结果
```

**预期输出**：

```
backend: native | shots: 1024
Result:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################
```

> 只有 `|00⟩` 和 `|11⟩`，没有 `|01⟩` 和 `|10⟩` — 这证明了纠缠。

### 用算法模板（1 行）

```python
from quonic.algorithms import bell

result = bell(shots=1024)
print(result.counts)  # {'00': ~512, '11': ~512}
```

---

## 原理详解

### 电路图

![Bell State Circuit](/images/bell_circuit.svg)

- **H** = Hadamard 门（创建叠加态）
- **●—⊕** = CNOT 门（创建纠缠）

### 数学推导

**Step 1: 初始态**

两个量子比特都从 `|0⟩` 开始：

```
|ψ₀⟩ = |00⟩
```

**Step 2: Hadamard 门**

对 q₀ 施加 H 门，创建叠加态：

```
|ψ₁⟩ = (|0⟩ + |1⟩)/√2 ⊗ |0⟩
      = (|00⟩ + |10⟩)/√2
```

**Step 3: CNOT 门**

CNOT 门的规则：如果控制比特是 `|1⟩`，就翻转目标比特。

```
|ψ₂⟩ = (|00⟩ + |11⟩)/√2
         ↑        ↑
      q₀=0,q₁=0  q₀=1,q₁=1（被翻转了）
```

**最终态**：`(|00⟩ + |11⟩)/√2` — 这就是 Bell 态 Φ⁺。

### 为什么测量结果只有 |00⟩ 和 |11⟩？

因为量子态是 `(|00⟩ + |11⟩)/√2`：
- 测量时，有 50% 概率坍缩到 `|00⟩`
- 测量时，有 50% 概率坍缩到 `|11⟩`
- **不可能**坍缩到 `|01⟩` 或 `|10⟩`（它们的振幅是 0）

---

## 全部 4 个 Bell 态

| 名称 | 符号 | 电路 | 数学表达式 |
|------|------|------|-----------|
| Bell-1 | Φ⁺ | H, CX | (\|00⟩ + \|11⟩)/√2 |
| Bell-2 | Φ⁻ | H, X, CX | (\|00⟩ - \|11⟩)/√2 |
| Bell-3 | Ψ⁺ | H, CX, X | (\|01⟩ + \|10⟩)/√2 |
| Bell-4 | Ψ⁻ | H, X, CX, X | (\|01⟩ - \|10⟩)/√2 |

### 生成所有 Bell 态

```python
from quonic import qgate, qshow, reset
from quonic.gates import CX, H, X

# Φ⁺: (|00⟩ + |11⟩)/√2
reset()
qgate(H, 0)
qgate(CX, 0, 1)
qshow()  # → |00⟩ 和 |11⟩ 各 50%

# Φ⁻: (|00⟩ - |11⟩)/√2
reset()
qgate(H, 0)
qgate(X, 0)      # 相位翻转
qgate(CX, 0, 1)
qshow()  # → |00⟩ 和 |11⟩ 各 50%（相位不同）

# Ψ⁺: (|01⟩ + |10⟩)/√2
reset()
qgate(H, 0)
qgate(CX, 0, 1)
qgate(X, 1)      # 翻转 q₁
qshow()  # → |01⟩ 和 |10⟩ 各 50%

# Ψ⁻: (|01⟩ - |10⟩)/√2
reset()
qgate(H, 0)
qgate(X, 0)
qgate(CX, 0, 1)
qgate(X, 1)
qshow()  # → |01⟩ 和 |10⟩ 各 50%
```

---

## 进阶用法

### 1. 查看态向量（调试用）

```python
from quonic import qgate, reset
from quonic.gates import CX, H
from quonic.backends import get_backend
from quonic.stack import current_circuit

reset()
qgate(H, 0)
qgate(CX, 0, 1)

backend = get_backend("native")
result = backend.run(current_circuit(), shots=1)
print(result.statevector)
# [0.707+0j, 0+0j, 0+0j, 0.707+0j]
#  ↑ |00⟩                    ↑ |11⟩
```

### 2. 多对 Bell 态（GHZ 的前身）

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

# 3 对 Bell 态：q₀-q₁, q₂-q₃, q₄-q₅
for i in range(0, 6, 2):
    qgate(H, i)
    qgate(CX, i, i + 1)

qshow()
# 结果：|000000⟩, |000011⟩, |001100⟩, |001111⟩,
#       |110000⟩, |110011⟩, |111100⟩, |111111⟩ 各 ~12.5%
```

### 3. Bell 态 + 噪声（测试硬件）

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)

# 无噪声：完美 50/50
qshow(noise=0)

# 5% 噪声：接近 50/50
qshow(noise=0.05)

# 20% 噪声：明显偏离
qshow(noise=0.20)
```

### 4. Bell 态测量（Bell measurement）

用于量子隐形传态的接收端：

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

# 假设 q₀ 和 q₁ 是要测量的 Bell 对
qgate(CX, 0, 1)  # 反向 CNOT
qgate(H, 0)       # 反向 Hadamard
qshow()
# 结果：|00⟩, |01⟩, |10⟩, |11⟩ 各 25%
# 对应 4 种 Bell 态
```

---

## 适用场景

### 1. 量子隐形传态

Bell 态是隐形传态的"量子信道"：

```
Alice 有 |ψ⟩，想传给 Bob
1. Alice 和 Bob 共享 Bell 态
2. Alice 做 Bell 测量
3. Bob 根据测量结果做校正
4. Bob 得到 |ψ⟩
```

### 2. 超密编码

用 1 个量子比特传输 2 个经典比特：

```
Alice 想发 2 比特信息
1. Alice 和 Bob 共享 Bell 态
2. Alice 根据信息选择 4 种操作之一
3. Alice 发送 1 个量子比特给 Bob
4. Bob 做 Bell 测量，得到 2 比特信息
```

### 3. 量子密钥分发（E91）

Bell 态用于检测窃听：

```
1. 发送方和接收方共享 Bell 态
2. 各自随机选择基测量
3. 比较部分结果
4. 如果有窃听 → 结果不一致 → 检测到攻击
```

### 4. 测试量子硬件

Bell 态是测试量子硬件质量的"金标准"：

```python
# 理想：|00⟩ 和 |11⟩ 各 50%
# 实际：如果看到 |01⟩ 和 |10⟩ → 硬件有噪声
qshow(noise=0)    # 理想
qshow(noise=0.05) # 有噪声
```

---

## 常见问题

### Q1: 为什么我的结果不是精确的 50/50？

**A**: 量子测量有随机性。增加 `shots`：

```python
qshow(shots=10000)  # 更接近 50/50
```

### Q2: 为什么我看到了 |01⟩ 或 |10⟩？

**A**: 可能原因：
1. **噪声**：检查是否设置了 `noise` 参数
2. **代码错误**：确认 H 门在 CNOT 之前
3. **后端问题**：试试 `backend='native'`

### Q3: Bell 态和 GHZ 态有什么区别？

| 特性 | Bell 态 | GHZ 态 |
|------|---------|--------|
| 量子比特数 | 2 | 3+ |
| 数学表达式 | (\|00⟩+\|11⟩)/√2 | (\|000⟩+\|111⟩)/√2 |
| 用途 | 两方协议 | 多方纠缠 |

### Q4: 如何验证我制备的是 Bell 态？

**A**: 检查测量结果：
- ✅ 只有 `|00⟩` 和 `|11⟩`
- ✅ 两者概率接近 50%
- ❌ 如果有 `|01⟩` 或 `|10⟩` → 不是 Bell 态

### Q5: Bell 态违反 Bell 不等式是什么意思？

**A**: 经典物理中，两个粒子的关联有一个上限（Bell 不等式）。量子力学的预测**超过**这个上限，实验证实了量子力学的正确性。这意味着**没有局域隐变量理论**能解释量子关联。

---

## 学习路径

### 前置知识

- 量子比特 — 什么是 `|0⟩` 和 `|1⟩`
- 叠加态 — Hadamard 门的作用
- 量子门 — CNOT 门的作用

### 继续学习

- **量子隐形传态** — 用 Bell 态传输量子态
- **超密编码** — 用 Bell 态传输经典信息
- **GHZ 态** — 多量子比特纠缠
- **Bell 不等式** — 量子非局域性的数学证明

### 相关算法

| 算法 | 与 Bell 态的关系 |
|------|-----------------|
| 量子隐形传态 | 使用 Bell 态作为量子信道 |
| 超密编码 | 使用 Bell 态编码 2 比特信息 |
| BB84 QKD | 使用 Bell 态检测窃听 |
| 量子纠错 | Bell 态用于纠缠辅助纠错 |

---

## 完整示例代码

### 文件：`examples/bell/complete_demo.py`

```python
"""
Bell 态完整演示
包含：4 种 Bell 态、噪声测试、态向量查看
"""

from quonic import qgate, qshow, reset
from quonic.gates import CX, H, X
from quonic.backends import get_backend
from quonic.stack import current_circuit


def demo_phi_plus():
    """Φ⁺: (|00⟩ + |11⟩)/√2"""
    print("=" * 50)
    print("1. Bell 态 Φ⁺: (|00⟩ + |11⟩)/√2")
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    result = qshow()
    print(f"测量结果: {result.counts}")
    print()


def demo_phi_minus():
    """Φ⁻: (|00⟩ - |11⟩)/√2"""
    print("=" * 50)
    print("2. Bell 态 Φ⁻: (|00⟩ - |11⟩)/√2")
    reset()
    qgate(H, 0)
    qgate(X, 0)
    qgate(CX, 0, 1)
    result = qshow()
    print(f"测量结果: {result.counts}")
    print()


def demo_psi_plus():
    """Ψ⁺: (|01⟩ + |10⟩)/√2"""
    print("=" * 50)
    print("3. Bell 态 Ψ⁺: (|01⟩ + |10⟩)/√2")
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(X, 1)
    result = qshow()
    print(f"测量结果: {result.counts}")
    print()


def demo_psi_minus():
    """Ψ⁻: (|01⟩ - |10⟩)/√2"""
    print("=" * 50)
    print("4. Bell 态 Ψ⁻: (|01⟩ - |10⟩)/√2")
    reset()
    qgate(H, 0)
    qgate(X, 0)
    qgate(CX, 0, 1)
    qgate(X, 1)
    result = qshow()
    print(f"测量结果: {result.counts}")
    print()


def demo_noise_test():
    """噪声对 Bell 态的影响"""
    print("=" * 50)
    print("5. 噪声测试")
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)

    for noise in [0, 0.05, 0.10, 0.20]:
        result = qshow(noise=noise)
        counts = result.counts
        total = sum(counts.values())
        p00 = counts.get('00', 0) / total
        p11 = counts.get('11', 0) / total
        p_other = 1 - p00 - p11
        print(f"  noise={noise:.2f}: |00⟩={p00:.1%} |11⟩={p11:.1%} 其他={p_other:.1%}")
    print()


def demo_statevector():
    """查看态向量"""
    print("=" * 50)
    print("6. 态向量（调试用）")
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)

    backend = get_backend("native")
    result = backend.run(current_circuit(), shots=1)
    sv = result.statevector
    print(f"  |00⟩ 振幅: {sv[0]:.4f}")
    print(f"  |01⟩ 振幅: {sv[1]:.4f}")
    print(f"  |10⟩ 振幅: {sv[2]:.4f}")
    print(f"  |11⟩ 振幅: {sv[3]:.4f}")
    print(f"  验证: |00⟩ 和 |11⟩ 振幅相等 = {abs(sv[0] - sv[3]) < 1e-10}")
    print()


if __name__ == "__main__":
    demo_phi_plus()
    demo_phi_minus()
    demo_psi_plus()
    demo_psi_minus()
    demo_noise_test()
    demo_statevector()

    print("=" * 50)
    print("✅ 所有示例运行完成！")
```

### 运行方式

```bash
python examples/bell/complete_demo.py
```

---

## 下载

- [bell.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/bell/bell.py) — 基础示例
- [complete_demo.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/bell/complete_demo.py) — 完整演示

---

## 参考文献

- Bell, J. S. (1964). *On the Einstein Podolsky Rosen Paradox*. Physics Physique Физика, 1(3), 195-200.
- Bennett, C. H., et al. (1993). *Teleporting an unknown quantum state via dual classical and Einstein-Podolsky-Rosen channels*. Physical Review Letters, 70(13), 1895.
