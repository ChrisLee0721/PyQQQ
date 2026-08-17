"""groverize —— cwhile 的 Grover 振幅放大编译 pass 测试。

核心验证点：把 repeat-until-success 循环编译成静态 Grover 电路后，
单次成功概率 p 从 ~1/4 放大到 ~1（确定性），且结果与 native 逐 shot 回退一致。
"""

import math

import pytest

from quonic import creg, cwhile, groverize, qgate, reset
from quonic.backends import get_backend
from quonic.gates import Ry
from quonic.ir import ClassicalWhileOperation, CMeasureOperation, GateOperation
from quonic.stack import current_circuit


def _rus_op(angle: float, until: int) -> ClassicalWhileOperation:
    body = (
        GateOperation("ry", (0,), (angle,)),
        CMeasureOperation(0, "flag"),
    )
    return ClassicalWhileOperation("flag", until, body)


# ---------------------------------------------------------------------------
# 1. 放大成功态（p=1/4 -> ~1）
# ---------------------------------------------------------------------------

def test_groverize_amplifies_until0():
    # Ry(2π/3) 后测 q0，成功 (q0==0) 概率 p=1/4；Grover 化后集中到 |00>
    op = _rus_op(2 * math.pi / 3, 0)
    static = groverize(op, success_prob=0.25)
    result = get_backend("native").run(static, shots=1024)
    assert result.counts == {"00": 1024}


def test_groverize_amplifies_until1():
    # Ry(π/3) 后测 q0，成功 (q0==1) 概率 p=1/4；Grover 化后集中到 |11>
    op = _rus_op(math.pi / 3, 1)
    static = groverize(op, success_prob=0.25)
    result = get_backend("native").run(static, shots=1024)
    assert result.counts == {"11": 1024}


@pytest.mark.parametrize("backend", ["qiskit", "cirq", "pennylane"])
def test_groverize_backends(backend):
    if backend == "qiskit":
        pytest.importorskip("qiskit_aer")
    else:
        pytest.importorskip(backend)
    op = _rus_op(2 * math.pi / 3, 0)
    static = groverize(op, success_prob=0.25)
    result = get_backend(backend).run(static, shots=256)
    assert result.counts == {"00": 256}


# ---------------------------------------------------------------------------
# 2. DSL 集成
# ---------------------------------------------------------------------------

def test_groverize_from_dsl():
    reset()
    flag = creg("flag")
    with cwhile(flag, until=0):
        qgate(Ry(2 * math.pi / 3), 0)
        flag.measure(0)
    op = current_circuit().ops[-1]
    static = groverize(op, success_prob=0.25)
    result = get_backend("native").run(static, shots=256)
    assert result.counts == {"00": 256}


# ---------------------------------------------------------------------------
# 2b. 平滑 API：auto-infer p + builder 方法
# ---------------------------------------------------------------------------

def test_groverize_auto_infers_prob():
    # 省略 success_prob：由模拟精确推断 p
    op = _rus_op(2 * math.pi / 3, 0)
    static = groverize(op)
    result = get_backend("native").run(static, shots=1024)
    assert result.counts == {"00": 1024}


def test_groverize_auto_infers_prob_until1():
    op = _rus_op(math.pi / 3, 1)
    static = groverize(op)
    result = get_backend("native").run(static, shots=1024)
    assert result.counts == {"11": 1024}


def test_groverize_builder_method():
    # with cwhile(...) as loop: 直接 loop.groverize()，不再手抠 ops[-1] 或手算 p
    reset()
    flag = creg("flag")
    with cwhile(flag, until=0) as loop:
        qgate(Ry(2 * math.pi / 3), 0)
        flag.measure(0)
    static = loop.groverize()
    result = get_backend("native").run(static, shots=256)
    assert result.counts == {"00": 256}


def test_groverize_builder_before_exit():
    reset()
    flag = creg("flag")
    loop = cwhile(flag, until=0)
    with pytest.raises(ValueError, match="with cwhile"):
        loop.groverize()


# ---------------------------------------------------------------------------
# 3. 错误分支
# ---------------------------------------------------------------------------

def test_groverize_rejects_non_cwhile():
    with pytest.raises(TypeError, match="cwhile"):
        groverize(GateOperation("h", (0,)), success_prob=0.25)


def test_groverize_rejects_bad_prob():
    op = _rus_op(2 * math.pi / 3, 0)
    with pytest.raises(ValueError, match="success_prob"):
        groverize(op, success_prob=0.0)
    with pytest.raises(ValueError, match="success_prob"):
        groverize(op, success_prob=1.0)


def test_groverize_rejects_nonunitary_body():
    # 循环体含终态测量门（非 cmeasure），非酉
    body = (GateOperation("h", (0,)), GateOperation("measure", (0,)))
    op = ClassicalWhileOperation("flag", 0, body)
    with pytest.raises(ValueError, match="unitary"):
        groverize(op, success_prob=0.25)


def test_groverize_rejects_missing_trailing_cmeasure():
    body = (GateOperation("h", (0,)),)
    op = ClassicalWhileOperation("flag", 0, body)
    with pytest.raises(ValueError, match="unitary"):
        groverize(op, success_prob=0.25)


def test_groverize_rejects_wrong_creg():
    # cmeasure 写入的 creg 与循环条件不一致
    body = (GateOperation("h", (0,)), CMeasureOperation(0, "other"))
    op = ClassicalWhileOperation("flag", 0, body)
    with pytest.raises(ValueError, match="unitary"):
        groverize(op, success_prob=0.25)
