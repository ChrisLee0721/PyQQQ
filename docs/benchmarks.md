# Performance Benchmarks / 性能基准测试

QuoNic benchmarks cover simulation speed, circuit compilation, algorithm performance, and scheduler optimization.

QuoNic 的基准测试覆盖模拟速度、电路编译、算法性能和调度器优化。

## Code Size: QuoNic vs Qiskit

QuoNic reduces quantum program code by **77%** on average compared to raw Qiskit.

| Example | QuoNic (lines) | Qiskit (lines) | Reduction |
|---------|---------------|----------------|-----------|
| Bell State | 3 | 10 | 3.3x |
| GHZ State (n qubits) | 5 | 11 | 2.2x |
| Grover Search | 3 | 25 | 8.3x |
| QFT (n qubits) | 4 | 20 | 5.0x |
| VQE | 8 | 30 | 3.8x |
| Noise Simulation | 4 | 20 | 5.0x |
| **Total** | **27** | **116** | **4.3x** |

Why is QuoNic shorter?
- No `QuantumCircuit` object — just call `qgate()`
- No manual `measure()` — `qshow()` handles it
- No backend boilerplate — smart scheduling picks the best one
- Built-in algorithms — `grover()`, `qft()`, `vqe()` are one-liners

## Simulation Speed / 模拟速度

### Statevector Simulator / 态向量模拟器

| Qubits | QuoNic Native | Qiskit Aer | Cirq |
|--------|---------------|------------|------|
| 10 | 0.10s | 0.73s | 2.98s |
| 15 | 0.04s | 0.01s | 0.01s |
| 20 | 1.59s | 0.03s | 0.07s |

### MPS Simulator / MPS 模拟器

| Qubits | Entanglement | Time | Bond Dim |
|--------|-------------|------|----------|
| 50 | Low | 0.34s | 2 |
| 100 | Low | 0.73s | 2 |
| 200 | Low | 1.39s | 2 |

## Circuit Compilation / 电路编译

### MCX Decomposition / MCX 分解

| Controls | Standard | Vale (2024) | Reduction |
|----------|----------|-------------|-----------|
| 2 (Toffoli) | 6 CX | 6 CX | 0% |
| 3 | 18 CX | 14 CX | 22% |

### groverize() Performance

| Loop Body | Compile Time | Output Ops | Success Rate |
|-----------|-------------|------------|--------------|
| 100 gates | 0.08s | 103 | 100% |
| 10,000 gates | 0.23s | 30,009 | 99.7% |
| 1,000,000 gates | 14.10s | 1,000,003 | 99.7% |

## FPAA vs Grover

| Initial p | Grover | FPAA | Improvement |
|-----------|--------|------|-------------|
| 0.06 | 95.9% | 99.8% | +3.9% |
| 0.71 | 69.6% | 100% | +30.4% |

---

## Scheduler Benchmarks / 调度器基准

QuoNic 的调度器（`quonic.scheduler`）根据电路特征自动挑后端和方法。它不靠
拍脑袋的固定规则，而是靠两层数据决策：

1. **能力矩阵（静态硬约束）** —— 哪种方法能吃哪些门、是否支持噪声。能力不
   匹配直接排除该方法（例如 `stabilizer` 只吃基础 Clifford 门）。
2. **性能数据（动态软选择）** —— 各方法在参考机上的实测耗时，据此推导交叉
   点阈值，在剩余可用的方法里挑最快。

别人可以抄代码，但很难复制你积累的基准数据——这就是调度器的护城河。

---

## 决策链路

```
电路 ──► circuit_features ──► 能力矩阵(硬) ──► 性能数据(软) ──► 后端 + 方法
                                │                    │
                                └─ 排除不支持的方法     └─ 挑最快（实测交叉点）
```

- **`eligible_methods(gate_types, noise)`**：返回能跑该电路的方法集合（能力）。
- **`recommend_method(features)`**：在能跑的方法里，用实测交叉点选最快。
- **`schedule(circuit)`**：返回 `Recommendation(backend, method)`，一条龙。

---

## 基准套件

`src/quonic/scheduler/benchmark.py` 覆盖「门类型 × 比特数 × 方法」的组合，
五类代表电路族对应三个决策类别：

