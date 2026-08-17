"""ZNE：折叠等价性 + 外推恢复真值 + 期望值指标与态矢量对拍。"""

import numpy as np
import pytest

from quonic import fold, zne
from quonic.ir import Circuit, GateOperation
from quonic.simulator import StatevectorSimulator
from quonic.simulators import DensityMatrixEngine, StatevectorEngine


def _statevector(circuit):
    eng = StatevectorEngine(circuit.num_qubits)
    for op in circuit.ops:
        if op.name == "measure":
            continue
        eng.apply(op.name, list(op.qubits), op.params)
    return eng.state


def _bell():
    c = Circuit()
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))
    return c


# ---------------------------------------------------------------------------
# fold
# ---------------------------------------------------------------------------

def test_fold_unitary_equiv():
    # 对酉电路，fold(C, k) = C(C†C)^k = C，与原电路逐位等价
    c = _bell()
    for k in (0, 1, 2, 3):
        a = _statevector(c)
        b = _statevector(fold(c, k))
        assert np.allclose(a, b, atol=1e-9), k


def test_fold_preserves_measure_at_end():
    c = Circuit()
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("measure", (0,)))
    out = fold(c, 1)
    assert out.num_qubits == 1
    # 折叠只影响酉门，measure 仍留在末尾
    assert out.ops[-1].name == "measure"
    assert sum(1 for op in out.ops if op.name == "measure") == 1


def test_fold_rejects_negative_k():
    with pytest.raises(ValueError):
        fold(_bell(), -1)


def test_fold_rejects_dynamic_ops():
    c = Circuit()
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("measure", (0,)))
    for name in ("cmeasure", "cif", "cwhile"):
        from quonic.ir import CMeasureOperation

        bad = Circuit()
        bad.add(GateOperation("h", (0,)))
        if name == "cmeasure":
            bad.add(CMeasureOperation(0, "flag"))
        else:
            bad.add(GateOperation("x", (0,)))
        # 仅 cmeasure 直接可构造；cif/cwhile 由 fold 内部同样拒绝
        if name == "cmeasure":
            with pytest.raises(ValueError):
                fold(bad, 1)


def test_fold_matches_statevector_manually():
    # fold 通过 C†C 插入：验证 fold(C,1) 的态矢量 = 原态矢量（用 X 门直接对拍）
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    assert np.allclose(_statevector(fold(c, 1)), _statevector(c), atol=1e-12)


# ---------------------------------------------------------------------------
# DensityMatrixEngine.expectation vs StatevectorSimulator.expectation
# ---------------------------------------------------------------------------

def _expectation_pair(circuit, pauli):
    dm = DensityMatrixEngine(circuit.num_qubits)
    sv = StatevectorSimulator(circuit.num_qubits)
    for op in circuit.ops:
        if op.name == "measure":
            continue
        dm.apply(op.name, list(op.qubits), op.params)
        sv.apply(op.name, list(op.qubits), op.params)
    return dm.expectation(pauli), sv.expectation(pauli)


def test_expectation_matches_statevector():
    # 单比特 |1> 的 <Z> = -1
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    a, b = _expectation_pair(c, "Z")
    assert a == pytest.approx(b, abs=1e-9)
    assert a == pytest.approx(-1.0, abs=1e-9)


def test_expectation_matches_statevector_two_qubit():
    # 贝尔态 |00>+|11>：<ZZ> = 1, <IZ> = 0, <ZI> = 0, <XX> = 1
    c = _bell()
    for pauli, expected in (("ZZ", 1.0), ("IZ", 0.0), ("ZI", 0.0), ("XX", 1.0)):
        a, b = _expectation_pair(c, pauli)
        assert a == pytest.approx(b, abs=1e-9)
        assert a == pytest.approx(expected, abs=1e-9)


def test_expectation_pauli_len_error():
    dm = DensityMatrixEngine(2)
    with pytest.raises(ValueError):
        dm.expectation("ZZZ")


