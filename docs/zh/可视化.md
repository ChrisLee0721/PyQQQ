# 全量可视化套件

QuoNic 提供 23 类图，覆盖「用户刚需 → 调度器证据 → 算法教学 → 量子态」四层需求。
所有图只用 **matplotlib** 一个依赖——不引入 Graphviz（系统级依赖）、
Seaborn、NetworkX，保证 `pip install` 一把梭。

可视化是可选能力：`import quonic` 不引入 matplotlib，只有真正调用某个
`plot_*` 时才懒加载。

## 安装

```bash
pip install 'quonic[viz]'
```

## 统一约定

每个 `plot_*` 函数都接受四个可选参数，便于嵌入你自己的 figure 或导出：

| 参数 | 说明 |
|------|------|
| `ax` | 传入已有 matplotlib Axes（不传则新建） |
| `show` | 是否调用 `plt.show()`（默认 False，适合脚本/测试） |
| `save` | 保存路径，如 `save="circuit.png"` |
| `title` | 图标题 |

返回值统一为 matplotlib Axes（`plot_statevector` / `plot_density_matrix` /
`plot_gate_matrix` 返回长度为 2 的 Axes 序列）。

```python
from quonic.viz import plot_circuit

plot_circuit(circuit, save="circuit.png", title="贝尔态电路")
```

## 23 类图一览

| # | 图 | 函数 | 用途 |
|---|----|------|------|
| 1 | 门序列电路图 | `plot_circuit` | 最基础，用户最常需要 |
| 2 | 测量直方图 | `plot_counts` | 采样结果分布 |
| 3 | 耦合拓扑图 | `plot_coupling_map` | 硬件连通性（接真实硬件后刚需） |
| 4 | 方法对比折线图 | `plot_method_comparison` | 展示调度器优势的关键证据 |
| 5 | 调度决策树 | `plot_decision_tree` | 解释「为什么选这个方法」 |
| 6 | 方法选择热力图 | `plot_method_heatmap` | 展示调度器决策依据 |
| 7 | 降级链路径图 | `plot_fallback_chain` | 展示后端降级过程 |
| 8 | 量子比特活跃度热力图 | `plot_qubit_activity` | 调试与教学 |
| 9 | 电路特征雷达图 | `plot_feature_radar` | 单电路多维特征展示 |
| 10 | 能量收敛图 | `plot_energy_convergence` | VQE/QAOA 优化过程 |
| 11 | Grover 迭代振幅图 | `plot_grover_amplitudes` | 算法教学 |
| 12 | 态向量可视化 | `plot_statevector` | 高级用户/研究场景 |
| 13 | 噪声成本热力图 | `plot_noise_heatmap` | 噪声下密度矩阵模拟的成本墙 |
| 14 | 布洛赫球 | `plot_bloch_sphere` | 单比特态 3D 可视化 |
| 15 | 密度矩阵热力图 | `plot_density_matrix` | ρ 实/虚部 |
| 16 | 纠缠可视化 | `plot_entanglement` | 纠缠谱 + 熵 + 并发度 |
| 17 | 门矩阵可视化 | `plot_gate_matrix` | 门酉矩阵实/虚部 |
| 18 | SWAP 路由可视化 | `plot_routing` | 耦合图上的 SWAP 插入 |
| 19 | 逐门态演化 | `plot_state_evolution` | 态随门序列的概率演化 |
| 20 | 问题图 | `plot_problem_graph` | QAOA MaxCut 的图与割 |
| 21 | 哈密顿量可视化 | `plot_hamiltonian` | 泡利项系数 + 算符结构 |
| 22 | 纠缠熵谱 | `plot_entanglement_profile` | 所有二分切口的纠缠熵 |
| 23 | 噪声叠加电路图 | `plot_noisy_circuit` | 电路图上叠加噪声强度 |

## 用法示例

### 1. 门序列电路图

```python
from quonic import qgate, qshow
from quonic.gates import H, CX
from quonic.viz import plot_circuit
from quonic.stack import current_circuit

qgate(H, 0)
qgate(CX, 0, 1)
plot_circuit(current_circuit())
```

多比特门自动画控制点（实心圆）与目标符号（`⊕` / 盒子），参数化门显示
`rx(0.5)` 形式。

### 2. 测量直方图

```python
from quonic.viz import plot_counts

result = qshow(shots=1024)          # 或任意 Result（counts）
plot_counts(result)
```

也接受裸 dict：`plot_counts({"00": 512, "11": 512})`。

### 3. 耦合拓扑图

```python
from quonic import CouplingMap
from quonic.viz import plot_coupling_map

plot_coupling_map(CouplingMap.from_line(4))      # 直线布局
plot_coupling_map(CouplingMap.from_grid(3, 3))   # 环形布局兜底
```

### 4. 方法对比折线图

```python
from quonic.viz import plot_method_comparison

plot_method_comparison("clifford")   # statevector / stabilizer / MPS 随 n 的耗时
plot_method_comparison("low_tw")
```

数据来自 `scheduler/data/benchmarks.json`（对数 y 轴，展示 2^n 墙）。

### 5. 调度决策树

```python
from quonic.viz import plot_decision_tree

plot_decision_tree()
```

树结构固定：噪声 → `density_matrix`，其余按决策类别 + 实测交叉点选方法，
交叉点阈值自动从实测数据读取。

### 6. 方法选择热力图

```python
from quonic.viz import plot_method_heatmap

plot_method_heatmap()   # 行 = 决策类别，列 = 比特数，格子 = 所选方法
```

### 7. 降级链路径图

```python
from quonic.viz import plot_fallback_chain

plot_fallback_chain()   # qiskit → cirq → pennylane → native（自研兜底）
```

