# 通用优化报告（多比特 / 单比特）

> 生成日期：2026-08-18 ｜ 更新：2026-08-19（全部 P0/P1/P2 已修复）
> 覆盖两部分：① 误差缓解优化（Tuna-17 真机实测归纳）② 后端门/噪声优化（engine 后端 v2 实现审查）。

---

## 第一部分 · 误差缓解优化

数据来源：Tuna-17 真机实测（shots=1024），单比特 groverize（n=2，目标 `00`）与
多比特 groverize（n=4，目标 `1010`）。

### 1. 数据基线

| 方法 method | 单比特 (n=2) | 多比特 (n=4) |
|---|---|---|
| raw | 0.936 | 0.706 |
| 逐比特读出校准 per-qubit readout | 0.982 (+4.6pt) | 0.788 (+8.2pt) |
| 关联读出校准 correlated readout | 0.985 (+4.9pt) | 0.796 (+9.0pt) |
| ZNE 线性外推 linear | 0.917 (−1.9pt) | 0.791 (+8.5pt) |
| ZNE 指数外推 exponential | 0.920 (−1.6pt) | 0.812 (+10.6pt) |
| ZNE 指数 + 关联校准（堆叠 stacked）| **0.963** (+2.7pt) | **0.869** (+16.3pt) |

### 2. 三条通用规律

**规律一：多比特的优化空间 >> 单比特。**
所有方法在多比特上的绝对增益都远大于单比特。根因是 raw 基线差异——单比特 0.936 已贴近
天花板，可优化空间只有 6.4pt；多比特 0.706 有 29.4pt 空间。**优化资源应优先投向多比特 /
深电路。**

**规律二：读出校准与 ZNE 各管一端。**
- 读出校准修**测量端**（读出翻转），对浅电路、读出主导的场景最有效。
- ZNE 修**门端**（门去极化），对深电路、门噪声主导的场景最有效。
- 单比特：读出误差占比高 → 读出校准 +4.6pt，而 ZNE 反而 −1.9pt（折叠引入额外门，得不偿失）。
- 多比特：门误差占比高 → ZNE +8.5pt，读出校准 +8.2pt，两者都有效。

**规律三：指数外推在门噪声主导时明显优于线性。**
多比特 +2.1pt（0.791→0.812），单比特仅 +0.3pt。指数模型 `a·e^(-bλ)+c` 更贴合「噪声随深度
指数累积」的物理。

### 3. 通用优化决策树

```
电路深度 / 噪声主导类型？
├─ 浅电路、读出主导 ──→ 读出校准（逐比特够用）
├─ 深电路、门主导   ──→ ZNE 指数外推
├─ 预算充足          ──→ 堆叠：ZNE 指数 + 关联读出校准
└─ 追求极限          ──→ 设备专属（选高 T2 比特、原生门集、脉冲级校准）
```

### 4. 天花板

- 通用缓解天花板：**多比特 ~87–90%，单比特 ~96%**。
- 关联读出增益很小（多比特 +0.8pt、单比特 +0.3pt）——Tuna-17 读出串扰小，且 2ⁿ 电路排队代价高。
- 噪声 run-to-run 漂移：多比特 raw 三次 0.699 / 0.646 / 0.706，上表是单次快照非常数。

---

## 第二部分 · 后端门/噪声优化

架构现状（v2）：`src/quonic/backends/engine.py` 三路分发 `run()` → clean / `_run_noisy` /
`_run_dynamic`。6 个 engine 后端（qulacs / tensorcircuit / mindquantum / qpanda / cudaq /
cqlib；paddle_quantum 已因 protobuf 冲突移除）各实现了不同子集的 v2 hook。

### 1. 【已修复 ✓】`_measure_qubit` 不塌缩态 → 中段测量结果错误

~~这是最严重的问题~~，**已修复并验证**。

**修复前**（qulacs）：

| 后端 | H(0)+cif(0).then(X,1).else_(Z,1)+H(0)H(1) 输出 |
|---|---|
| native（正确）| `{00,01,10,11}` 各 ~25%（经典混合态）|
| qulacs（错误）| `{00:50, 01:50}`（纯态，2 个结果）|

