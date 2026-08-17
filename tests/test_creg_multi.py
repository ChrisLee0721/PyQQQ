"""多比特 creg：宽寄存器 + cif/cwhile 比特串判据 + groverize 推广。"""

import pytest

from quonic import cif, creg, cwhile, qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, I, X
from quonic.stack import current_circuit


def _run(shots=256, backend="native", **kwargs):
    return get_backend(backend).run(current_circuit(), shots=shots, **kwargs)


# ---------------------------------------------------------------------------
# 1. creg 宽度 API
# ---------------------------------------------------------------------------

def test_creg_width_default():
    assert creg("flag").width == 1


def test_creg_width_two():
    assert creg("flag", width=2).width == 2


def test_creg_repr_multi():
    assert repr(creg("flag", width=2)) == "CReg('flag', width=2)"


def test_creg_rejects_zero_width():
    with pytest.raises(ValueError, match="width"):
        creg("flag", width=0)


def test_creg_measure_rejects_bit_out_of_range():
    reset()
    reg = creg("reg", width=2)
    with pytest.raises(ValueError, match="bit"):
        reg.measure(0, bit=2)


def test_creg_getitem_measure_equivalence():
    reset()
    qgate(X, 1)
    reg = creg("reg", width=2)
    reg[0].measure(0)  # 等价于 reg.measure(0, bit=0)
    reg[1].measure(1)  # 等价于 reg.measure(1, bit=1)
    cif(reg, 2).then(X, 2).else_(I, 2)
    result = _run(shots=256)
    assert result.counts == {"110": 256}


# ---------------------------------------------------------------------------
# 2. native 多比特 cif / cwhile
# ---------------------------------------------------------------------------

def test_cif_multi_register_value():
    reset()
    qgate(X, 1)  # bit1 = 1
    reg = creg("reg", width=2)
    reg.measure(0, bit=0)  # bit0 = 0
    reg.measure(1, bit=1)  # bit1 = 1 -> 寄存器值 2
    cif(reg, 2).then(X, 2).else_(I, 2)
    result = _run(shots=256)
    # q2=1, q1=1, q0=0 -> "110"
    assert result.counts == {"110": 256}


def test_cif_multi_register_else():
    reset()
    reg = creg("reg", width=2)
    reg.measure(0, bit=0)  # bit0 = 0
    reg.measure(1, bit=1)  # bit1 = 0 -> 寄存器值 0
    cif(reg, 2).then(X, 2).else_(I, 2)  # reg != 2 -> else I(q2)
    result = _run(shots=256)
    assert result.counts == {"000": 256}


def test_cif_multi_bitstring_value():
    reset()
    qgate(X, 1)
    reg = creg("reg", width=2)
    reg.measure(0, bit=0)
    reg.measure(1, bit=1)
    cif(reg, "10").then(X, 2).else_(I, 2)
    result = _run(shots=256)
    assert result.counts == {"110": 256}


def test_cwhile_multi_until_value():
    # 循环直到寄存器值 == 3 ("11")：两比特都 H+measure，直到同时测到 1
    reset()
    reg = creg("reg", width=2)
    with cwhile(reg, until=3):
        qgate(H, 0)
        qgate(H, 1)
        reg.measure(0, bit=0)
        reg.measure(1, bit=1)
    result = _run(shots=1024)
    assert result.counts == {"11": 1024}


def test_cwhile_multi_bitstring_until():
    reset()
    reg = creg("reg", width=2)
    with cwhile(reg, until="11"):
        qgate(H, 0)
        qgate(H, 1)
        reg.measure(0, bit=0)
        reg.measure(1, bit=1)
    result = _run(shots=1024)
    assert result.counts == {"11": 1024}


def test_cwhile_rejects_until_out_of_range():
    reset()
    reg = creg("reg", width=2)
    with pytest.raises(ValueError, match="until"):
        cwhile(reg, until=4)


def test_cwhile_rejects_bad_bitstring():
    reset()
    reg = creg("reg", width=2)
    with pytest.raises(ValueError):
        cwhile(reg, until="2x")


def test_cif_rejects_value_out_of_range():
    reset()
    reg = creg("reg", width=2)
    with pytest.raises(ValueError, match="value"):
        cif(reg, 4).then(X, 2).else_(I, 2)


# ---------------------------------------------------------------------------
# 3. groverize 推广：多比特成功态放大到 1
# ---------------------------------------------------------------------------

def test_groverize_multi_until2():
    # 两比特 H+H，成功 = 寄存器值 2 ("10")，p=1/4 -> 放大到确定性
    reset()
    reg = creg("reg", width=2)
    with cwhile(reg, until=2) as loop:
        qgate(H, 0)
        qgate(H, 1)
        reg.measure(0, bit=0)
        reg.measure(1, bit=1)
    static = loop.groverize()
    result = get_backend("native").run(static, shots=1024)
    # 输出 4 比特：ancilla 寄存器(左 2 位 "10") + 数据(q1 q0 = "10")
    assert result.counts == {"1010": 1024}


