"""Hardware-Aware Compilation Workflow / 硬件感知编译工作流

Complete workflow for circuit compilation with hardware constraints.

## Problem / 问题
Compile a circuit for specific hardware topology with optimization.

## QuoNic Features Used / 使用的 QuoNic 功能
- Gate decomposition (门分解)
- Circuit optimization (电路优化)
- SWAP routing (SWAP 路由)
- Gate fusion (门融合)
- Smart scheduling (智能调度)

## Output / 输出
Compiled circuit with reduced depth and gate count.
"""

from quonic.compiler import decompose, optimize, route_swaps
from quonic.ir import Circuit, GateOperation
from quonic.topology import CouplingMap
from quonic import qshow, reset
from quonic.gates import H, CX

print("=== Hardware-Aware Compilation ===")
print()

# Build a test circuit
print("--- Original Circuit ---")
circuit = Circuit()
circuit.allocate(4)
circuit.add(GateOperation("h", (0,)))
circuit.add(GateOperation("cx", (0, 1)))
circuit.add(GateOperation("cx", (1, 2)))
circuit.add(GateOperation("cx", (2, 3)))
circuit.add(GateOperation("h", (3,)))
circuit.add(GateOperation("cx", (0, 2)))
circuit.add(GateOperation("cx", (1, 3)))

ops_orig = len([op for op in circuit.ops if op.name != 'measure'])
print(f"Original ops: {ops_orig}")
print()

# Step 1: Decompose high-level gates
print("--- Step 1: Decompose ---")
decomposed = decompose(circuit)
ops_decomp = len([op for op in decomposed.ops if op.name != 'measure'])
print(f"Decomposed ops: {ops_decomp}")
print()

# Step 2: Optimize
print("--- Step 2: Optimize ---")
optimized = optimize(decomposed, passes=("cancel", "commute", "cancel", "peephole", "fuse"))
ops_opt = len([op for op in optimized.ops if op.name != 'measure'])
print(f"Optimized ops: {ops_opt}")
print(f"Reduction: {ops_orig} → {ops_opt} ({(1-ops_opt/ops_orig)*100:.1f}%)")
print()

# Step 3: Route for hardware topology
print("--- Step 3: SWAP Routing ---")
# Linear topology: 0-1-2-3
coupling = CouplingMap(4, [(0, 1), (1, 2), (2, 3)])
routed = route_swaps(optimized, coupling)
ops_routed = len([op for op in routed.ops if op.name != 'measure'])
print(f"Routed ops: {ops_routed}")
print()

# Step 4: Final optimization
print("--- Step 4: Final Optimization ---")
final = optimize(routed, passes=("cancel", "commute", "cancel"))
ops_final = len([op for op in final.ops if op.name != 'measure'])
print(f"Final ops: {ops_final}")
print()

# Summary
print("--- Summary ---")
print(f"Original: {ops_orig} ops")
print(f"Final: {ops_final} ops")
print(f"Total reduction: {(1-ops_final/ops_orig)*100:.1f}%")
print()

print("=== Conclusion ===")
print("QuoNic provides complete hardware-aware compilation:")
print("1. Gate decomposition for hardware compatibility")
print("2. Circuit optimization (cancel, commute, fuse)")
print("3. SWAP routing for topology constraints")
print("4. Smart scheduling for backend selection")