**修复方案**：qulacs 改用 stateful `QuantumState` + `_measure_and_collapse`（塌缩态后归一化），
不再走 `_measure_qubit`（只算 P 不塌缩）。tensorcircuit 改用 segment-by-segment
DMCircuit 执行。实测修复后两后端均输出 4 个经典混合态 ~25%。全量 459 测试通过。

### 2. 【已修复 ✓】`_apply_readout_noise` 逐 shot 循环

~~O(shots × n) 逐 shot Python 循环~~。改为 numpy `tensordot` + `moveaxis` 沿每个
qubit 轴施加 2×2 混淆矩阵，O(n × 2^n)。无 Python per-shot 循环。

### 3. 【已修复 ✓】`_measure_qubit` 每次从头跑全电路

~~qulacs 的 `_measure_qubit` 每次调用都 `update_quantum_state` 从头执行整条电路~~。
修复后改为 stateful `QuantumState`，每条门直接 `apply_to_state`，测量后塌缩——不再重复跑全电路。

### 4. 【架构】六后端 v2 覆盖不一致

| 后端 | `_create_dm` | `_apply_noise` | `_measure` | `_run_noisy` | `_run_dynamic` |
|---|---|---|---|---|---|
| qulacs | ✓ | ✓ | ✓（塌缩 ✓）| 默认 | ✓ 原生 override |
| tensorcircuit | ✓ | ✓ | ✓ | 默认 | ✓ segment-by-segment |
| mindquantum | ✗ | ✗ | ✓ | ✓ 原生 | 默认 |
| qpanda | ✗ | ✓ | ✓ | 默认 | 默认 |
| cudaq | ✗ | ✗ | ✗ | ✓ 原生 | ✓ 原生 |
| cqlib | ✗ | ✓ | ✓ | 默认 | 默认 |

不一致导致：同一个 `noise=` 请求在不同后端走不同路径，能力边界不透明。**建议维护一张
显式的能力矩阵（或声明式 `CAPABILITIES`），并在不支持时抛出统一错误。**

**已修复**：每个后端声明 `_CAPABILITIES = {"noise": bool, "ctrl": bool, "mid_measure": bool}`，
`run()` 入口检查能力矩阵，不支持时抛 `err.engine_ctrl` / `err.engine_noise` 统一错误。

### 5. 【已修复 ✓】cqlib 不是模拟器

~~`cqlib.Circuit` 没有 `sample()`，v2 hook 全是无效的~~。已改造：cqlib 后端只积累门操作
（`_apply_one` → `self._ops`），`_sample` 委托给 native `StatevectorEngine` 逐门 replay。
`_CAPABILITIES = {"noise": False, "ctrl": False, "mid_measure": False}`。11 个测试全部通过。

### 6. 【已修复 ✓】tensorcircuit 的 numpy 全局 monkey-patch

~~`np.reshape` / `np.ComplexWarning` 全局污染~~。重命名为 `_ensure_tc_numpy_compat()`
（语义更清晰：一次性、幂等、只在首次 TC 操作时触发）。文档说明 patch 不改变 numpy
公共 API 语义（只翻译废弃的 `newshape` 关键字），对其他后端和用户代码透明。

### 7. 【已修复 ✓】测试未跟上 v2

~~`test_cif_raises` / `test_noise_raises` 仍断言 `NotImplementedError`~~。已新增
`tests/test_engine_ctrl.py` 覆盖 cif 正向测试（then/else/叠加混合态）+ 态塌缩回归。
全量 459 测试通过（含 cirq/pennylane 多比特 creg + engine ctrl 测试）。

---

## 优化优先级总表

| 优先级 | 项 | 类型 | 影响 | 状态 |
|---|---|---|---|---|
| **P0** | 修复 `_measure_qubit` 态塌缩 | 正确性 | cif/cmeasure 结果全错 | ✓ 已修复 |
| P0 | 更新测试（cif/noise 正向用例 + 态塌缩回归）| 正确性 | 防回归 | ✓ 已修复 |
| P1 | 向量化 `_apply_readout_noise` | 性能 | O(shots×n) → O(n×2^n) | ✓ 已修复 |
| P1 | 统一六后端能力矩阵 | 架构 | 能力边界透明 | ✓ 已修复 |
| P2 | cqlib 改造为 native 代理 | 架构 | 11 个测试全挂 | ✓ 已修复 |
| P2 | tensorcircuit patch 重命名 + 文档化 | 维护 | 防全局污染 | ✓ 已修复 |
