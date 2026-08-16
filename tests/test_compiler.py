"""耦合图 + 编译 seam + 门分解测试。"""

import math

import numpy as np
import pytest

from quonic import CouplingMap, RoutingError, decompose
from quonic.compiler import BASIC_GATES, compile
from quonic.ir import Circuit, GateOperation
from quonic.simulators import StatevectorEngine


def _ghz(n):
    c = Circuit()
    c.add(GateOperation("h", (0,)))
    for i in range(n - 1):
        c.add(GateOperation("cx", (i, i + 1)))
    return c


# ---------------------------------------------------------------------------
# CouplingMap
# ---------------------------------------------------------------------------

def test_coupling_map_from_line():
    cm = CouplingMap.from_line(3)
    assert cm.has_edge(0, 1) and cm.has_edge(1, 2)
    assert not cm.has_edge(0, 2)
    assert cm.edges() == [(0, 1), (1, 2)]


def test_coupling_map_from_grid():
    cm = CouplingMap.from_grid(2, 2)
    assert len(cm) == 4
    assert cm.has_edge(0, 1) and cm.has_edge(2, 3)  # 行内
    assert cm.has_edge(0, 2) and cm.has_edge(1, 3)  # 列内
    assert not cm.has_edge(0, 3)


def test_coupling_map_fully_connected():
    cm = CouplingMap.fully_connected(4)
    assert cm.has_edge(0, 3) and cm.has_edge(1, 2)
    assert len(cm.edges()) == 6


def test_coupling_map_rejects_invalid_edge():
    with pytest.raises(ValueError):
        CouplingMap(2, [(0, 0)])  # 自环
    with pytest.raises(ValueError):
        CouplingMap(2, [(0, 2)])  # 越界
    with pytest.raises(ValueError):
        CouplingMap(2, [(-1, 0)])  # 负数


# ---------------------------------------------------------------------------
# compile（连通性校验）
# ---------------------------------------------------------------------------

def test_compile_no_map_copies():
    c = _ghz(2)
    out = compile(c)
    assert out is not c
    assert [op.name for op in out.ops] == ["h", "cx"]


def test_compile_line_topology_ok():
    # GHZ 链天然落在 line 拓扑上
    c = _ghz(3)
    out = compile(c, CouplingMap.from_line(3))
    assert out.gate_count() == c.gate_count()


def test_compile_line_topology_violates():
    c = Circuit()
    c.add(GateOperation("cx", (0, 2)))
    with pytest.raises(RoutingError):
        compile(c, CouplingMap.from_line(3))


def test_compile_multiqubit_requires_clique():
    # ccx 三比特门要求 0-1、0-2、1-2 都相连；line(3) 缺 0-2
    c = Circuit()
    c.add(GateOperation("ccx", (0, 1, 2)))
    with pytest.raises(RoutingError):
        compile(c, CouplingMap.from_line(3))
    # 全连接则通过
    out = compile(c, CouplingMap.fully_connected(3))
    assert out.gate_count() == 1


def test_compile_ignores_measure():
    c = Circuit()
    c.add(GateOperation("cx", (0, 1)))
    c.add(GateOperation("measure", (0,)))
    out = compile(c, CouplingMap.from_line(2))
    assert [op.name for op in out.ops] == ["cx", "measure"]


# ---------------------------------------------------------------------------
# decompose：用自研 statevector 引擎对拍验证分解正确性
# ---------------------------------------------------------------------------

def _statevector(circuit):
    eng = StatevectorEngine(circuit.num_qubits)
    for op in circuit.ops:
        eng.apply(op.name, list(op.qubits), op.params)
    return eng.state


def _assert_equiv(orig, dec):
    """断言 decompose 后的电路与原电路等价（含 ancilla 全部回到 |0>）。"""
    a = _statevector(orig)
    b = _statevector(dec)
    n = orig.num_qubits
    if dec.num_qubits > n:
        # 分解引入的 ancilla 必须为 |0>：高位（ancilla）全为 0
        assert np.allclose(b[2 ** n:], 0.0, atol=1e-9)
        b = b[: 2 ** n]
    # 全局相位无关比较：|⟨a|b⟩| == 1
    assert abs(np.vdot(a, b)) > 1 - 1e-8


def test_decompose_cp_matches():
    for theta in (0.3, 1.1, math.pi):
        c = Circuit()
        c.add(GateOperation("h", (0,)))
        c.add(GateOperation("h", (1,)))
        c.add(GateOperation("cp", (0, 1), (theta,)))
        _assert_equiv(c, decompose(c))


def test_decompose_ccx_matches():
    c = Circuit()
    for q in range(3):
        c.add(GateOperation("h", (q,)))
    c.add(GateOperation("ccx", (0, 1, 2)))
    _assert_equiv(c, decompose(c))


def test_decompose_mcz_matches():
    # 1..4 个控制（总 2..5 比特），覆盖 cz / H·ccx·H / AND 级联（含 ancilla）
    for k in range(1, 5):
        n = k + 1
        c = Circuit()
        for q in range(n):
            c.add(GateOperation("h", (q,)))
        c.add(GateOperation("mcz", tuple(range(n))))
        _assert_equiv(c, decompose(c))


def test_decompose_mcz_ancilla_count():
    # mcz(0,1,2,3)：3 控制 -> 1 个 ancilla
    c = Circuit()
    c.add(GateOperation("mcz", (0, 1, 2, 3)))
    out = decompose(c)
    assert out.num_qubits == 5


def test_decompose_mcz_ancilla_recycled():
    # 两个各需 1 个 ancilla 的 mcz，复用同一组，总 ancilla 仍为 1（不累加）
    c = Circuit()
    c.add(GateOperation("mcz", (0, 1, 2, 3)))
    c.add(GateOperation("mcz", (0, 1, 2, 3)))
    out = decompose(c)
    assert out.num_qubits == 5


def test_decompose_mcz_recycled_equiv():
    # 复用 ancilla 后，多 mcz 电路仍与原始电路等价
    c = Circuit()
    for q in range(4):
        c.add(GateOperation("h", (q,)))
    c.add(GateOperation("mcz", (0, 1, 2, 3)))
    c.add(GateOperation("mcz", (0, 1, 2, 3)))
    _assert_equiv(c, decompose(c))


def test_decompose_output_is_basic():
    c = Circuit()
    c.add(GateOperation("ccx", (0, 1, 2)))
    c.add(GateOperation("cp", (0, 1), (0.5,)))
    c.add(GateOperation("mcz", (0, 1, 2, 3)))
    out = decompose(c)
    assert out.ops
    for op in out.ops:
        assert op.name in BASIC_GATES