| 电路族 | 决策类别 | 特征 | 挑战方法 |
|--------|----------|------|----------|
| GHZ（H + CX 链） | `clifford` | 纯基础 Clifford，树宽 1 | `stabilizer` |
| 旋转链 / QAOA（rz + CX 链） | `low_tw` | 非 Clifford 但低树宽 | `matrix_product_state` |
| QFT（全连接 cp） | `general` | 非 Clifford 高树宽 | 仅 `statevector` |
| Grover（ccx + mcz） | `general` | 高树宽非 Clifford | 仅 `statevector` |

### 重新校准

耗时与 CPU / 内存 / BLAS / 后端版本强相关，跨机器会漂移。在你自己的机器上
重跑一次即可校准：

```bash
python -m quonic.scheduler.benchmark -o src/quonic/scheduler/data/benchmarks.json
```

随包附带的 `data/benchmarks.json` 是参考机（Windows 11 / numpy 2.5.2 /
qiskit-aer 0.17.2）上的固化表，冷启动兜底用。

---

## 参考机实测结果

在参考机上实测的交叉点（备选方法首次快于 `statevector` 的最小比特数）：

| 决策类别 | 调度器方法 | 交叉点 | 意义 |
|----------|------------|--------|------|
| `clifford` | `stabilizer` | n ≥ 20 | `statevector` 撞 2^n 墙，stabilizer 多项式增长 |
| `low_tw` | `matrix_product_state` | n ≥ 20 | 低树宽电路 MPS 只需线性资源 |

关键数据点（来自 `benchmarks.json`）：

| n | 类别 | statevector | stabilizer | matrix_product_state |
|---|------|-------------|------------|----------------------|
| 20 | clifford | 0.034s | **0.011s** | 0.022s |
| 24 | clifford | 0.445s | **0.016s** | 0.028s |
| 24 | low_tw | 0.425s | — | **0.009s** |

> 交叉点推导带 20% 的「明显更快」阈值：小 n 时两种方法都在毫秒量级，1% 的
> 计时抖动不该改变路由，只有备选方法至少快 20% 才计为交叉点，避免阈值在
> 小 n 处被噪声来回拨动。

---

## 真实收益验证（`examples/scheduler_demo.py`）

跑三个典型电路，对比「调度器自动选择」与「手动选错 / 默认」的差异：

```bash
python examples/scheduler_demo.py
```

实测输出（参考机）：

```
一、选对方法：调度器 vs 手动默认 statevector
电路         | 调度器自动                          | 手动/默认                          | 加速
--------------------------------------------------------------------------------------------
GHZ(24)    | qiskit:stabilizer              | qiskit:statevector             |  36.4x
           |       14.4 ms          |      523.8 ms          |
QAOA(24)   | qiskit:matrix_product_state    | qiskit:statevector             |  18.7x
           |       34.3 ms          |      640.6 ms          |

二、能力矩阵：Grover(10) 高树宽非 Clifford，调度器留在 statevector
  调度器选择：qiskit:statevector  运行成功 8.4 ms

  手动选错（Aer 不支持 mcz->mcphase，全部崩溃）：
    stabilizer             ✗ QiskitError
    matrix_product_state   ✗ QiskitError
    density_matrix         ✗ QiskitError
```

两条结论：

1. **选对方法带来数量级加速** —— GHZ(24) 快 36 倍、QAOA(24) 快 19 倍。
   默认 `statevector` 在 n=24 撞上 2^24 状态向量墙，而 stabilizer / MPS 用
   多项式资源绕开了它。
2. **调度器避免崩溃** —— Grover 的 `mcz` 在 Aer 里映射成 `mcphase`，只有
   `statevector` 支持；手动选 `stabilizer` / `matrix_product_state` /
   `density_matrix` 都会直接 `QiskitError`。调度器通过能力矩阵把它正确留在
   `statevector`，跑通而不是崩溃。

---

## 高树宽非 Clifford：`general` 验证点