### 8. 量子比特活跃度热力图

```python
from quonic.viz import plot_qubit_activity

plot_qubit_activity(circuit)   # 行 = qubit，列 = 门序列，着色 = 被触及
```

### 9. 电路特征雷达图

```python
from quonic.viz import plot_feature_radar
from quonic.scheduler import circuit_features

plot_feature_radar(circuit)                    # 直接传 Circuit
plot_feature_radar(circuit_features(circuit))  # 或传特征 dict
```

### 10. 能量收敛图

```python
from quonic.algorithms import vqe
from quonic.viz import plot_energy_convergence

hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
result = vqe(hamiltonian, 2, record_history=True)   # 记录每步能量
plot_energy_convergence(result)
```

`record_history=True` 把每步能量写入 `result.metadata["history"]`；也接受
裸能量列表 `plot_energy_convergence([1.0, 0.5, 0.3])`。

### 11. Grover 迭代振幅图

```python
from quonic.viz import plot_grover_amplitudes

plot_grover_amplitudes(3, "101")   # 3 比特搜索 |101>，目标态概率随迭代振荡
```

用自研 `StatevectorEngine` 逐步模拟，不依赖任何后端，纯教学用。

### 12. 态向量可视化

```python
import numpy as np
from quonic.viz import plot_statevector

plot_statevector(np.array([1, 0, 0, 0], dtype=complex))  # 裸数组
plot_statevector(circuit)                                 # 或 Circuit
```

上图幅值、下图相位，按基态索引排列。

### 13. 噪声成本热力图

```python
from quonic.viz import plot_noise_heatmap

plot_noise_heatmap()  # 横轴 n，纵轴去极化概率 p，色块 = log10(耗时/s)
```

密度矩阵模拟成本按 4^n 增长，红框标出超过预算 `budget` 秒的不可行格子。

### 14. 布洛赫球

```python
import numpy as np
from quonic.viz import plot_bloch_sphere, plot_bloch_multivector

plot_bloch_sphere(np.array([1, 1], dtype=complex) / np.sqrt(2))  # |+> → +x
plot_bloch_sphere((0, 0, 1))                                     # 直接传布洛赫向量

# 多比特态：每个比特一个布洛赫球（约化单比特密度矩阵）
ghz = np.zeros(1024, dtype=complex)
ghz[0] = ghz[-1] = 1.0
ghz /= np.sqrt(2)
plot_bloch_multivector(ghz, cols=5)              # 每个球标注 |r|（纯/混合）
plot_bloch_multivector(ghz, cols=5, annotate=True)  # 额外在球下标注精确 (x, y, z)
```

纯态箭头为蓝、混合态为橙红；`|r|` 是布洛赫矢量模长（1 = 纯态在球面，
<1 = 混合态缩进球内），但方向由 (x, y, z) 三个分量决定——GHZ 各比特
`|r|=0`（球心）、QFT|x> 各比特 `|r|=1` 但方向各异（赤道相位梯度）。

### 15. 密度矩阵热力图

```python
from quonic.viz import plot_density_matrix

plot_density_matrix(circuit)   # 实部/虚部双面板
```

接受 `DensityMatrixEngine` / `StatevectorEngine` / `Circuit` / 复数组。

### 16. 纠缠可视化

```python
import numpy as np
from quonic.viz import plot_entanglement

bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
plot_entanglement(bell, partition=[0])   # 纠缠谱 + 冯诺依曼熵（2 比特附加并发度）
```

`partition` 是子系 A 的比特下标，默认取前一半。

### 17. 门矩阵可视化

```python
from quonic.viz import plot_gate_matrix

plot_gate_matrix("cx")   # 也可传 Gate 对象或 GateOperation
```

### 18. SWAP 路由可视化

```python
from quonic import CouplingMap
from quonic.viz import plot_routing

plot_routing(circuit, CouplingMap.from_line(3))   # 橙色叉号 = 插入的 SWAP
```

### 19. 逐门态演化

```python
from quonic.viz import plot_state_evolution

plot_state_evolution(circuit)   # 横轴门序列，纵轴基态，色块 = |振幅|²
```

### 20. 问题图

```python
from quonic.viz import plot_problem_graph

plot_problem_graph([(0, 1), (1, 2), (0, 2)])                  # 三角形图
plot_problem_graph([(0, 1), (1, 2), (0, 2)], partition={0: 0, 1: 1, 2: 1})  # 高亮割
```

### 21. 哈密顿量可视化

```python
from quonic.viz import plot_hamiltonian

plot_hamiltonian([(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")])  # 左系数柱状图，右算符热力图
```

### 22. 纠缠熵谱

```python
import numpy as np
from quonic.viz import plot_entanglement_profile

ghz = np.array([1, 0, 0, 0, 0, 0, 0, 1], dtype=complex) / np.sqrt(2)
plot_entanglement_profile(ghz)   # 所有二分切口的纠缠熵（GHZ 处处为 1）
```

### 23. 噪声叠加电路图

```python
from quonic.viz import plot_noisy_circuit

plot_noisy_circuit(circuit, noise=0.1)   # 每个门背景色 = 去极化噪声率
```

## 设计要点

- **单依赖**：`matplotlib` 是唯一可视化依赖，热力图/雷达图/树全部手绘，
  不引入 Seaborn（重）、Graphviz（系统级）、NetworkX（布局自己算）。
- **懒加载**：`import quonic` 零 matplotlib 开销，调用 `plot_*` 才加载。
- **中文字体**：自动探测 Microsoft YaHei / SimHei 等，找不到回退英文。
- **不侵入**：所有图都返回 Axes，可塞进用户自己的 subplot 布局。