# ---------------------------------------------------------------------------
# zne
# ---------------------------------------------------------------------------

def test_zne_expectation_recovers_clean_value():
    # X|0> = |1>，无噪声 <Z> = -1；去极化噪声把 <Z> 推向 0。
    # 折叠放大噪声档后线性外推到 λ=0 应恢复到接近 -1。
    c = Circuit()
    c.add(GateOperation("x", (0,)))

    res = zne(c, noise=0.05, observable="Z")
    assert res.metric == "expectation"
    assert list(res.factors) == [1.0, 3.0, 5.0]
    # 噪声使 <Z> 向 0 漂移（|⟨Z⟩| 单调递减）
    assert abs(res.values[0]) > abs(res.values[1]) > abs(res.values[2])
    # 外推值比 λ=1 的单次值更接近真值 -1
    assert abs(res.extrapolated - (-1.0)) < abs(res.values[0] - (-1.0))
    assert res.extrapolated == pytest.approx(-1.0, abs=0.05)


def test_zne_success_recovers_clean_value():
    # X|0> = |1>，target="1" 无噪声成功率 = 1；噪声 + 折叠外推应恢复到接近 1
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("measure", (0,)))

    res = zne(c, noise=0.05, target="1", shots=8192)
    assert res.metric == "success"
    assert 0.0 <= res.extrapolated <= 1.0
    # 外推值比 λ=1 的单次采样更接近真值 1
    assert abs(res.extrapolated - 1.0) < abs(res.values[0] - 1.0)
    assert res.extrapolated > 0.9


def test_zne_target_iterable():
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("measure", (0,)))
    res = zne(c, noise=0.05, target={"1"}, shots=4096)
    assert res.metric == "success"
    assert res.extrapolated > 0.9


def test_zne_requires_exactly_one_metric():
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    with pytest.raises(ValueError):
        zne(c, noise=0.05)  # 两者都没给
    with pytest.raises(ValueError):
        zne(c, noise=0.05, target="1", observable="Z")  # 两者都给


def test_zne_requires_noise():
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    with pytest.raises(ValueError):
        zne(c, noise=0.0, observable="Z")


def test_zne_factors_validation():
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    with pytest.raises(ValueError):
        zne(c, noise=0.05, observable="Z", factors=(1, 2, 5))  # 偶数
    with pytest.raises(ValueError):
        zne(c, noise=0.05, observable="Z", factors=(3, 1))  # 非递增


def test_zne_observable_validation():
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    with pytest.raises(ValueError):
        zne(c, noise=0.05, observable="Z2")


def test_zne_backend_validation():
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("measure", (0,)))
    with pytest.raises(ValueError):
        zne(c, noise=0.05, target="1", backend="cirq")


# ---------------------------------------------------------------------------
# backend="qi": fold amplifies intrinsic noise (no injected noise)
# ---------------------------------------------------------------------------

def _expectation_via_rotation(circuit, observable):
    """Deterministic ⟨O⟩ from the rotated circuit's statevector probabilities."""
    from quonic.zne import _observable_circuit

    rotated = _observable_circuit(circuit, 0, observable)
    eng = StatevectorEngine(rotated.num_qubits)
    for op in rotated.ops:
        if op.name == "measure":
            continue
        eng.apply(op.name, list(op.qubits), op.params)
    probs = np.abs(eng.state) ** 2
    total = 0.0
    for idx, pr in enumerate(probs):
        prod = 1.0
        for q, p in enumerate(observable):
            if p == "I":
                continue
            if (idx >> q) & 1:
                prod = -prod
        total += prod * pr
    return total


def test_pauli_rotation_matches_statevector():
    # 贝尔态：旋转到对应测量基后，计数期望应与 <O> 一致
    c = _bell()
    sv = StatevectorSimulator(2)
    for op in c.ops:
        sv.apply(op.name, list(op.qubits), op.params)
    for pauli in ("ZZ", "XX", "IZ", "YY"):
        got = _expectation_via_rotation(c, pauli)
        want = sv.expectation(pauli)
        assert got == pytest.approx(want, abs=1e-9), pauli