QFT / Grover 只有 `statevector` 能跑（含全连接 `cp` 或 `mcz`），不存在第二个
方法可选，所以基准不是找交叉点，而是**验证「general → statevector」分类**并
记录 statevector 随 n 的 2^n 天花板：

| 电路 | n=8 | n=12 | n=16 |
|------|-----|------|------|
| QFT | 0.010s | 0.019s | 0.038s |
| Grover | 0.006s | 0.009s | 0.016s |

---

## 噪声：`density_matrix` 的 4^n 成本

去极化噪声是硬约束：一旦开启（`schedule(circuit, noise=True)` 或
`qshow(noise=...)`），方法恒为 `density_matrix`——唯一支持噪声的方法。能力
矩阵保证这一点，但**以前调度器对它的成本是盲的**。现在基准实测了
`density_matrix` + 噪声随 n 的 4^n 成本曲线：

| n | 2 | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|----|
| density_matrix | 0.012s | 0.014s | 0.015s | 0.018s | 0.051s | **0.684s** |

每 +2 个比特成本 ×16（4^n）。参考机上 n=12 已超过 0.5s 预算，记为
`infeasible_n = 12`。

调度器在噪声场景下会按实测数据提示成本，而不是盲选：

```python
from quonic.scheduler import load_noise_cost
cost = load_noise_cost()
# {"method": "density_matrix", "noise": 0.01, "budget": 0.5,
#  "performance": [...], "infeasible_n": 12}
```

`qshow(noise=...)` 在 n 超过实测阈值时会打印一句提示（无实测数据则静默）。

---

## 拓扑模型 + 编译 seam（通往硬件的半成品）

不碰真实硬件，但把「电路能否落在受限拓扑上」这件事提前做对——这是将来接
IBM / 国产引擎时路由的前置：

```python
from quonic import CouplingMap
from quonic.compiler import compile

cm = CouplingMap.from_line(4)   # 一维链拓扑
compile(circuit, cm)            # 校验每个多比特门的两两量子比特对是否直接相连
```

- **`CouplingMap`**：无向耦合图，支持 `from_line` / `from_grid` /
  `fully_connected` / `has_edge`。
- **`compile(circuit, coupling_map)`**：目前做连通性校验——放不下时抛
  `RoutingError` 并列出违规的门；`coupling_map=None` 表示全连接（无约束）。
- **留好的扩展点**：SWAP 路由接在 `compile` 之后即可，无需改动 IR 或调度器。

---

## 门分解：`decompose`（可移植核心）

`compile` 只校验拓扑，`decompose` 才负责把高阶门展开成基础门集——这是
QuoNic 自己拥有的「可移植核心」，用户不被某个后端的电路形状绑住：

```python
from quonic import decompose
from quonic.compiler import BASIC_GATES

out = decompose(circuit)        # 返回新的 Circuit，不改动原对象
# out 中的门都落在 BASIC_GATES = {h, x, y, z, rx, ry, rz, p, cx, cz}
```

分解规则（全部精确，无相对相位，可对拍 statevector 验证）：

| 门 | 分解 |
|----|------|
| `cp(θ)` | `p(θ/2)·cx·p(-θ/2)·cx·p(θ/2)`（无 ancilla） |
| `ccx` | 精确 Toffoli（Nielsen-Chuang 图 4.9），用 `p(π/4)` 当 T 门，6 个 `cx` |
| `mcz` | `H·mcx·H`；多控制 mcx 用 AND 级联，k≥3 控制引入 k-2 个干净 ancilla |

多控制 `mcz` 会引入干净 ancilla（起止均为 `|0>`），因此 `decompose` 输出的
比特数可能多于输入。测试用自研 `StatevectorEngine` 当 oracle 对拍：分解前后
`|⟨a|b⟩| == 1`（全局相位无关），且 ancilla 高位必须回到 `|0>`。

**分解的价值**：Grover 的 `mcz` 在 Aer 里映射成 `mcphase`，`stabilizer` /
`matrix_product_state` / `density_matrix` 全部 `QiskitError`。`decompose` 把它
展开成 `cx / h / p / x` 后，同样的电路能直接跑通这三个方法——这就是「可移植
核心」的意义：高阶门是 QuoNic 的语法糖，后端只需支持基础门集。
