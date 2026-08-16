"""creg（具名经典寄存器）与 cwhile（测量反馈循环）测试。"""

import pytest

from quonic import cif, creg, cwhile, qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, I, X
from quonic.stack import current_circuit


def _run(shots=256, backend="native", **kwargs):
    return get_backend(backend).run(current_circuit(), shots=shots, **kwargs)


# ---------------------------------------------------------------------------
# creg：具名经典寄存器
# ---------------------------------------------------------------------------

def test_creg_measure_then_cif_then():
    reset()
    qgate(X, 0)  # qubit0 = |1>
    flag = creg("flag")
    flag.measure(0)  # flag = 1
    cif(flag).then(X, 1).else_(I, 1)  # 按 flag 分支 -> X(q1)
    result = _run(shots=256)
    assert result.counts == {"11": 256}


def test_creg_measure_then_cif_else():
    reset()
    flag = creg("flag")
    flag.measure(0)  # qubit0 = |0> -> flag = 0
    cif(flag).then(X, 1).else_(I, 1)  # else -> I(q1)
    result = _run(shots=256)
    assert result.counts == {"00": 256}


def test_creg_requires_nonempty_name():
    reset()
    with pytest.raises(ValueError, match="non-empty"):
        creg("")


def test_creg_repr():
    reset()
    assert repr(creg("flag")) == "CReg('flag')"


def test_creg_qiskit_flat_output():
    # qiskit 后端应输出与 native 一致的扁平比特串（非具名寄存器 "1 10" 格式）
    pytest.importorskip("qiskit_aer")
    reset()
    qgate(X, 0)
    flag = creg("flag")
    flag.measure(0)
    cif(flag).then(X, 1).else_(I, 1)
    result = _run(shots=256, backend="qiskit")
    assert result.counts == {"11": 256}


# ---------------------------------------------------------------------------
# cwhile：测量反馈循环（repeat-until-success）
# ---------------------------------------------------------------------------

def test_cwhile_single_iteration():
    reset()
    flag = creg("flag")
    with cwhile(flag, until=1):
        qgate(X, 0)
        flag.measure(0)
    result = _run(shots=256)
    # 初始 flag=0 != 1 -> 进入循环体 X(0)+measure -> flag=1 退出，qubit0=|1>
    assert result.counts == {"1": 256}


def test_cwhile_rus_deterministic_outcome():
    reset()
    flag = creg("flag")
    with cwhile(flag, until=0):
        qgate(H, 0)
        flag.measure(0)
    result = _run(shots=1024)
    # 每次 H+measure 都 50% 概率测到 0，循环直到 flag==0 才退出，
    # 因此退出时 qubit0 必然已坍缩到 |0>（迭代次数随机，结果确定）。
    assert result.counts == {"0": 1024}


def test_cwhile_rejects_non_creg():
    reset()
    with pytest.raises(TypeError, match="creg"):
        cwhile(0, until=0)


def test_cwhile_rejects_bad_until():
    reset()
    flag = creg("flag")
    with pytest.raises(ValueError, match="until"):
        cwhile(flag, until=2)


def test_cwhile_rejects_qiskit_backend():
    pytest.importorskip("qiskit_aer")
    reset()
    flag = creg("flag")
    with cwhile(flag, until=1):
        qgate(X, 0)
        flag.measure(0)
    with pytest.raises(NotImplementedError):
        _run(shots=16, backend="qiskit")


@pytest.mark.parametrize("backend", ["cirq", "pennylane"])
def test_cwhile_rejects_unsupported_backends(backend):
    reset()
    flag = creg("flag")
    with cwhile(flag, until=1):
        qgate(X, 0)
        flag.measure(0)
    with pytest.raises(NotImplementedError):
        _run(shots=16, backend=backend)
