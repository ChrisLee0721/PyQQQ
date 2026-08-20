# Architecture Decision Record — 回顾

> 生成日期：2026-08-19
> 覆盖版本：v0.3.0 → v0.7.0
> 类型：回顾型 ADR（已实现的决策回顾）

---

## ADR-1：EngineBackend 通用基类

**决策**：用一个 `EngineBackend` 基类统一所有模拟器后端，子类只需实现 `_create` / `_apply_one` / `_sample` 三个方法。

**背景**：原计划是 translator 模式（19 个 translator 文件 × 7 个后端 = 133 处改动）。engine 模式只需每个后端一个文件。

**选择**：engine 模式。

**权衡**：
- ✅ 新增后端极快（一个文件 ~60 行）
- ✅ 不动任何现有 translator
- ❌ 经典控制流（cif/cmeasure/cwhile）需要 per-shot 动态执行
- ❌ 每个后端的 translator 语义丢失（如 qiskit 的 `if_test`、cirq 的 `with_classical_controls`）

**后果**：6 个 engine 后端 + CuPy 兜底引擎 + 7 个 translator 后端并存。后端数量从 5 增长到 12。

---

## ADR-2：CuPy 兜底引擎 vs 各后端 GPU

**决策**：两者都做——各后端 GPU 变体为主，CuPy 兜底为辅。

**背景**：讨论过三种方案：
- A. CuPy 统一层（一个引擎覆盖所有后端）
- B. 各后端 GPU 变体（每个后端用自己的 GPU）
- C. 两者结合

**选择**：方案 C。

**权衡**：
- ✅ 各后端 GPU 性能最优（专属 kernel）
- ✅ CuPy 兜底覆盖无 GPU 后端（cirq 等）
- ❌ CuPy 性能不如专属 GPU（通用矩阵乘法 vs 手写 kernel）
- ❌ 维护成本增加（两套 GPU 路径）

**后果**：CuPy 引擎作为 fallback 存在，各后端有 GPU 的用各自的。用户不需要知道 CuPy 存在。

---

## ADR-3：智能调度 vs 硬编码阈值

**决策**：先用硬编码阈值，再用 measured 数据覆盖，最终走向学习型调度。

**背景**：GPU 调度需要决定「哪条电路用哪个后端」。两种方案：
- A. 硬编码 if/elif 链
- B. benchmark 数据驱动

**选择**：两者结合——`recommend_backend_gpu()` 先查 measured 数据，没有时 fallback 硬编码。

**权衡**：
- ✅ 冷启动有默认值（硬编码）
- ✅ 有数据后自动优化（measured）
- ✅ 用户可覆盖（LocalCacheRegistry）
- ❌ 硬编码阈值没有 benchmark 支撑（n=20/30 是拍脑袋的）

**后果**：`benchmarks.json` 已有 RTX 2070 数据。后续需要更多硬件上跑 benchmark。

---

## ADR-4：自定义门通过 gate registry 而非修改 translator

**决策**：用全局 `_GATE_REGISTRY` 注册自定义门，各后端在 `apply` / `_apply_one` 时查 registry。

**背景**：自定义门需要在所有后端工作。两种方案：
- A. 修改所有 translator（19 个文件 × 3 个方法）
- B. 用全局 registry，各后端在 dispatch 前查 registry

**选择**：方案 B。

**权衡**：
- ✅ 改动小（每个后端加 ~5 行）
- ✅ translator 后端（qiskit/cirq/pennylane）也支持（查 registry 后用原生 matrix gate）
- ❌ 全局 registry 是进程级状态（不支持并发）
- ❌ 自定义门不支持 gate cancellation（`_SELF_INVERSE` 不含自定义门）

**后果**：`Gate.from_matrix()` 成为高阶用户的核心 API。后续需要考虑 gate metadata（逆门、自逆、commutation 关系）。

---

## ADR-5：MixedState 而非强制纯态

**决策**：当 `return_state=True` + noise 时，返回 `MixedState`（密度矩阵封装），而非 `StateVector`。

**背景**：噪声路径返回密度矩阵，不是纯态矢量。两种方案：
- A. 抛 NotImplementedError（noise + return_state 不支持）
- B. 返回 MixedState，支持 probabilities/expectation/purity

**选择**：方案 B。

**权衡**：
- ✅ 用户可以在噪声条件下访问量子态
- ✅ MixedState 支持 probabilities/expectation/purity
- ❌ `amplitude()` 抛 NotImplementedError（混合态没有振幅）
- ❌ StateVector 和 MixedState 是两个不同的类，API 不完全统一

**后果**：用户代码需要处理两种返回类型（StateVector vs MixedState）。后续考虑用 Protocol 或 Union 类型统一。

---

## ADR-6：电路优化 pass 接受 callable

