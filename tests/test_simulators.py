"""自研四引擎 + native 后端 + 能力降级测试。

四个引擎是"朴素版"，正确性用确定性断言（非统计）验证：statevector /
density / MPS 直接对比振幅，stabilizer 对比已知态或 statevector 分布。
"""

import numpy as np
import pytest

from quonic.ir import Circuit, GateOperation
from quonic.simulators import (
    DensityMatrixEngine,
    MPSEngine,
    StabilizerEngine,
    StatevectorEngine,
)


def _run(engine, gates):
    for name, qubits, params in gates:
        engine.apply(name, list(qubits), params)
    return engine


def _bell():
    return [("h", (0,), ()), ("cx", (0, 1), ())]


def _sv_probs(engine):
    p = np.abs(engine.state) ** 2
    return p / p.sum()


def _mps_sv(engine):
    n = engine.n
    out = np.zeros(2 ** n, dtype=complex)
    for idx in range(2 ** n):
        v = np.array([[1.0 + 0j]])
        for q in range(n):
            m = engine.M[q][:, (idx >> q) & 1, :]
            v = np.einsum("ab,bc->ac", v, m)
        out[idx] = v[0, 0]
    p = np.abs(out) ** 2
    return p / p.sum()


# ---------------------------------------------------------------------------
# statevector
# ---------------------------------------------------------------------------

def test_statevector_bell():
    sv = _run(StatevectorEngine(2), _bell())
    probs = _sv_probs(sv)
    assert probs[0] == pytest.approx(0.5)
    assert probs[3] == pytest.approx(0.5)
    assert probs[1] == pytest.approx(0.0)
    assert probs[2] == pytest.approx(0.0)


def test_statevector_bitstring_order():
    # X 作用于 qubit 1 -> 状态 index 0b10 = 2
    sv = _run(StatevectorEngine(2), [("x", (1,), ())])
    assert _sv_probs(sv)[2] == pytest.approx(1.0)


def test_statevector_rotation():
    # Rx(pi) 等价于 -iX，概率上把 |0> 翻成 |1>
    sv = _run(StatevectorEngine(1), [("rx", (0,), (np.pi,))])
    assert _sv_probs(sv)[1] == pytest.approx(1.0, abs=1e-9)


def test_statevector_identity():
    # I 门是恒等：|0> 保持 |0>
    sv = _run(StatevectorEngine(1), [("i", (0,), ())])
    assert _sv_probs(sv)[0] == pytest.approx(1.0, abs=1e-9)


def test_statevector_swap():
    # X(0) 得 |01>（index 1），swap(0,1) 后得 |10>（index 2）
    sv = _run(StatevectorEngine(2), [("x", (0,), ()), ("swap", (0, 1), ())])
    assert _sv_probs(sv)[2] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# stabilizer
# ---------------------------------------------------------------------------

def test_stabilizer_bell_support():
    st = _run(StabilizerEngine(2), _bell())
    counts = st.sample(4000)
    assert set(counts) <= {"00", "11"}
    assert "00" in counts and "11" in counts


def test_stabilizer_bitstring_order():
    st = _run(StabilizerEngine(2), [("x", (1,), ())])
    assert st.sample(100) == {"10": 100}


def test_stabilizer_ghz():
    # GHZ: H(0), CX(0,1), CX(0,2) -> |000>+|111>
    gates = [("h", (0,), ()), ("cx", (0, 1), ()), ("cx", (0, 2), ())]
    st = _run(StabilizerEngine(3), gates)
    counts = st.sample(2000)
    assert set(counts) <= {"000", "111"}
    assert "000" in counts and "111" in counts


def test_stabilizer_rejects_nonclifford():
    st = StabilizerEngine(2)
    with pytest.raises(ValueError):
        st.apply("rz", [0], (0.3,))


# ---------------------------------------------------------------------------
# MPS
# ---------------------------------------------------------------------------