def test_groverize_multi_until3():
    reset()
    reg = creg("reg", width=2)
    with cwhile(reg, until=3) as loop:
        qgate(H, 0)
        qgate(H, 1)
        reg.measure(0, bit=0)
        reg.measure(1, bit=1)
    static = loop.groverize()
    result = get_backend("native").run(static, shots=1024)
    # ancilla "11" + 数据 "11"
    assert result.counts == {"1111": 1024}


def test_groverize_multi_infer_prob_matches():
    # auto-infer p 对 2 比特均匀叠加应为 1/4（通过结果确定性间接验证）
    reset()
    reg = creg("reg", width=2)
    with cwhile(reg, until=0) as loop:
        qgate(H, 0)
        qgate(H, 1)
        reg.measure(0, bit=0)
        reg.measure(1, bit=1)
    static = loop.groverize()
    result = get_backend("native").run(static, shots=1024)
    assert result.counts == {"0000": 1024}


def test_groverize_multi_rejects_missing_bit():
    # 循环体两次测 bit0（缺 bit1）-> groverize 拒绝
    reset()
    reg = creg("reg", width=2)
    with cwhile(reg, until=1) as loop:
        qgate(H, 0)
        qgate(H, 1)
        reg.measure(0, bit=0)
        reg.measure(1, bit=0)
    with pytest.raises(ValueError, match="bit"):
        loop.groverize()


# ---------------------------------------------------------------------------
# 4. 后端覆盖：多比特 creg 支持 native / qiskit / cirq / pennylane
# ---------------------------------------------------------------------------

def test_multi_creg_qiskit_cif():
    pytest.importorskip("qiskit_aer")
    reset()
    qgate(X, 1)
    reg = creg("reg", width=2)
    reg.measure(0, bit=0)
    reg.measure(1, bit=1)
    cif(reg, 2).then(X, 2).else_(I, 2)
    result = _run(shots=256, backend="qiskit")
    # qiskit 具名寄存器格式 "reg_bits flat_bits"；flat 最高位是 q2
    counts = result.counts
    assert len(counts) == 1
    reg_bits, flat_bits = next(iter(counts)).split(" ")
    assert reg_bits == "10"  # 寄存器值 2
    assert flat_bits[0] == "1"  # q2 被 then 分支翻转


@pytest.mark.parametrize("backend", ["cirq", "pennylane"])
def test_multi_creg_cif_then_cirq_pennylane(backend):
    pytest.importorskip(backend)
    reset()
    qgate(X, 1)  # bit1 = 1 -> 寄存器值 2
    reg = creg("reg", width=2)
    reg.measure(0, bit=0)
    reg.measure(1, bit=1)
    cif(reg, 2).then(X, 2).else_(I, 2)
    result = _run(shots=256, backend=backend)
    # q2=1, q1=1, q0=0 -> "110"
    assert result.counts == {"110": 256}


@pytest.mark.parametrize("backend", ["cirq", "pennylane"])
def test_multi_creg_cif_else_cirq_pennylane(backend):
    pytest.importorskip(backend)
    reset()
    reg = creg("reg", width=2)
    reg.measure(0, bit=0)  # 寄存器值 0
    reg.measure(1, bit=1)
    cif(reg, 2).then(X, 2).else_(I, 2)  # reg != 2 -> else I(q2)
    result = _run(shots=256, backend=backend)
    assert result.counts == {"000": 256}


@pytest.mark.parametrize("backend", ["cirq", "pennylane"])
def test_multi_creg_bitstring_cif_cirq_pennylane(backend):
    pytest.importorskip(backend)
    reset()
    qgate(X, 0)  # bit0 = 1 -> 寄存器值 1
    reg = creg("reg", width=2)
    reg.measure(0, bit=0)
    reg.measure(1, bit=1)
    cif(reg, "01").then(X, 2).else_(I, 2)
    result = _run(shots=256, backend=backend)
    # q2=1, q1=0, q0=1 -> "101"
    assert result.counts == {"101": 256}


@pytest.mark.parametrize("backend", ["cirq", "pennylane"])
def test_cif_str_control_cirq_pennylane(backend):
    # 单比特寄存器 value=1 走 str 控制：cif(flag) 应等价于 cif(flag, 1)
    pytest.importorskip(backend)
    reset()
    qgate(X, 0)
    flag = creg("flag")
    flag.measure(0)
    cif(flag).then(X, 1).else_(I, 1)
    result = _run(shots=256, backend=backend)
    assert result.counts == {"11": 256}


@pytest.mark.parametrize("backend", ["cirq", "pennylane"])
def test_cif_single_bit_value_zero_cirq_pennylane(backend):
    # 单比特寄存器 value=0 走 CRegCondition(width=1)：cif(flag, 0)
    pytest.importorskip(backend)
    reset()
    qgate(X, 0)
    flag = creg("flag")
    flag.measure(0)
    cif(flag, 0).then(X, 1).else_(I, 1)  # flag == 1 != 0 -> else I(q1)
    result = _run(shots=256, backend=backend)
    # q1=0, q0=1 -> "01"
    assert result.counts == {"01": 256}
