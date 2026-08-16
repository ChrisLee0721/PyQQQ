"""QuoNic 自研后端：不依赖任何外部量子库，直接用四个朴素引擎。

这是"不绑定 + 组合"的兜底：无论用户切到哪个后端，只要电路适合
stabilizer / MPS 等非 statevector 方法，都可降级到这里跑（仅需 numpy）。

引擎在 run() 内延迟导入，保证 `import quonic` 不引入 numpy。
"""

from ..noise import resolve_noise
from ..result import Result
from .base import Backend

_METHODS = ("statevector", "stabilizer", "matrix_product_state", "density_matrix")


class NativeBackend(Backend):
    name = "native"
    methods = frozenset(_METHODS)

    def run(self, circuit, shots=1024, noise=None, method="statevector"):
        from ..simulators import (
            DensityMatrixEngine,
            MPSEngine,
            StabilizerEngine,
            StatevectorEngine,
        )

        nm = resolve_noise(noise)
        # 经典控制流（cif / creg / cwhile）需要逐 shot 模拟：中途测量会
        # 不可逆地坍缩态矢量
        if any(op.name in ("cif", "cmeasure", "cwhile") for op in circuit.ops):
            return self._run_dynamic(circuit, shots, nm, method)

        # 噪声模拟需要密度矩阵方法；其余引擎不支持通用噪声模型
        if nm.enabled:
            engine = DensityMatrixEngine(circuit.num_qubits, noise=nm)
        else:
            engines = {
                "statevector": StatevectorEngine,
                "stabilizer": StabilizerEngine,
                "matrix_product_state": MPSEngine,
                "density_matrix": DensityMatrixEngine,
            }
            if method not in engines:
                raise ValueError(
                    f"native 后端不支持方法 '{method}'，"
                    f"可用：{', '.join(sorted(engines))}"
                )
            engine = engines[method](circuit.num_qubits)

        for op in circuit.ops:
            engine.apply(op.name, list(op.qubits), op.params)
        return Result.from_counts(engine.sample(shots), shots)

    @classmethod
    def _run_dynamic(cls, circuit, shots, nm, method):
        from ..simulators import DensityMatrixEngine, StatevectorEngine

        if nm.enabled:
            method = "density_matrix"
        if method == "density_matrix":
            def new_engine():
                return DensityMatrixEngine(circuit.num_qubits, noise=nm)
        elif method == "statevector":
            def new_engine():
                return StatevectorEngine(circuit.num_qubits)
        else:
            raise NotImplementedError(
                f"native 后端的经典控制流（cif/creg/cwhile）仅支持 "
                f"statevector / density_matrix 方法，当前 method='{method}'"
            )

        counts = {}
        for _ in range(shots):
            engine = new_engine()
            cregs = {}
            cls._execute(engine, circuit.ops, cregs)
            for bs, c in engine.sample(1).items():
                counts[bs] = counts.get(bs, 0) + c
        return Result.from_counts(counts, shots)

    @staticmethod
    def _execute(engine, ops, cregs):
        """逐 shot 执行一段 ops，维护具名经典位 cregs（name -> 0/1）。"""
        for op in ops:
            name = op.name
            if name == "cmeasure":
                cregs[op.creg] = engine.measure_qubit(op.qubit)
            elif name == "cif":
                if isinstance(op.control, int):
                    outcome = engine.measure_qubit(op.control)
                else:
                    outcome = cregs.get(op.control, 0)
                branch = op.then_op if outcome == 1 else op.else_op
                engine.apply(branch.name, list(branch.qubits), branch.params)
            elif name == "cwhile":
                iters = 0
                while cregs.get(op.creg, 0) != op.until:
                    NativeBackend._execute(engine, op.body, cregs)
                    iters += 1
                    if iters > 100000:
                        raise RuntimeError(
                            f"cwhile 循环超过安全上限（100000 次），"
                            f"条件 creg={op.creg!r} 可能一直未满足"
                        )
            else:
                engine.apply(name, list(op.qubits), op.params)
