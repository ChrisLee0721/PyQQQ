"""电路特征提取：为调度器提供可哈希的分桶键。

特征只依赖门列表（不运行电路），O(门数) 内算完。分桶故意做粗，
让「微调电路」前后（迭代次数 +1、深度 ±几）仍落在同一个 key，从而
直接命中本地缓存，避免每次都重新决策。
"""

from .capabilities import CLIFFORD_GATES


def _gate_types(circuit):
    return sorted(
        {op.name for op in circuit.ops if op.name not in ("measure", "cmeasure")}
    )


def _interaction_graph(circuit):
    """两/多比特门连接的 qubit 对构成无向边，用于估计纠缠结构。"""
    edges = set()
    for op in circuit.ops:
        if op.name in ("measure", "cmeasure"):
            continue
        qs = op.qubits
        for i in range(len(qs)):
            for j in range(i + 1, len(qs)):
                edges.add((qs[i], qs[j]))
    return edges


def _treewidth_upper_bound(n, edges):
    """min-degree 消元给出的 treewidth 上界（张量网络复杂度的代理）。"""
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    active = set(range(n))
    width = 0
    while active:
        v = min(active, key=lambda x: len(adj[x] & active))
        neigh = list(adj[v] & active)
        width = max(width, len(neigh))
        for i in range(len(neigh)):
            for j in range(i + 1, len(neigh)):
                a, b = neigh[i], neigh[j]
                adj[a].add(b)
                adj[b].add(a)
        active.remove(v)
    return width


def _bucket_key(f):
    n = f["n"]
    n_bucket = "n<8" if n < 8 else ("n<16" if n < 16 else ("n<24" if n < 24 else "n>=24"))
    cliff = "clifford" if f["is_clifford"] else "nonclifford"
    tw = f["treewidth_ub"]
    tw_bucket = "tw0" if tw == 0 else ("tw<4" if tw < 4 else "tw>=4")
    depth_bucket = f"d{f['depth'] // 50}"
    return f"{n_bucket}|{cliff}|{tw_bucket}|{depth_bucket}"


def circuit_features(circuit):
    """提取电路特征，返回 dict，其中 features['key'] 是可哈希的分桶键。"""
    gate_types = _gate_types(circuit)
    edges = _interaction_graph(circuit)
    tw = _treewidth_upper_bound(circuit.num_qubits, edges)
    is_clifford = all(g in CLIFFORD_GATES for g in gate_types)
    feats = {
        "n": circuit.num_qubits,
        "depth": circuit.depth(),
        "gate_count": circuit.gate_count(),
        "gate_types": gate_types,
        "is_clifford": is_clifford,
        "treewidth_ub": tw,
    }
    feats["key"] = _bucket_key(feats)
    return feats