def test_mps_bell():
    mps = _run(MPSEngine(2), _bell())
    probs = _mps_sv(mps)
    assert probs[0] == pytest.approx(0.5)
    assert probs[3] == pytest.approx(0.5)


def test_mps_ghz():
    gates = [("h", (0,), ()), ("cx", (0, 1), ()), ("cx", (0, 2), ())]
    mps = _run(MPSEngine(3), gates)
    probs = _mps_sv(mps)
    assert probs[0] == pytest.approx(0.5)
    assert probs[7] == pytest.approx(0.5)


def test_mps_nonlocal_cx():
    # 非相邻 CNOT 需 SWAP 链搬移
    mps = _run(MPSEngine(3), [("h", (0,), ()), ("cx", (0, 2), ())])
    probs = _mps_sv(mps)
    assert probs[0] == pytest.approx(0.5)
    assert probs[5] == pytest.approx(0.5)  # |101>: q0=1,q1=0,q2=1


def test_mps_adjacent_swap():
    mps = _run(MPSEngine(2), [("x", (0,), ()), ("swap", (0, 1), ())])
    probs = _mps_sv(mps)
    assert probs[2] == pytest.approx(1.0)


def test_stabilizer_swap():
    st = _run(StabilizerEngine(2), [("x", (0,), ()), ("swap", (0, 1), ())])
    assert st.sample(100) == {"10": 100}


# ---------------------------------------------------------------------------
# density matrix + noise
# ---------------------------------------------------------------------------

def test_density_bell_noiseless():
    dm = _run(DensityMatrixEngine(2), _bell())
    p = np.real(np.diag(dm.rho))
    p = p / p.sum()
    assert p[0] == pytest.approx(0.5)
    assert p[3] == pytest.approx(0.5)


def test_density_depolarizing_leakage():
    from quonic.noise import depolarizing

    dm = DensityMatrixEngine(2, noise=depolarizing(0.1))
    _run(dm, _bell())
    p = np.real(np.diag(dm.rho))
    p = p / p.sum()
    # 去极化使 |01>/|10> 出现
    assert p[1] + p[2] > 0.01


# ---------------------------------------------------------------------------
# native 后端
# ---------------------------------------------------------------------------

def test_native_backend_bell():
    from quonic.backends import get_backend

    be = get_backend("native")

    c = Circuit()
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))
    counts = be.run(c, shots=2000).counts
    assert set(counts) <= {"00", "11"}
    assert "00" in counts and "11" in counts


def test_native_backend_noise_uses_density():
    from quonic.backends import get_backend

    c = Circuit()
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))
    counts = get_backend("native").run(c, shots=2000, noise=0.1).counts
    total = sum(counts.values())
    leakage = counts.get("01", 0) + counts.get("10", 0)
    assert leakage / total > 0.01


def test_native_backend_methods_declared():
    from quonic.backends import get_backend

    native = get_backend("native")
    for m in ("statevector", "stabilizer", "matrix_product_state", "density_matrix"):
        assert native.supports(m)


# ---------------------------------------------------------------------------
# 能力声明 + 调度降级
# ---------------------------------------------------------------------------

def test_backend_supports():
    from quonic.backends import get_backend

    assert get_backend("qiskit").supports("stabilizer")
    assert get_backend("cirq").supports("statevector")
    assert not get_backend("cirq").supports("stabilizer")
    assert not get_backend("pennylane").supports("matrix_product_state")


def test_get_backend_for_method_fallback():
    from quonic.backends import get_backend_for_method

    # cirq 只支持 statevector，请求 stabilizer 应降级到 native
    be = get_backend_for_method("cirq", "stabilizer")
    assert be.name == "native"
    # qiskit 支持 stabilizer，不降级
    assert get_backend_for_method("qiskit", "stabilizer").name == "qiskit"
    # statevector 原样返回
    assert get_backend_for_method("cirq", "statevector").name == "cirq"


def test_native_is_always_available():
    from quonic.backends import available_backends, get_backend

    assert "native" in available_backends()
    assert get_backend("native").name == "native"
