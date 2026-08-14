"""三后端一致性测试：同一段代码在 Qiskit / Cirq / PennyLane 上输出一致。"""

import pytest

from pyqqq import qgate, qshow
from pyqqq.gates import H, CX, X


@pytest.mark.parametrize("backend", ["qiskit", "cirq", "pennylane"])
def test_bell_state_consistent(backend, capsys):
    qgate(H, 0)
    qgate(CX, 0, 1)
    result = qshow(backend=backend, shots=1024)
    capsys.readouterr()

    counts = result["counts"]
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

    counts = result["counts"]
    assert set(counts) == {"10"}, f"{backend}: {counts}"