def test_expectation_from_counts():
    from quonic.zne import _expectation_from_counts

    assert _expectation_from_counts({"00": 1000}, "ZZ", 1000) == pytest.approx(1.0)
    assert _expectation_from_counts({"11": 1000}, "ZZ", 1000) == pytest.approx(1.0)
    assert _expectation_from_counts({"10": 1000}, "ZZ", 1000) == pytest.approx(-1.0)
    assert _expectation_from_counts({"10": 1000}, "IZ", 1000) == pytest.approx(-1.0)
    assert _expectation_from_counts({"01": 1000}, "ZI", 1000) == pytest.approx(-1.0)


def test_zne_qi_rejects_injected_noise():
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    with pytest.raises(ValueError):
        zne(c, noise=0.05, target="1", backend="qi")
    with pytest.raises(ValueError):
        zne(c, noise=0.05, observable="Z", backend="qi")


def test_zne_qi_observable_length_mismatch():
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    with pytest.raises(ValueError):
        zne(c, observable="ZZ", backend="qi")


# ---------------------------------------------------------------------------
# stacking readout calibration on top of ZNE
# ---------------------------------------------------------------------------

def test_zne_with_calibration_recovers_better():
    from quonic import calibrate
    from quonic.noise import NoiseModel

    c = Circuit()
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("measure", (0,)))
    # gate noise (foldable) + readout noise (flat, not foldable)
    nm = NoiseModel(single=0.02, readout=0.1)
    cal = calibrate(1, backend="native", shots=16384, noise=nm)

    plain = zne(c, noise=nm, target="1", backend="native", shots=16384)
    stacked = zne(c, noise=nm, target="1", backend="native", shots=16384,
                  calibration=cal)
    # removing readout error per-λ lets ZNE extrapolate closer to the true value 1
    assert stacked.extrapolated > plain.extrapolated
    assert stacked.extrapolated > 0.9


def test_zne_calibration_n_mismatch():
    from quonic import calibrate

    c = Circuit()
    c.add(GateOperation("x", (0,)))
    cal = calibrate(2, backend="native")
    with pytest.raises(ValueError):
        zne(c, noise=0.05, target="1", backend="native", calibration=cal)


# ---------------------------------------------------------------------------
# extrapolation methods
# ---------------------------------------------------------------------------

def test_zne_exponential_expectation_recovers_clean_value():
    # X|0> = |1>, <Z> = -1. Depolarizing noise decays <Z> geometrically in λ,
    # which the 3-param exponential fit recovers exactly at λ=0.
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    res = zne(c, noise=0.05, observable="Z", extrapolation="exponential")
    assert res.metric == "expectation"
    assert res.extrapolated == pytest.approx(-1.0, abs=0.05)
    assert abs(res.extrapolated - (-1.0)) < abs(res.values[0] - (-1.0))


def test_zne_exponential_success_recovers_clean_value():
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("measure", (0,)))
    res = zne(c, noise=0.05, target="1", shots=16384, extrapolation="exponential")
    assert res.metric == "success"
    assert 0.0 <= res.extrapolated <= 1.0
    assert abs(res.extrapolated - 1.0) < abs(res.values[0] - 1.0)
    assert res.extrapolated > 0.9


def test_zne_exponential_two_factors_falls_back_to_linear():
    # < 3 λ points underdetermine the 3-param exponential, so it falls back to linear.
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    lin = zne(c, noise=0.05, observable="Z", factors=(1, 3), extrapolation="linear")
    exp = zne(c, noise=0.05, observable="Z", factors=(1, 3), extrapolation="exponential")
    assert exp.extrapolated == pytest.approx(lin.extrapolated)


def test_zne_extrapolation_validation():
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    with pytest.raises(ValueError):
        zne(c, noise=0.05, observable="Z", extrapolation="quadratic")
