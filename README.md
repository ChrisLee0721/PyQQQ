# QuoNic — Quantum programming, as simple as writing Python

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-green.svg)](https://qiskit.org/)
[![Cirq](https://img.shields.io/badge/Cirq-1.0+-orange.svg)](https://quantumai.google/cirq)

**QuoNic is a tool that makes quantum programming as simple as writing Python.**

No `QuantumCircuit` to learn, no `backend` to understand, no manual `measure`. If you can write Python, you can write quantum programs.

[中文文档](README.zh-CN.md)

---

## 🚀 30-second quick start

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

**This is the Bell state — the most classic result in quantum computing.** The same thing takes 10+ lines in raw Qiskit. QuoNic does it in 3. The result appears directly in your terminal or Jupyter.

More copy-and-run examples (GHZ, `qif`, `QInt`, Grover, VQE, QAOA, noise) live in [`examples/`](examples/).

---

## 📦 Installation

```bash
pip install quonic
```

Backends are optional dependencies — install only what you need. To install all backends (plus numpy/scipy for the algorithm templates) in one shot:

```bash
pip install 'quonic[qiskit,cirq,pennylane,algorithms,all-sim]'
```

To install a single backend, e.g. only Cirq: `pip install 'quonic[cirq]'`. Calling an uninstalled backend raises a clear message (English by default; set `QUONIC_LANG=zh` for Chinese).

Additional simulator backends (Qulacs / TensorCircuit / CUDA-Q / MindQuantum / QPanda3 / CqLib): `pip install 'quonic[all-sim]'` or install individually, e.g. `pip install 'quonic[qulacs]'`.

Visualization is a separate optional dependency: `pip install 'quonic[viz]'` (matplotlib only — no Graphviz / Seaborn / NetworkX).

---

## ✨ Core features

### 1. Minimal syntax: a Bell state in 3 lines

You don't need to understand "quantum circuit objects", pick a "backend simulator", or write `measure` by hand. QuoNic handles all of it.

### 2. Switch every backend with one argument

```python
# Use the Qiskit simulator (default)
qshow(backend='qiskit')

# Switch to Cirq
qshow(backend='cirq')

# Switch to Qulacs (high-performance C++)
qshow(backend='qulacs')

# Switch to TensorCircuit (JAX/TensorFlow/PyTorch)
qshow(backend='tensorcircuit')

# Noise simulation
qshow(backend='qiskit', noise=0.05)

# Real hardware (Quantum Inspire) — requires login
qshow(backend='qi')                    # QX cloud simulator (default; verify before submitting)
qshow(backend='qi', device='tuna9')    # Tuna-9 real device
qshow(backend='qi', device='tuna17')   # Tuna-17 real device
qshow(backend='qi', device='qx')       # QX cloud simulator
```

**The same code, unchanged, runs on any backend.** Minimal syntax + backend independence is QuoNic's combined differentiator.

### 3. Conditional gates and "if = superposition"

QuoNic implements quantum superposition control with `qif` and draws a strict line between two concepts:

- **Quantum superposition control (`qif`, implemented)**: when the control qubit is in a superposition, the branches are **not measured** — they interfere coherently and produce real entanglement. This is "both branches happen at once", not "measure then pick one".
  ```python
  from quonic import qgate, qif, qshow
  from quonic.gates import H, X, I

  qgate(H, 0)                       # control qubit enters superposition
  qif(0).then(X, 1).else_(I, 1)     # q0==1 flips q1, else nothing (= controlled X)
  qshow()
  ```
  The `I` in `else_(I, ...)` is the identity gate, so "controlled gate = qif special case" reads naturally.
- **Conditional gates (classical control, planned)**: measure first, then branch on the result — a "classical branch after collapse".
  ```python
  # Planned: condition on the measurement result
  # qgate(H, 0)
  # if qgate(MEASURE, 0) == 0:
  #     qgate(X, 1)
  # else:
  #     qgate(Z, 1)
  ```

We don't dress up "classical branching after measurement" as "superposition" — teaching wrong physics is worse than not teaching at all.

### 4. Genuinely beginner-friendly

- **Clear error messages** (English by default, Chinese via `QUONIC_LANG=zh`): they tell you what went wrong, why, and how to fix it
- **Autocomplete**: gate names and parameters are hinted in VS Code / Jupyter
- **Automatic measurement**: forgot to write `measure`? `qshow()` fills it in

### 5. Smart scheduler: automatically picks the fastest method

Quantum simulation has four methods whose speeds differ by orders of magnitude — picking wrong hits a wall:

| Method | Complexity | Best for |
|------|--------|------|
| `statevector` | 2^n | general default |
| `stabilizer` | polynomial | pure Clifford circuits (e.g. error-correcting codes) |
| `matrix_product_state` | grows with treewidth | low-treewidth circuits (e.g. QAOA) |
| `density_matrix` | 4^n | noise simulation |

QuoNic's scheduler picks automatically based on circuit features (gate types, treewidth, whether it contains noise) — you never specify the method by hand. Measured evidence: **GHZ(24) is 36× faster, QAOA(24) 19× faster**; Grover's `mcz` only runs on `statevector`, and the scheduler routes around methods that would crash.

```python
from quonic.scheduler import schedule
rec = schedule(circuit)   # -> Recommendation(backend='qiskit', method='stabilizer')
```

See [scheduler benchmarks and measurements](docs/benchmarks.md).

### 6. Full visualization suite: 23 chart types with only Matplotlib

```python
from quonic.viz import plot_circuit, plot_counts, plot_decision_tree

plot_circuit(circuit)        # gate-sequence circuit diagram
plot_counts(result)          # measurement histogram
plot_decision_tree()         # scheduler decision tree
```

The 23 chart types span four layers: **core needs** (circuit / histogram / topology), **scheduler evidence** (method comparison / decision tree / heatmap / fallback chain / feature radar), **algorithm teaching** (energy convergence / Grover amplitude / statevector / Bloch sphere), and **quantum states** (density matrix / entanglement / gate matrix / routing / per-gate state evolution / noise cost). All with matplotlib as the single dependency, lazy-loaded, zero overhead on `import quonic`. See [visualization suite](docs/visualization.md).

---

## 📊 QuoNic vs Qiskit

| Scenario | Qiskit | QuoNic |
|------|--------|-------|
| **First quantum program** | 5–8 new concepts to learn | just 2: `qgate` and `qshow` |
| **Lines of code (Bell state)** | 8–12 lines | **3 lines** |
| **Install to first result** | 30–60 minutes | **2–3 minutes** |
| **Switching backends** | rewrite everything | **change one argument** |

---

## 🧠 Why the name QuoNic?

QuoNic is an acronym for **Quantum Unified Operation Native Interface Core**:

| Letter | Word | Meaning |
|------|-----|------|
| Q | Quantum | quantum |
| U | Unified | unified — one argument switches every backend |
| O | Operation | operations — `qgate` / `qshow` |
| N | Native | native — as natural as writing Python |
| I | Interface | interface — the backend adapter layer |
| C | Core | core — IR / scheduler / compiler |

Pronounced /ˈkwɑnɪk/ ("kwah-nik").

---

## 🛠️ Currently supported backends

| Backend | Status | Notes |
|------|------|------|
| Qiskit | ✅ stable | IBM ecosystem · all 4 methods · noise · classical control flow |
| Cirq | ✅ stable | Google ecosystem · statevector · noise |
| PennyLane | ✅ stable | quantum machine learning · statevector · noise |
| Qulacs | ✅ stable | high-performance C++ simulator · statevector + density matrix · noise |
| TensorCircuit | ✅ stable | JAX/TensorFlow/PyTorch backend · statevector + density matrix · noise |
| CUDA-Q | ✅ stable | NVIDIA GPU-accelerated · statevector · global noise model |
| MindQuantum | ✅ stable | Huawei · statevector + density matrix · noise (Linux/macOS) |
| QPanda3 | ✅ stable | Origin Quantum · statevector + density matrix |
| CqLib | ⚠️ cloud-only | China Telecom Quantum · no local simulator |
| Quantum Inspire | ✅ connected | real hardware Tuna-9 / Tuna-17 + QX simulator |
| Native | ✅ stable | in-house numpy engine · all 4 methods · noise · fallback |

> **Note**: Qiskit / Cirq / PennyLane / Qulacs / TensorCircuit / QPanda3 run on **local simulators**. CUDA-Q requires NVIDIA CUDA. MindQuantum requires Linux/macOS. CqLib is cloud-only (TianYan platform). Quantum Inspire real hardware is reached via `qshow(backend="qi", device="tuna9")`.

To pave the way for hardware, QuoNic already ships `CouplingMap` (coupling graph), the `compile()` compilation seam, and `decompose()` gate decomposition — which expands higher-order gates (`cp` / `ccx` / `mcz`) into the basic gate set. The latter is QuoNic's own "portable core": users aren't locked to one backend's circuit shape, and Grover's `mcz` decomposes into `cx / h / p` so it runs on every backend method. A greedy SWAP router `route_swaps()` is built in (with `plot_routing` visualization), so wiring up IBM / domestic engines later only touches the compilation layer — no changes to the IR or scheduler.

---

## 📖 Docs and tutorials

- [Quickstart](docs/quickstart.md) — up and running in 5 minutes
- [Jupyter tutorial](docs/tutorial.ipynb) — runnable interactive notebook
- [Scheduler benchmarks](docs/benchmarks.md) — the measured-data moat behind automatic method selection
- [Visualization suite](docs/visualization.md) — 23 chart types with only Matplotlib
- [Domestic hardware survey](docs/domestic-hardware.md) — QPanda3 / CqLib integration assessment

---

## 🤝 Contributing

QuoNic is open source (Apache 2.0) and welcomes all kinds of contribution:

- Report bugs
- Propose new features
- Submit code (new backend adapters, gates, features)
- Improve docs and tutorials

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development setup, code style, and conventions.

---

## 📄 License

QuoNic is licensed under the [Apache License 2.0](LICENSE) — friendly to commercial and closed-source use, with patent protection.

---

## 🌟 Star the project

If QuoNic helps you, please give us a ⭐️ on GitHub. Your support keeps us going.
