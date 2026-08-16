"""@oracle 装饰器：把经典谓词编译成 Grover 相位神谕。

     from quonic.algorithms import grover, oracle

     @oracle(3)
     def f(x):
         return x == 5            # 标记 |101>（qubit0 在最低位）

     result = grover(f, 3)        # 搜索唯一满足 f 的状态
"""

from .grover import mark_state


def oracle(n_qubits):
    """装饰器：把一个经典谓词 f(x) -> bool 变成 Grover 相位神谕。

    f 接受整数 x（0 <= x < 2**n_qubits），返回 True 表示标记该状态。
    所有满足 f(x)=True 的状态都会被施加 -1 相位。

    返回的装饰器把 f 包装成 oracle(circuit) 回调，可直接传给 grover()，
    也可传给 quantum_counting()（后者会读取其 .marked 属性）。

    参数：
        n_qubits: 谓词作用的量子比特数。
    """
    if not isinstance(n_qubits, int) or n_qubits < 1:
        raise ValueError(f"n_qubits 必须是正整数，收到 {n_qubits!r}")

    def decorator(f):
        marked = tuple(x for x in range(2 ** n_qubits) if f(x))

        def phase_oracle(circuit):
            for x in marked:
                mark_state(format(x, f"0{n_qubits}b"))(circuit)

        phase_oracle.marked = marked
        phase_oracle.n_qubits = n_qubits
        phase_oracle.__name__ = getattr(f, "__name__", "oracle")
        return phase_oracle

    return decorator
