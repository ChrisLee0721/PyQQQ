# ZX-Calculus Optimization API / ZX 演算优化 API

ZX-calculus is a graphical language for reasoning about quantum circuits. QuoNic uses it for circuit optimization.

ZX 演算是用于推理量子电路的图形语言。QuoNic 用它进行电路优化。

## Quick Start / 快速开始

```python
from quonic.zx import circuit_to_zx, optimize_zx, extract_circuit

# Convert → Optimize → Extract
# 转换 → 优化 → 提取
graph = circuit_to_zx(circuit)
optimized_graph = optimize_zx(graph)
optimized_circuit = extract_circuit(optimized_graph)

print(f"Before: {circuit.gate_count()} gates")
print(f"After:  {optimized_circuit.gate_count()} gates")
```

## circuit_to_zx(circuit) — Convert to ZX-Graph / 转换为 ZX 图

Convert a QuoNic circuit to a ZX-graph representation.

将 QuoNic 电路转换为 ZX 图表示。

```python
from quonic.zx import circuit_to_zx

graph = circuit_to_zx(circuit)
print(f"Nodes: {len(graph.spiders)}")
print(f"Edges: {len(graph.edges)}")
```

## optimize_zx(graph) — Apply Rewrite Rules / 应用重写规则

Apply 7 ZX-calculus rewrite rules to simplify the graph.

应用 7 条 ZX 演算重写规则简化图。

```python
from quonic.zx import optimize_zx

optimized = optimize_zx(graph)
```

### Rewrite rules / 重写规则

| Rule | Description | Effect |
|------|-------------|--------|
| Spider fusion | Merge adjacent same-color spiders | Reduce nodes |
| Identity removal | Remove degree-2 spiders | Simplify graph |
| H-edge elimination | Remove H-edges between spiders | Clean up |
| Supplementarity | Color-change simplification | Reduce complexity |
| Phase copy | Copy phases through H-edges | Optimize rotations |
| Bialgebra | Simplify X-Z interactions | Reduce gates |
| Pattern matching | HZH=X, HXH=Z | Cancel H pairs |

## extract_circuit(graph) — Extract Circuit / 提取电路

Convert optimized ZX-graph back to a QuoNic circuit.

将优化后的 ZX 图转换回 QuoNic 电路。

```python
from quonic.zx import extract_circuit

circuit = extract_circuit(optimized_graph)
```

## ZXGraph — Graph Representation / 图表示

```python
from quonic.zx import ZXGraph

graph = ZXGraph()
# Add spiders (nodes)
graph.add_spider("Z", phase=0.5, qubit=0, time=0)
graph.add_spider("X", phase=0, qubit=0, time=1)
# Add edges
graph.add_edge(0, 1)
```

## Examples / 示例

### Optimize a QFT circuit / 优化 QFT 电路

```python
from quonic.algorithms import qft
from quonic.zx import circuit_to_zx, optimize_zx, extract_circuit

# Build QFT
qft_circuit = qft(4)

# Optimize with ZX-calculus
graph = circuit_to_zx(qft_circuit)
optimized = optimize_zx(graph)
result = extract_circuit(optimized)

print(f"QFT: {qft_circuit.gate_count()} → {result.gate_count()} gates")
```

### Optimize before hardware compilation / 硬件编译前优化

```python
from quonic.zx import circuit_to_zx, optimize_zx, extract_circuit
from quonic.compiler import decompose, optimize

# 1. ZX optimization first (reduces gate count)
graph = circuit_to_zx(circuit)
optimized = extract_circuit(optimize_zx(graph))

# 2. Then decompose and optimize for hardware
final = optimize(decompose(optimized))
```
