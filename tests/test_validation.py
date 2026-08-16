"""非法参数边缘测试：确认各公开 API 对坏输入抛出清晰的中文异常。

覆盖：qgate / 参数化门 / QInt / CouplingMap / noise / 算法模板 /
后端注册表 / qshow，确保非法参数在进入计算前被拦截，而非静默出错。
"""

import pytest

from quonic import (
    CouplingMap,
    NoiseModel,
    QInt,
    depolarizing,
    qgate,
    qshow,
    reset,
)
from quonic.algorithms import mark_state, oracle
from quonic.algorithms.shor import shor
from quonic.backends import get_backend
from quonic.gates import H, Rx
from quonic.noise import resolve_noise

# ---------------------------------------------------------------------------
# qgate / 门解析
# ---------------------------------------------------------------------------

def test_qgate_wrong_qubit_count():
    reset()
    with pytest.raises(ValueError, match="requires"):
        qgate(H, 0, 1)  # H 是单比特门，给了 2 个


def test_qgate_unknown_gate_name():
    reset()
    with pytest.raises(ValueError, match="Unknown gate"):
        qgate("toffoli-x")


def test_qgate_non_gate_first_arg():
    reset()
    with pytest.raises(TypeError, match="Gate object"):
        qgate(123, 0)


def test_parameterized_gate_non_numeric_angle():
    with pytest.raises(TypeError, match="radians"):
        Rx("not-a-number")


# ---------------------------------------------------------------------------
# QInt 量子整数
# ---------------------------------------------------------------------------

def test_qint_zero_bits():
    reset()
    with pytest.raises(ValueError, match="positive integer"):
        QInt(0)


def test_qint_negative_bits():
    reset()
    with pytest.raises(ValueError, match="positive integer"):
        QInt(-1)


def test_qint_value_out_of_range():
    reset()
    with pytest.raises(ValueError, match="out of range"):
        QInt(2, value=5)  # 2 位整数范围 [0, 4)
    reset()


def test_qint_int_conversion_rejected():
    reset()
    x = QInt(2, value=1)
    with pytest.raises(TypeError, match="superposition"):
        int(x)
    reset()


# ---------------------------------------------------------------------------
# CouplingMap 耦合图
# ---------------------------------------------------------------------------

def test_coupling_map_negative_n():
    with pytest.raises(ValueError, match="non-negative"):
        CouplingMap(-1)


def test_coupling_map_self_loop():
    with pytest.raises(ValueError, match="self-loop"):
        CouplingMap(3, [(0, 0)])


def test_coupling_map_out_of_range_edge():
    with pytest.raises(ValueError, match="out of qubit range"):
        CouplingMap(2, [(0, 3)])


# ---------------------------------------------------------------------------
# 噪声模型
# ---------------------------------------------------------------------------

def test_noise_single_above_one():
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        NoiseModel(single=1.5)


def test_noise_double_negative():
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        NoiseModel(double=-0.1)


def test_depolarizing_out_of_range():
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        depolarizing(1.5)


def test_resolve_noise_bad_type():
    with pytest.raises(TypeError, match="NoiseModel"):
        resolve_noise("high")


# ---------------------------------------------------------------------------
# 算法模板
# ---------------------------------------------------------------------------

def test_mark_state_non_binary():
    with pytest.raises(ValueError, match="0/1"):
        mark_state("12")


def test_mark_state_empty():
    with pytest.raises(ValueError, match="0/1"):
        mark_state("")


def test_oracle_zero_qubits():
    with pytest.raises(ValueError, match="positive integer"):
        oracle(0)


def test_shor_n_too_small():
    with pytest.raises(ValueError, match=">= 2"):
        shor(1)


# ---------------------------------------------------------------------------
# 后端注册表 / qshow
# ---------------------------------------------------------------------------

def test_get_backend_unknown_name():
    with pytest.raises(ValueError, match="Unknown backend"):
        get_backend("not-a-backend")


def test_qshow_rejects_non_result():
    reset()
    with pytest.raises(TypeError, match="Result"):
        qshow(result="not a Result")
