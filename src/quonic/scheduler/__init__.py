"""调度器：按电路特征查表路由到最优后端。

查表链（优先级从高到低）：

    本地缓存 ──► 静态参数表 ──► 内置规则兜底

本地缓存是用户自己的经验表（跑过一次就记住），静态表是冷启动用的
通用基准（从文件或网站导入），规则兜底保证任何电路都有后端可跑。

示例：
    from quonic.scheduler import schedule, circuit_features, LocalCacheRegistry

    cache = LocalCacheRegistry(".quonic_cache.json")
    backend = schedule(circuit, cache=cache)   # 查缓存 -> 规则
"""

from .capabilities import (
    METHOD_CAPABILITIES,
    decision_class,
    eligible_methods,
)
from .features import circuit_features
from .registry import (
    BackendRegistry,
    BuiltinRegistry,
    FileRegistry,
    LocalCacheRegistry,
    MemoryRegistry,
    Recommendation,
    load_measured_decision,
    load_noise_cost,
    load_performance,
    recommend_method,
)

_BUILTIN = BuiltinRegistry()


def _parse(rec):
    """把查表结果解析成 (backend, method)；"qiskit" -> (qiskit, None)，
    "qiskit:stabilizer" -> (qiskit, stabilizer)，None -> (None, None)。"""
    if rec is None:
        return None, None
    if ":" in rec:
        backend, method = rec.split(":", 1)
        return backend, method
    return rec, None


def schedule(circuit, cache=None, table=None, noise=False):
    """返回调度决策（后端名 + 模拟 method）。

    参数：
        cache: 本地缓存（LocalCacheRegistry），优先级最高。
        table: 静态参数表（FileRegistry / MemoryRegistry），次之。
        noise: 是否启用去极化噪声（启用时 method 恒为 density_matrix）。
        两者都查不到时回退到内置规则。

    返回：Recommendation(backend=..., method=...)。查表结果可为
    "backend" 或 "backend:method"；method 未在表中指定时，由
    「解析电路」（recommend_method）补全，无需任何预存数据。
    """
    feats = circuit_features(circuit)
    backend = method = None
    for reg in (cache, table):
        if reg is not None and backend is None:
            backend, method = _parse(reg.get_recommendation(feats))
    if backend is None:
        backend = _BUILTIN.get_recommendation(feats)
    if method is None or noise:
        method = recommend_method(feats, noise=noise)
    return Recommendation(backend=backend, method=method)


__all__ = [
    "schedule",
    "circuit_features",
    "recommend_method",
    "load_measured_decision",
    "load_noise_cost",
    "load_performance",
    "Recommendation",
    "BackendRegistry",
    "BuiltinRegistry",
    "MemoryRegistry",
    "FileRegistry",
    "LocalCacheRegistry",
    "METHOD_CAPABILITIES",
    "eligible_methods",
    "decision_class",
]
