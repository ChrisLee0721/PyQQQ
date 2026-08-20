# 真实硬件验证：qif + groverize + 典型案例

把本轮新增的两类**可静态编译**的构造，连同典型基准态，一起提交到 Quantum Inspire
真机（Tuna-17）验证。全部是无中段反馈的静态电路，超导真机可直接运行：

- **qif（量子叠加 if）**：编译成受控酉（cx/rz/ry/p），不测量控制比特；
  `qif(0).then(X,1).else_(I,1)` 等价于 CNOT。
- **cwhile → groverize**：RUS 循环编译成静态 Grover 电路（延迟测量 + 振幅放大）。
- **典型案例**：Bell、GHZ-3 作为无噪声参考基准。

Submits the two statically-compilable constructs added this round — plus typical
reference states — to Quantum Inspire real hardware (Tuna-17). All are static,
feedback-free circuits that superconducting hardware can run directly:

- **qif (quantum-superposition if)**: compiled to a controlled unitary (cx/rz/ry/p),
  the control qubit is not measured; `qif(0).then(X,1).else_(I,1)` equals CNOT.
- **cwhile → groverize**: an RUS loop compiled to a static Grover circuit (deferred
  measurement + amplitude amplification).
- **typical cases**: Bell and GHZ-3 as noiseless reference baselines.

## 运行 Run

```bash
# 先用 QX 云模拟器验证提交链路（免费、快）
.venv-qi\Scripts\python examples/qi_hardware/hardware_test.py qx

# 再上 Tuna-17 真机（消耗机时、排队）
.venv-qi\Scripts\python examples/qi_hardware/hardware_test.py tuna17
```

## 预期输出 Expected output

QX 模拟器上，各电路计数接近理想值：

- Bell / GHZ-3 / qif→CNOT：约 50% 各一半。
- qif→ctrl-Ry：`|00>,|01>,|10>,|11>` 各约 25%。
- cwhile→groverize（单/多比特）：成功态 `|00>` / `|1010>` 命中 100%。

真机（Tuna-17）带读取/门噪声，理想态计数会略降、出现少量杂项，但主峰应集中在
理想态上（贝尔态主峰合计通常 > 90%）。

On the QX emulator each circuit matches its ideal closely: Bell / GHZ-3 / qif→CNOT are
~50/50; qif→ctrl-Ry gives ~25% on each of `|00>,|01>,|10>,|11>`; both groverize circuits
hit their success state (`|00>` / `|1010>`) 100% of the time. On Tuna-17, readout/gate
noise slightly lowers the ideal-state counts and adds a few stray terms, but the main
peaks stay on the ideal states (the Bell peaks usually sum to > 90%).

## 注意 Note

- 前置依赖：`qiskit-quantuminspire` 要求 `qiskit<2.4.0`，需在 `.venv-qi` 独立环境运行，
  并用 `qi login` 登录（token 存 `~/.quantuminspire/config.json`）。
- 只有静态电路能上真机：`cif` / 裸 `cwhile`（中段测量反馈）会抛 `NotImplementedError`；
  必须 `loop.groverize()` 编译成静态电路后才能跑。
- 真机无法注入 `noise`，传 `noise=` 会抛 `ValueError`（真机噪声是内禀的）。

- Prerequisites: `qiskit-quantuminspire` requires `qiskit<2.4.0`, so run inside the
  `.venv-qi` environment and log in with `qi login` (token at `~/.quantuminspire/config.json`).
- Only static circuits run on hardware: `cif` / bare `cwhile` (mid-circuit feedback) raise
  `NotImplementedError`; call `loop.groverize()` to compile them to static first.
- Hardware cannot inject `noise`; passing `noise=` raises `ValueError` (hardware noise is intrinsic).

---

## 误差缓解验证 Error-mitigation validation

`mitigation_test.py` 在真机上验证四项误差缓解优化，以及两项后续增强：

