"""后端无关的中间表示（IR）。

qgate() 先把用户操作记录成与后端无关的 GateOperation / Circuit，
qshow() 再交给具体后端（Qiskit / Cirq / ...）翻译执行。
"""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class GateOperation:
    name: str
    qubits: Tuple[int, ...]
    params: Tuple[float, ...] = ()


@dataclass(frozen=True)
class ClassicalIfOperation:
    """经典控制流：按控制源二选一施加分支门。

    与 qif 的量子叠加不同，这里产生经典混合态（非相干纠缠）。
    control 可为：
      - int：测量该 qubit（先测量再分支）
      - str：读取具名经典位 creg 中已存好的测量结果
    then_op / else_op 为单比特分支门。
    """

    control: object
    then_op: GateOperation
    else_op: GateOperation

    @property
    def name(self):
        return "cif"

    @property
    def params(self):
        return ()

    @property
    def qubits(self):
        qs = set()
        if isinstance(self.control, int):
            qs.add(self.control)
        qs.update(self.then_op.qubits)
        qs.update(self.else_op.qubits)
        return tuple(sorted(qs))


@dataclass(frozen=True)
class CMeasureOperation:
    """测量 qubit，把结果存入具名经典位 creg。"""

    qubit: int
    creg: str

    @property
    def name(self):
        return "cmeasure"

    @property
    def params(self):
        return ()

    @property
    def qubits(self):
        return (self.qubit,)


@dataclass(frozen=True)
class ClassicalWhileOperation:
    """经典反馈循环：重复执行 body，直到 creg 的测量结果等于 until。

    body 为 ops 元组（通常以 creg.measure(...) 结尾更新条件），
    是 repeat-until-success（RUS）动态电路的核心。
    """

    creg: str
    until: int
    body: Tuple[object, ...]

    @property
    def name(self):
        return "cwhile"

    @property
    def params(self):
        return ()

    @property
    def qubits(self):
        qs = set()
        for op in self.body:
            qs.update(op.qubits)
        return tuple(sorted(qs))


_MEASURE_NAMES = ("measure", "cmeasure")


class Circuit:
    def __init__(self):
        self.ops: List[GateOperation] = []
        self.num_qubits: int = 0

    def add(self, op) -> None:
        self.ops.append(op)
        for q in op.qubits:
            if q + 1 > self.num_qubits:
                self.num_qubits = q + 1

    def allocate(self, n_qubits: int) -> None:
        # 预占量子比特（不发门），供 QInt 等类型在无初始门时也能占据下标
        if n_qubits > self.num_qubits:
            self.num_qubits = n_qubits

    def measured_qubits(self):
        measured = set()
        for op in self.ops:
            if op.name == "measure":
                measured.add(op.qubits[0])
            elif op.name == "cmeasure":
                measured.add(op.qubit)
            elif op.name == "cif":
                if isinstance(op.control, int):
                    measured.add(op.control)
        return measured

    def unmeasured_qubits(self):
        measured = self.measured_qubits()
        return [q for q in range(self.num_qubits) if q not in measured]

    def is_empty(self):
        return not self.ops

    def gate_count(self):
        """逻辑门数（不含测量门）。"""
        return sum(1 for op in self.ops if op.name not in _MEASURE_NAMES)

    def depth(self):
        """电路深度：非测量门的最长依赖链（按量子比特时钟同步多比特门）。"""
        clocks = [0] * self.num_qubits
        for op in self.ops:
            if op.name in _MEASURE_NAMES:
                continue
            d = max(clocks[q] for q in op.qubits) + 1
            for q in op.qubits:
                clocks[q] = d
        return max(clocks) if clocks else 0
