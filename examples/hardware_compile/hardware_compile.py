"""Hardware-Aware Compilation / 硬件感知编译

Circuit compilation with topology constraints and optimization.
带有拓扑约束和优化的电路编译。

## Application / 应用场景
- NISQ algorithms (NISQ 算法)
- Hardware targeting (硬件目标)
- Circuit optimization (电路优化)

## Output / 输出
Compiled circuit with reduced depth.
减少深度的编译电路。"""

from quonic import compile, qgate, zne
from quonic.gates import CCX, CX, H
from quonic.stack import current_circuit, reset
from quonic.topology import CouplingMap
from quonic.viz import plot_zne

# 1. 构建 GHZ-3（含高层 Toffoli 门）
qgate(H, 0)
qgate(CX, 0, 1)
qgate(CCX, 0, 1, 2)
ghz = current_circuit()
reset()

# 2. 路由到 3 比特链：CCX 分解为基础门，非相邻的 CX 用 SWAP 桥接
line = CouplingMap.from_line(3)
routed = compile(ghz, coupling_map=line, route=True)

print(f"原始电路门数: {ghz.gate_count()}")
print(f"路由后门数:   {routed.gate_count()}  (含 SWAP)")

# 3. 带噪声仿真 + 零噪声外推（两个指标）
# 注意：ZNE 在**逻辑电路**上跑 —— 路由会额外插入 SWAP，噪声超出线性外推的
# 适用范围；真机上则应对路由后电路做 ZNE。这里用逻辑电路演示外推收敛到 1.0。
noise = 0.05

succ = zne(ghz, noise, target={"000", "111"}, backend="native", shots=1024)
print("\n成功率指标 (target={'000','111'}):")
for lam, v in zip(succ.factors, succ.values):
    print(f"  λ={lam:.0f}  命中率 = {v:.4f}")
print(f"  外推(λ→0) = {succ.extrapolated:.4f}  (真值 1.0)")

expect = zne(ghz, noise, observable="XXX")
print("\n期望值指标 (observable='XXX'):")
for lam, v in zip(expect.factors, expect.values):
    print(f"  λ={lam:.0f}  <XXX> = {v:.4f}")
print(f"  外推(λ→0) = {expect.extrapolated:.4f}  (真值 1.0)")

# 4. 出图（保存到当前目录，不阻塞）
plot_zne(succ, save="zne_success.png")
plot_zne(expect, save="zne_expectation.png")