- **#1 ZNE（零噪声外推）**：全局酉折叠 `C → C(C†C)^k` 放大本征噪声，外推到 λ=0。
- **#2 reflect_zero**：groverize 只对数据比特反射（深度更浅）。
- **#3 transpile level 3**：qi 后端自动应用。
- **#4 读出校准**：混淆矩阵求逆。
- **增强 · 指数外推** `extrapolation="exponential"`：三参数 `a·e^(-bλ)+c` 拟合（默认线性）。
- **增强 · 关联读出校准** `correlated=True`：完整 2ⁿ×2ⁿ 混淆矩阵（默认逐比特张量积）。

`mitigation_test.py` validates the four error-mitigation optimizations on hardware, plus two
later enhancements:

- **#1 ZNE (zero-noise extrapolation)**: global unitary folding `C → C(C†C)^k` amplifies
  intrinsic noise, extrapolated back to λ=0.
- **#2 reflect_zero**: groverize reflects on data qubits only (shallower depth).
- **#3 transpile level 3**: applied automatically inside the qi backend.
- **#4 readout calibration**: confusion-matrix inversion.
- **enhancement · exponential extrapolation** (`extrapolation="exponential"`): a 3-parameter
  `a·e^(-bλ)+c` fit (linear is the default).
- **enhancement · correlated readout** (`correlated=True`): the full 2ⁿ×2ⁿ confusion matrix
  (per-qubit tensor product is the default).

### 运行 Run

```bash
.venv-qi\Scripts\python examples/qi_hardware/mitigation_test.py qx       # QX 无噪声预检
.venv-qi\Scripts\python examples/qi_hardware/mitigation_test.py tuna17    # Tuna-17 真机
.venv-qi\Scripts\python examples/qi_hardware/mitigation_test.py tuna17 1  # 只跑多比特案例
```

### 真机实测 Measured on Tuna-17（shots=1024）

单比特 groverize（n=2，目标 `00`）：

| 方法 method | 成功率 success |
|---|---|
| raw | 0.936 |
| 逐比特读出校准 per-qubit readout | 0.982 |
| 关联读出校准 correlated readout | 0.985 |
| ZNE 线性外推 linear | 0.917 |
| ZNE 指数外推 exponential | 0.920 |
| ZNE+校准 指数外推 stacked exponential | **0.963** |

多比特 groverize（n=4，目标 `1010`）：

| 方法 method | 成功率 success |
|---|---|
| raw | 0.706 |
| 逐比特读出校准 per-qubit readout | 0.788 |
| 关联读出校准 correlated readout | 0.796 |
| ZNE 线性外推 linear | 0.791 |
| ZNE 指数外推 exponential | 0.812 |
| ZNE+校准 指数外推 stacked exponential | **0.869** |

### 结论 Findings

- **指数外推是更有价值的增强**：多比特 +2.1pt（0.791→0.812），门噪声主导时更贴合物理模型。
- **关联读出增益很小**：多比特 +0.8pt（0.788→0.796）、单比特 +0.3pt——Tuna-17 的读出串扰小，
  且 2ⁿ 电路在真机排队上代价高（本次实测单 job 排队曾超过 30 分钟，超时已放宽到 60 分钟）。
- **噪声 run-to-run 漂移**：多比特 raw 三次实测 0.699 / 0.646 / 0.706，以上是单次快照而非常数。
- **通用缓解天花板**：多比特 ~87–90%、单比特 ~96%；再往上需要设备专属优化（选高 T2 比特、
  原生门集、脉冲级校准）。

- **Exponential extrapolation is the more valuable enhancement**: +2.1pt on multi
  (0.791→0.812), a closer match to the physics when gate noise dominates.
- **Correlated readout gains little**: +0.8pt on multi (0.788→0.796) and +0.3pt on single —
  Tuna-17's readout crosstalk is small, and 2ⁿ circuits are expensive on the hardware queue
  (one job was observed to queue > 30 minutes, so the timeout is now 60 minutes).
- **Noise drifts run to run**: multi raw measured 0.699 / 0.646 / 0.706 across three runs;
  the tables above are single snapshots, not constants.
- **General-mitigation ceiling**: ~87–90% for multi, ~96% for single; beyond that requires
  device-specific optimization (high-T2 qubit selection, native gate set, pulse-level calibration).
