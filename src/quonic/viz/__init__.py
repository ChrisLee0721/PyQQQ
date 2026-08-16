"""QuoNic 全量可视化套件 —— 12 类图，只用 matplotlib。

可视化是可选能力：`import quonic` 不引入 matplotlib，调用任一 plot_* 时
才懒加载。依赖收敛到唯一的 `quonic[viz]`（matplotlib），不引入
Graphviz / Seaborn / NetworkX。

    from quonic.viz import plot_circuit, plot_counts

    plot_circuit(circuit)          # 门序列电路图
    plot_counts(result)            # 测量直方图

每个函数都接受可选 ax / show / save / title 参数，返回 matplotlib Axes
（plot_statevector 返回 Axes 列表），便于嵌入用户自己的 figure 或导出。
"""

from .algorithm import (
    plot_energy_convergence,
    plot_grover_amplitudes,
    plot_hamiltonian,
    plot_problem_graph,
)
from .circuit import (
    plot_circuit,
    plot_coupling_map,
    plot_qubit_activity,
    plot_statevector,
)
from .gate import plot_gate_matrix
from .noise import plot_noise_heatmap, plot_noisy_circuit
from .result import plot_counts
from .routing import plot_routing
from .scheduler import (
    plot_decision_tree,
    plot_fallback_chain,
    plot_feature_radar,
    plot_method_comparison,
    plot_method_heatmap,
)
from .state import (
    plot_bloch_multivector,
    plot_bloch_sphere,
    plot_density_matrix,
    plot_entanglement,
    plot_entanglement_profile,
    plot_state_evolution,
)

__all__ = [
    "plot_circuit",
    "plot_counts",
    "plot_coupling_map",
    "plot_method_comparison",
    "plot_decision_tree",
    "plot_method_heatmap",
    "plot_fallback_chain",
    "plot_qubit_activity",
    "plot_feature_radar",
    "plot_energy_convergence",
    "plot_grover_amplitudes",
    "plot_statevector",
    "plot_noise_heatmap",
    "plot_bloch_sphere",
    "plot_bloch_multivector",
    "plot_density_matrix",
    "plot_entanglement",
    "plot_gate_matrix",
    "plot_routing",
    "plot_state_evolution",
    "plot_problem_graph",
    "plot_hamiltonian",
    "plot_entanglement_profile",
    "plot_noisy_circuit",
]
