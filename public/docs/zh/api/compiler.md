# Compiler API

Gate decomposition, routing, and optimization.

门分解、路由和优化。

## decompose(circuit) — Gate Decomposition / 门分解

Decompose high-level gates into basic gate set (H, X, Y, Z, Rx, Ry, Rz, P, CX, CZ).

将高级门分解为基础门集。

```python
from quonic.compiler import decompose

# Decompose MCX, CCX, CP etc. into basic gates
# 将 MCX、CCX、CP 等分解为基础门
decomposed = decompose(circuit)
print(f"Before: {circuit.gate_count()} gates")
print(f"After:  {decomposed.gate_count()} gates")
```

### Decomposition rules / 分解规则

| Gate | Decomposition |
|------|---------------|
| `cp(θ)` | `p(θ/2)·cx·p(-θ/2)·cx·p(θ/2)` |
| `ccx` | 6 CX gates (Toffoli) |
| `mcz` | `H·mcx·H` with AND cascade |

## compile(circuit, coupling_map=None) — Topology Check / 拓扑校验

Verify circuit fits on hardware topology.

验证电路是否适合硬件拓扑。

```python
from quonic.compiler import compile
from quonic import CouplingMap

# Create a linear topology
cm = CouplingMap.from_line(4)
compile(circuit, cm)  # Raises RoutingError if gates don't fit
```

## optimize(circuit) — Gate Optimization / 门优化

Apply optimization passes: cancel redundant gates, merge rotations.

应用优化 pass：消除冗余门、合并旋转。

```python
from quonic.compiler import optimize

optimized = optimize(circuit)
print(f"Reduced {circuit.gate_count()} → {optimized.gate_count()} gates")
```

### Optimization passes / 优化 pass

| Pass | Description |
|------|-------------|
| `optimize_cancel` | Cancel inverse gate pairs (消除逆门对) |
| `optimize_commute` | Reorder commuting gates (重排可交换门) |
| `optimize_peephole` | Local pattern matching (局部模式匹配) |
| `optimize_fuse` | Merge consecutive single-qubit gates (合并连续单比特门) |

## groverize(circuit) — Algorithm-Level Compilation / 算法级编译

Convert classical loops (`cwhile`) into static Grover circuits.

将经典循环（`cwhile`）转换为静态 Grover 电路。

```python
from quonic.compiler import groverize

# Convert a cwhile loop to a Grover circuit
# 将 cwhile 循环转换为 Grover 电路
grover_circuit = groverize(cwhile_circuit, method="grover")

# FPAA method for higher success probability
grover_circuit = groverize(cwhile_circuit, method="fpaa")
```

### groverize methods / groverize 方法

| Method | Description | Success Rate |
|--------|-------------|-------------|
| `grover` | Standard Grover iteration | ~99.7% |
| `fpaa` | Fixed-Point Amplitude Amplification | ~100% |

## Examples / 示例

### Full compilation pipeline / 完整编译流水线

```python
from quonic.compiler import decompose, optimize, compile
from quonic import CouplingMap

# 1. Decompose high-level gates
step1 = decompose(circuit)

# 2. Optimize
step2 = optimize(step1)

# 3. Check topology
cm = CouplingMap.from_line(8)
compile(step2, cm)
```

### Vale et al. MCX decomposition / Vale 等人 MCX 分解

```python
from quonic.compiler import decompose

# 3-control MCX: 14 CX gates (vs 18 standard)
# 3 控制 MCX：14 个 CX 门（标准需要 18 个）
decomposed = decompose(mcx_circuit)
```
