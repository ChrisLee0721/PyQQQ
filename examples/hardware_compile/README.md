# 硬件编译 + 零噪声外推（端到端）

把含高层门（Toffoli `ccx`）的 GHZ-3 电路 `decompose` → `compile(route=True)` 落到 3 比特链拓扑
（非相邻 CX 用 SWAP 桥接），再用 5% 退极化噪声仿真，最后 `zne()` 用**成功率**与**期望值**
两种指标外推回无噪声真值，`plot_zne` 出图。ZNE 跑在逻辑电路上（路由额外插入的 SWAP 会让
噪声超出线性外推的适用范围）。

Route a GHZ-3 circuit containing a high-level Toffoli (`ccx`) via `decompose` →
`compile(route=True)` onto a 3-qubit line (non-adjacent CX gates are bridged by SWAPs),
simulate under 5% depolarizing noise, then `zne()` extrapolates back to the noiseless
value with both **success-probability** and **expectation-value** metrics, and `plot_zne`
renders the plots. ZNE runs on the logical circuit (routing's extra SWAPs push the noise
out of ZNE's linear regime).

## 运行 Run

```bash
python examples/hardware_compile/hardware_compile.py
```

## 预期输出 Expected output

打印路由前后门数、各 λ 成功率 / 期望值、以及外推值（应接近真值 1.0），
并把两张外推折线图存为 `zne_success.png`、`zne_expectation.png`。

Prints the gate counts before/after routing, the per-λ success / expectation values, and
the extrapolated value (close to the true 1.0), saving two plots as `zne_success.png`
and `zne_expectation.png`.

## 注意 Note

`CCX(0,1,2)` 分解出的 CX 里有非相邻的 `cx(0,2)`，在 0-1-2 链上无法直接放置，
`route=True` 会自动插入 SWAP 使其落到拓扑上。噪声越大，单次 λ=1 采样越偏离真值，
外推带来的增益越明显；`zne` 的成功率指标默认用 native / qiskit 采样，期望值指标
始终用库内密度矩阵引擎计算。真机上应对路由后电路做 ZNE，但 20 个门 × 5% 噪声会
超出线性外推的适用范围，故本例在逻辑电路上演示外推收敛到 1.0。

`CCX(0,1,2)` decomposes into CX gates including a non-adjacent `cx(0,2)` that cannot be
placed directly on the 0-1-2 line; `route=True` inserts SWAPs automatically. The stronger
the noise, the further the λ=1 sample drifts from the truth and the larger the extrapolation
gain. The success metric samples via the native / qiskit backends, while the expectation
metric always uses the in-house density-matrix engine. On real hardware you would ZNE the
routed circuit, but 20 gates × 5% noise exceeds ZNE's linear regime, so this example runs
ZNE on the logical circuit to show clean convergence to 1.0.
