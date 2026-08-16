"""耦合图（连通性）模型：描述量子比特之间哪些两比特门可以直接执行。

与后端无关、不碰任何真实硬件——只刻画「允许的两比特连接」这一物理事实，
供编译 seam（compiler.py）校验电路能否落在目标拓扑上，也是将来接真实硬件
/ 国产引擎时做路由的前置抽象。
"""


class CouplingMap:
    """无向耦合图：n 个量子比特 + 一组允许直接交互的边。"""

    def __init__(self, n, edges=()):
        if n < 0:
            raise ValueError(f"量子比特数需非负，收到 {n}")
        self.n = n
        self._edges = set()
        for u, v in edges:
            self._add_edge(u, v)

    def _add_edge(self, u, v):
        if u == v:
            raise ValueError(f"自环边 ({u}, {v}) 不合法")
        if u < 0 or v < 0 or u >= self.n or v >= self.n:
            raise ValueError(f"边 ({u}, {v}) 超出量子比特范围 [0, {self.n})")
        self._edges.add((min(u, v), max(u, v)))

    @classmethod
    def fully_connected(cls, n):
        """全连接：任意两个量子比特都能直接交互（模拟器的默认情形）。"""
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        return cls(n, edges)

    @classmethod
    def from_line(cls, n):
        """一维链：每个量子比特只与相邻的相连（n=0/1 时无边）。"""
        edges = [(i, i + 1) for i in range(n - 1)]
        return cls(n, edges)

    @classmethod
    def from_grid(cls, rows, cols):
        """二维网格：每个格点与右、下邻居相连（行优先编号）。"""
        n = rows * cols
        edges = []
        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                if c + 1 < cols:
                    edges.append((idx, idx + 1))
                if r + 1 < rows:
                    edges.append((idx, idx + cols))
        return cls(n, edges)

    def has_edge(self, u, v):
        """u 与 v 之间是否允许直接两比特门。"""
        return (min(u, v), max(u, v)) in self._edges

    def edges(self):
        """排序后的边列表（元组，小端在前）。"""
        return sorted(self._edges)

    def __len__(self):
        return self.n

    def __repr__(self):
        return f"CouplingMap(n={self.n}, edges={self.edges()})"
