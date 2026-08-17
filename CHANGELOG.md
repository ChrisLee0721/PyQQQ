# Changelog

本项目所有重要变更都记录于此。All notable changes to this project are documented here.

## [0.3.0] — 2026-08-17

补齐五块缺口并加入误差缓解：多比特经典寄存器、路由编译、ZNE、读出校准，以及四个新
example。This release fills five gaps and adds error mitigation: multi-bit classical
registers, route-aware compilation, ZNE, readout calibration, and four new examples.

### 新增 Added

- **多比特经典寄存器** `creg(name, width=N)`；`cwhile(reg, until=v)` / `cif(reg, v)`
  支持整数值或比特串判据；`groverize()` 推广到 N 比特成功态。
  **Multi-bit classical registers** `creg(name, width=N)`; `cwhile`/`cif` accept integer
  or bitstring criteria; `groverize()` generalizes to N-bit success states.

- **路由编译** `compile(circuit, coupling_map, route=True)` 自动 `decompose` + `route_swaps`。
  **Route-aware compilation** `compile(..., route=True)` decomposes then routes onto the
  coupling map.

- **ZNE 误差缓解** `zne()` / `fold()`：全局酉折叠 + 线性或指数（三参数）外推，成功率与
  期望值两种指标；`plot_zne()` 可视化。
  **ZNE** `zne()` / `fold()`: global unitary folding with linear or exponential (3-param)
  extrapolation, success and expectation metrics; `plot_zne()` visualization.

- **读出校准** `calibrate()` / `ReadoutCalibration`：逐比特（张量积）与关联（完整 2ⁿ 矩阵）
  两种混淆矩阵模型。
  **Readout calibration** `calibrate()` / `ReadoutCalibration`: per-qubit (tensor-product)
  and correlated (full 2ⁿ matrix) confusion-matrix models.

- **`DensityMatrixEngine.expectation()`** 计算泡利串可观测量期望值。
  **`DensityMatrixEngine.expectation()`** for Pauli-string observables.

- **cmeasure 支持 cirq / pennylane** 后端翻译。
  **cmeasure translation** for the cirq and pennylane backends.

- **新 example**：`creg_multi`、`groverize`、`hardware_compile`、`qi_hardware`。
  **New examples**: `creg_multi`, `groverize`, `hardware_compile`, `qi_hardware`.

### 变更 Changed

- 后端门翻译重构为共享 `translators/` 模块。
  Backend gate translation factored into a shared `translators/` module.

- `NoiseModel` 新增 `readout` 字段（测量比特翻转）。
  `NoiseModel` gained a `readout` (measurement bit-flip) field.

- qi 后端 job 超时 30 → 60 分钟（Tuna-17 排队）。
  qi backend job timeout relaxed 30 → 60 minutes (Tuna-17 queue).

- qi 依赖冲突指南默认改走 venv 方案。
  qi dependency-conflict guide now defaults to the venv workaround.
