# Visualization API

23 chart types for quantum circuits, results, and algorithms.

量子电路、结果和算法的 23 种图表类型。

## Quick Start / 快速开始

```python
from quonic.viz import plot_counts, plot_circuit

# Plot measurement results
plot_counts(result.counts)

# Plot circuit diagram
plot_circuit(circuit)
```

## Core Plots / 核心图表

### plot_counts(counts) — Measurement Histogram / 测量直方图

```python
from quonic.viz import plot_counts

plot_counts({"00": 512, "11": 512})
```

### plot_circuit(circuit) — Circuit Diagram / 电路图

```python
from quonic.viz import plot_circuit

plot_circuit(circuit)
```

### plot_topology(coupling_map) — Hardware Topology / 硬件拓扑

```python
from quonic.viz import plot_topology
from quonic import CouplingMap

cm = CouplingMap.from_line(8)
plot_topology(cm)
```

## Algorithm Plots / 算法图表

### plot_energy_convergence — VQE Convergence / VQE 收敛

```python
from quonic.viz import plot_energy_convergence

plot_energy_convergence(vqe_result)
```

### plot_grover_amplitude — Grover Amplitudes / Grover 振幅

```python
from quonic.viz import plot_grover_amplitude

plot_grover_amplitude(n_qubits=3, target="101")
```

### plot_bloch(state) — Bloch Sphere / Bloch 球

```python
from quonic.viz import plot_bloch

plot_bloch(state_vector)
```

### plot_statevector(state) — State Amplitudes / 态振幅

```python
from quonic.viz import plot_statevector

plot_statevector(state_vector)
```

## Quantum State Plots / 量子态图表

### plot_density_matrix(rho) — Density Matrix / 密度矩阵

```python
from quonic.viz import plot_density_matrix

plot_density_matrix(density_matrix)
```

### plot_entanglement(circuit) — Entanglement Map / 纠缠图

```python
from quonic.viz import plot_entanglement

plot_entanglement(circuit)
```

## Scheduler Plots / 调度器图表

```python
from quonic.viz import plot_method_comparison, plot_decision_tree, plot_heatmap

plot_method_comparison(benchmark_results)
plot_decision_tree(features)
plot_heatmap(benchmark_data)
```

## All Available Plots / 所有可用图表

| Category | Functions |
|----------|-----------|
| Core | `plot_circuit`, `plot_counts`, `plot_topology` |
| Scheduler | `plot_method_comparison`, `plot_decision_tree`, `plot_heatmap`, `plot_fallback_chain`, `plot_feature_radar` |
| Algorithm | `plot_energy_convergence`, `plot_grover_amplitude`, `plot_statevector`, `plot_bloch` |
| Quantum States | `plot_density_matrix`, `plot_entanglement`, `plot_gate_matrix`, `plot_routing`, `plot_per_gate_state`, `plot_noise_cost` |
