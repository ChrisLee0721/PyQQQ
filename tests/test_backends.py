"""三后端一致性测试：同一段代码在 Qiskit / Cirq / PennyLane 上输出一致。"""

import pytest

from quonic import qgate, qshow
from quonic.gates import CX, H, X


@pytest.mark.parametrize("backend", ["qiskit", "cirq", "pennylane"])
def test_bell_state_consistent(backend, capsys):
    qgate(H, 0)
    qgate(CX, 0, 1)
    result = qshow(backend=backend, shots=1024)
    capsys.readouterr()

    counts = result.counts
    assert set(counts) <= {"00", "11"}, f"{backend}: {counts}"
    total = sum(counts.values())
    assert "00" in counts and "11" in counts
    assert 0.4 < counts["00"] / total < 0.6, f"{backend}: {counts}"
    assert 0.4 < counts["11"] / total < 0.6, f"{backend}: {counts}"


@pytest.mark.parametrize("backend", ["qiskit", "cirq", "pennylane"])
def test_bitstring_order_consistent(backend, capsys):
    # X 作用在 qubit 1：qubit0=0, qubit1=1 -> 按统一约定应是 "10"
    qgate(X, 1)
    result = qshow(backend=backend, shots=100)
    capsys.readouterr()

    counts = result.counts
    assert set(counts) == {"10"}, f"{backend}: {counts}"


@pytest.mark.parametrize("backend", ["qiskit", "cirq", "pennylane"])
def test_depolarizing_noise(backend):
    from quonic.backends import get_backend
    from quonic.ir import Circuit, GateOperation

    c = Circuit()
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))

    be = get_backend(backend)
    noisy = be.run(c, shots=2000, noise=0.1)
    counts = noisy.counts
    total = sum(counts.values())
    leakage = counts.get("01", 0) + counts.get("10", 0)
    # 去极化噪声应使 |01>/|10> 出现（无噪声贝尔态只有 |00>/|11>）
    assert leakage / total > 0.01, f"{backend}: {counts}"
    # 但主分量仍是 |00>/|11>
    main = counts.get("00", 0) + counts.get("11", 0)
    assert main / total > 0.8, f"{backend}: {counts}"


def test_noise_model_validation():
    from quonic import NoiseModel, depolarizing
    from quonic.noise import resolve_noise

    assert depolarizing(0.05).single == 0.05
    assert depolarizing(0.05).double == 0.05
    assert resolve_noise(None).enabled is False
    assert resolve_noise(0.1).enabled is True
    with pytest.raises(ValueError):
        NoiseModel(single=1.5)
    with pytest.raises(TypeError):
        resolve_noise("high")


def test_backend_auto(capsys):
    # auto 应按优先级探测，返回一个已注册后端
    from quonic.backends import get_backend

    name = get_backend("auto").name
    assert name in ("qiskit", "cirq", "pennylane"), f"auto -> {name}"


def test_qshow_report(capsys):
    qgate(H, 0)
    qgate(CX, 0, 1)
    qshow(backend="qiskit", shots=10, report=True)
    out = capsys.readouterr().out
    assert "电路资源" in out
    assert "门数" in out and "深度" in out and "量子比特" in out


@pytest.mark.parametrize("backend", ["qiskit", "cirq", "pennylane"])
def test_qft_cp_consistent(backend, capsys):
    # QFT 走原生 cp 门：QInt 加法 |1> + 3 = |4> 在三个后端一致
    from quonic import QInt, reset

    reset()
    x = QInt(3, value=1)
    x += 3
    result = qshow(backend=backend, shots=256)
    capsys.readouterr()
    assert result.counts == {"100": 256}, f"{backend}: {result.counts}"
