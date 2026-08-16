"""模拟方法的静态能力矩阵：调度决策的「硬约束」层。

能力不匹配是硬约束（直接排除该方法），性能数据是「软选择」（在剩余方法里
挑最快）。这里只记录与具体机器无关的静态事实：

- 每种方法能吃哪些门（基础 Clifford / 全 Clifford / 任意非 Clifford）
- 每种方法是否支持去极化噪声

性能数据（耗时）在 benchmark.py 里实测，二者分离：能力稳定可白送，
性能随机器漂移需重跑校准。
"""

BASIC_CLIFFORD = {"h", "x", "y", "z", "cx", "cz"}
"""Aer 的 stabilizer 方法只接受这组基础 Clifford 门（不含 mcz / cp / ccx）。"""

CLIFFORD_GATES = BASIC_CLIFFORD | {"mcz"}
"""完整 Clifford 门集（含多控制 Z）。用于 is_clifford 判断。"""


METHOD_CAPABILITIES = {
    "statevector": {
        "clifford": True,
        "nonclifford": True,
        "noise": False,
        "gates": "all",
    },
    "stabilizer": {
        "clifford": True,  # 仅基础 Clifford（不含 mcz）
        "nonclifford": False,
        "noise": False,
        "gates": "basic_clifford",
    },
    "matrix_product_state": {
        "clifford": True,
        "nonclifford": True,
        "noise": False,
        "gates": "all",
    },
    "density_matrix": {
        "clifford": True,
        "nonclifford": True,
        "noise": True,
        "gates": "all",
    },
}


def eligible_methods(gate_types, noise=False):
    """返回能跑该电路的方法集合（能力硬约束）。

    - 有噪声 -> 只有 density_matrix 支持
    - 基础 Clifford -> statevector / stabilizer / matrix_product_state
    - 其它（mcz / 任意角旋转等）-> statevector / matrix_product_state
    """
    if noise:
        return {"density_matrix"}
    gs = set(gate_types)
    methods = {"statevector", "matrix_product_state"}
    if gs <= BASIC_CLIFFORD:
        methods.add("stabilizer")
    return methods


def decision_class(features):
    """把电路特征归入三个决策类别，与 benchmark 的电路族一一对应。

    - "clifford"  —— 纯基础 Clifford，stabilizer 的用武之地
    - "low_tw"    —— 非基础 Clifford 但低树宽，MPS 的用武之地
    - "general"   —— 高纠缠/高树宽，只有 statevector 能高效跑
    """
    gs = set(features["gate_types"])
    if gs and gs <= BASIC_CLIFFORD:
        return "clifford"
    if features["treewidth_ub"] <= 4:
        return "low_tw"
    return "general"


__all__ = [
    "BASIC_CLIFFORD",
    "CLIFFORD_GATES",
    "METHOD_CAPABILITIES",
    "eligible_methods",
    "decision_class",
]