**决策**：`optimize(circuit, passes=...)` 接受字符串或 callable。

**背景**：用户想自定义优化 pass。两种方案：
- A. 只接受字符串（内置 pass 名称）
- B. 接受字符串或 callable

**选择**：方案 B。

**权衡**：
- ✅ 用户可以传自定义优化函数
- ✅ 内置 pass 仍然用字符串
- ❌ 类型检查变复杂（`Tuple[str, ...]` → `Tuple`）
- ❌ 自定义 pass 的错误处理不统一

**后果**：`optimize` 的类型签名变宽。后续考虑用 Protocol 约束 pass 函数签名。

---

## ADR-7：cwhile + GPU 自动 groverize

**决策**：`run(method="gpu")` 检测到 cwhile 时，自动尝试 `groverize()` 编译成静态电路再跑 GPU。

**背景**：cwhile 需要 per-shot 动态执行，GPU 后端不支持。两种方案：
- A. 抛 NotImplementedError（cwhile + GPU 不支持）
- B. 自动 groverize 成静态电路再跑 GPU

**选择**：方案 B（部分）。

**权衡**：
- ✅ 用户不需要手动 groverize
- ✅ groverize 失败时 fallback 到原始电路
- ❌ groverize 改变电路结构（增加 ancilla、改变深度）
- ❌ groverize 需要推断成功概率（`_infer_success_prob`）

**后果**：cwhile + GPU 不再报错，但结果可能与 CPU 版本略有差异（groverize 近似）。

---

## ADR-8：翻译器自定义门 fallback

**决策**：qiskit/cirq/pennylane 翻译器遇到未知门名时，查 `_GATE_REGISTRY`，用原生 matrix gate 翻译。

**背景**：翻译器用 `TRANSLATORS[op.name]` 分发门，自定义门不在 TRANSLATORS 里。两种方案：
- A. 抛 KeyError（自定义门不支持）
- B. 查 `_GATE_REGISTRY`，用原生 matrix gate

**选择**：方案 B。

**权衡**：
- ✅ 自定义门在所有后端都能跑
- ✅ 改动小（每个翻译器加 ~5 行）
- ❌ 原生 matrix gate 可能不如手写 gate 高效
- ❌ 依赖 `_GATE_REGISTRY` 全局状态

**后果**：`Gate.from_matrix()` 成为全后端通用 API。

---

## ADR-9：功能耦合测试矩阵

**决策**：建立三层测试体系——单功能测试、两两耦合测试、嵌套测试。

**背景**：功能数量增长后，单独测试无法覆盖功能间的交互。两种方案：
- A. 只测单功能（现有做法）
- B. 建立系统化耦合测试矩阵

**选择**：方案 B。

**权衡**：
- ✅ 69 个跨功能测试覆盖关键耦合
- ✅ 已知不兼容被文档化（5 个，修了 3 个）
- ❌ 测试数量增长快（578 个）
- ❌ 维护成本随功能增长

**后果**：`test_integration.py` + `test_coupling_matrix.py` + `test_nesting.py` 成为质量保障的核心。

---

## ADR-10：版本发布节奏

**决策**：快速迭代（几天一个 minor 版本），不做长期规划。

**背景**：v0.3.0 → v0.7.0 在几天内完成，4 个 minor 版本。

**权衡**：
- ✅ 快速反馈，快速迭代
- ✅ 功能密度高（每个版本有实质内容）
- ❌ 文档滞后（功能先做，文档后补）
- ❌ 技术债累积（tensorcircuit patch、cqlib 委托等）
- ❌ 架构决策可能不够深思熟虑

**后果**：需要在某个版本停下来做一轮技术债清理。建议 v0.8.0 作为「稳定化」版本。

---

## 总结

| 决策 | 核心权衡 | 最大收益 | 最大风险 |
|---|---|---|---|
| EngineBackend 基类 | 简单 vs 语义 | 新增后端极快 | 经典控制流语义丢失 |
| CuPy + 各后端 GPU | 通用 vs 专属 | 全后端 GPU 覆盖 | 维护成本 |
| 智能调度 | 默认 vs 学习 | 冷启动有保障 | 阈值不准 |
| 自定义门 registry | 全局 vs 局部 | 全后端通用 | 并发不安全 |
| MixedState | 统一 vs 分离 | 噪声态可访问 | API 不统一 |
| 优化 pass callable | 固定 vs 灵活 | 用户可扩展 | 类型安全 |
| cwhile + GPU 自动 groverize | 报错 vs 自动 | 用户无感 | 结果可能不同 |
| 翻译器自定义门 fallback | 报错 vs 兼容 | 全后端通用 | 依赖全局状态 |
| 耦合测试矩阵 | 快 vs 全 | 质量保障 | 维护成本 |
| 快速迭代 | 速度 vs 质量 | 功能密度高 | 技术债累积 |
