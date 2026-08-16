"""调度器数据源接口：查表推荐 + 记录结果。

统一接口支撑多种来源，调度核心与存储方式完全解耦：

- BuiltinRegistry   —— 规则兜底（无外部表时的保守选择，只读）
- MemoryRegistry    —— 内存映射表（测试 / 一次性任务）
- FileRegistry      —— 只读静态参数表（从文件或网站导入，冷启动用）
- LocalCacheRegistry—— 可写的本地缓存（用户自己的经验表，越用越准）
"""

import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .capabilities import decision_class, eligible_methods


class BackendRegistry(ABC):
    """调度器与外部数据源的统一接口。"""

    @abstractmethod
    def get_recommendation(self, features):
        """根据电路特征返回推荐后端名；查不到返回 None。"""

    def report_result(self, features, backend_name, duration, memory):
        """记录一次运行结果，用于未来优化调度（默认不做事）。"""
        return None


class BuiltinRegistry(BackendRegistry):
    """内置规则兜底：无外部表时的保守选择。"""

    def get_recommendation(self, features):
        # 当前三个后端都是状态矢量模拟器，能力一致，qiskit(Aer) 最快
        return "qiskit"

    def __repr__(self):
        return "BuiltinRegistry()"


# 冷启动兜底阈值：无实测数据时用的保守交叉点（n=24）。实测表会覆盖它。
_DEFAULT_DECISION = {
    "clifford": {"method": "stabilizer", "above_n": 24},
    "low_tw": {"method": "matrix_product_state", "above_n": 24},
}


@dataclass(frozen=True)
class Recommendation:
    """调度决策结果：后端名 + 模拟 method。"""

    backend: str
    method: str = "statevector"


_benchmark_cache = None  # None = 尚未加载


def _load_benchmarks():
    """读取整份 data/benchmarks.json；找不到/解析失败返回空 dict。"""
    global _benchmark_cache
    if _benchmark_cache is None:
        try:
            import json
            import os

            path = os.path.join(os.path.dirname(__file__), "data", "benchmarks.json")
            with open(path, encoding="utf-8") as f:
                _benchmark_cache = json.load(f)
        except (OSError, ValueError):
            _benchmark_cache = {}
    return _benchmark_cache


def load_measured_decision():
    """加载实测决策表（decision 字段）；找不到/解析失败时返回空 dict。"""
    return _load_benchmarks().get("decision", {})


def load_performance():
    """加载实测性能数据（performance 字段）；找不到时返回空列表。"""
    return _load_benchmarks().get("performance", [])


def load_noise_cost():
    """加载实测噪声成本（noise 字段）；找不到/解析失败时返回空 dict。

    内容：{"method": "density_matrix", "noise": ..., "performance": [...],
    "infeasible_n": ...}，由 scheduler.benchmark 生成，供 qshow 等在噪声场景下
    按实测数据提示成本（4^n 资源），而不是盲选 density_matrix。
    """
    return _load_benchmarks().get("noise", {})


def recommend_method(features, noise=False):
    """解析电路结构选出 method：先查实测表，再回退冷启动规则。

    硬约束（能力）：有噪声只能 density_matrix；stabilizer 只吃基础 Clifford。
    软选择（性能）：在能力允许的方法里挑实测最快（无实测数据用默认阈值）。

    - 噪声                         -> density_matrix
    - 基础 Clifford 且 n>=交叉点   -> stabilizer（多项式级）
    - 低树宽 且 n>=交叉点          -> matrix_product_state（低纠缠）
    - 否则                         -> statevector
    """
    if noise:
        return "density_matrix"
    n = features["n"]
    gate_types = set(features["gate_types"])
    cls = decision_class(features)
    if cls == "general":
        return "statevector"

    measured = load_measured_decision()
    entry = measured.get(cls) if measured else None
    if entry is None:
        entry = _DEFAULT_DECISION.get(cls)

    if entry and n >= entry["above_n"]:
        method = entry["method"]
        if method in eligible_methods(gate_types):
            return method
    return "statevector"


class MemoryRegistry(BackendRegistry):
    """内存中的 key -> backend 映射表。"""

    def __init__(self, table=None):
        self.table = dict(table or {})

    def get_recommendation(self, features):
        return self.table.get(features["key"])

    def __repr__(self):
        return f"MemoryRegistry({len(self.table)} 项)"


class FileRegistry(BackendRegistry):
    """只读静态参数表：从 JSON 文件加载 key -> backend 映射。"""

    def __init__(self, path):
        with open(path, encoding="utf-8") as f:
            self.table = json.load(f)

    def get_recommendation(self, features):
        return self.table.get(features["key"])

    def __repr__(self):
        return f"FileRegistry({len(self.table)} 项)"


class LocalCacheRegistry(BackendRegistry):
    """本地持久化缓存：记录用户自己跑过的 (key -> backend)。

    微调电路时 key 不变，直接命中缓存，无需重新决策。report_result 会
    把每次运行结果写回文件，下次查询即可复用。
    """

    def __init__(self, path):
        self.path = path
        self.table = {}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self.table = json.load(f)

    def get_recommendation(self, features):
        return self.table.get(features["key"])

    def report_result(self, features, backend_name, duration, memory):
        self.table[features["key"]] = backend_name
        self._save()

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.table, f, ensure_ascii=False, indent=2)

    def __repr__(self):
        return f"LocalCacheRegistry({len(self.table)} 项, {self.path})"
