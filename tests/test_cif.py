"""cif —— 经典控制流（先测量再分支）测试。

核心验证点：cif 与 qif 不同，它**先测量**控制比特再二选一施加分支门，
产生经典混合态而非相干纠缠。用「H⊗H 旋转回读」区分两者：经典混合在
旋转后四个基态各 ~25%，而 qif 的纠缠态会给出 |00>/|11> 各 ~50%。
"""

import pytest

from quonic import cif, qgate, reset
from quonic.backends import get_backend
from quonic.gates import CX, MEASURE, H, I, X, Z
from quonic.stack import current_circuit


def _run(shots, backend="native", **kwargs):
    return get_backend(backend).run(current_circuit(), shots=shots, **kwargs)


# ---------------------------------------------------------------------------
# 1. 确定性控制：分支按测量结果二选一
# ---------------------------------------------------------------------------

def test_cif_then_branch():
    reset()
    qgate(X, 0)  # q0 = |1>
    cif(0).then(X, 1).else_(I, 1)  # 测到 1 -> X(q1)
    result = _run(shots=256)
    assert result.counts == {"11": 256}


def test_cif_else_branch():
    reset()
    # q0 = |0>（默认），测到 0 -> else 分支 I(q1)，目标保持 |0>
    cif(0).then(X, 1).else_(I, 1)
    result = _run(shots=256)
    assert result.counts == {"00": 256}


def test_cif_else_branch_active():
    # else 分支也应是实际施加的门：q0=|0> -> Z(q1)（Z|0>=|0>）不足以区分，
    # 改用 else=X 翻转目标，确认 else 分支真正生效
    reset()
    cif(0).then(I, 1).else_(X, 1)
    result = _run(shots=256)
    # qubit0 是最低位（比特串最右侧）：q0=0, q1=1 -> "10"
    assert result.counts == {"10": 256}


# ---------------------------------------------------------------------------
# 2. 叠加控制 -> 经典混合（非纠缠）
# ---------------------------------------------------------------------------

def test_cif_superposition_is_classical_mixture():
    reset()
    qgate(H, 0)
    cif(0).then(X, 1).else_(Z, 1)
    qgate(H, 0)
    qgate(H, 1)
    result = _run(shots=4096)
    counts = result.counts
    total = sum(counts.values())
    # 经典混合旋转后四个基态各 ~25%；qif 的纠缠态会让 |01>/|10> 消失
    for bs in ("00", "01", "10", "11"):
        assert 0.15 < counts.get(bs, 0) / total < 0.35, f"{bs}: {counts}"


def test_cif_density_matrix_method():
    reset()
    qgate(H, 0)
    cif(0).then(X, 1).else_(Z, 1)
    qgate(H, 0)
    qgate(H, 1)
    result = _run(shots=4096, method="density_matrix")
    counts = result.counts
    total = sum(counts.values())
    for bs in ("00", "01", "10", "11"):
        assert 0.15 < counts.get(bs, 0) / total < 0.35, f"{bs}: {counts}"


# ---------------------------------------------------------------------------
# 3. 后端支持范围
# ---------------------------------------------------------------------------

def test_cif_qiskit_backend():
    pytest.importorskip("qiskit_aer")
    reset()
    qgate(X, 0)
    cif(0).then(X, 1).else_(I, 1)
    result = _run(shots=256, backend="qiskit")
    assert result.counts == {"11": 256}


def test_cif_rejects_stabilizer():
    reset()
    qgate(H, 0)
    cif(0).then(X, 1).else_(Z, 1)
    with pytest.raises(NotImplementedError):
        _run(shots=16, method="stabilizer")


@pytest.mark.parametrize("backend", ["cirq", "pennylane"])
def test_cif_rejects_unsupported_backends(backend):
    reset()
    qgate(H, 0)
    cif(0).then(X, 1).else_(Z, 1)
    with pytest.raises(NotImplementedError):
        _run(shots=16, backend=backend)


# ---------------------------------------------------------------------------
# 4. 错误分支
# ---------------------------------------------------------------------------

def test_cif_requires_then_branch():
    reset()
    with pytest.raises(ValueError, match="missing then"):
        cif(0).else_(Z, 1)


def test_cif_rejects_different_targets():
    reset()
    with pytest.raises(ValueError, match="same target"):
        cif(0).then(X, 1).else_(Z, 2)


def test_cif_rejects_multi_qubit_branch():
    reset()
    with pytest.raises(ValueError, match="single-qubit"):
        cif(0).then(CX, 1).else_(Z, 1)


def test_cif_rejects_measure_branch():
    reset()
    with pytest.raises(ValueError, match="unitary"):
        cif(0).then(MEASURE, 1).else_(Z, 1)


def test_cif_rejects_control_equals_target():
    reset()
    with pytest.raises(ValueError, match="cannot be the same"):
        cif(0).then(X, 0).else_(Z, 0)
