"""Quantum Inspire 真实硬件后端（qi）测试。

真实硬件无法离线端到端运行（需 token + 网络 + 降级 qiskit），故这里的
测试覆盖「无需依赖即可验证」的部分：注册、参数/动态电路拒绝、缺包时的
清晰报错，以及 QI 十六进制计数 → 比特串的转换。
"""

import pytest

from quonic import cif, creg, cwhile, qgate, reset
from quonic.backends import available_backends, get_backend, resolve_target
from quonic.backends.qi import _hex_to_bitstring, resolve_device
from quonic.gates import H, I, X
from quonic.stack import current_circuit


def _run(shots=64, **kwargs):
    return get_backend("qi").run(current_circuit(), shots=shots, **kwargs)


# ---------------------------------------------------------------------------
# 注册
# ---------------------------------------------------------------------------

def test_qi_registered():
    assert get_backend("qi").name == "qi"
    assert "qi" in available_backends()


def test_qi_supports_any_method_no_fallback():
    # 硬件后端不参与 method 能力匹配，任何 method 都直接跑硬件而非降级 native
    be = get_backend("qi")
    assert be.supports("statevector")
    assert be.supports("stabilizer")


# ---------------------------------------------------------------------------
# 设备捷径映射（tuna9 / tuna17 / qx）
# ---------------------------------------------------------------------------

def test_device_shortcuts_resolve_to_qi():
    # 旧设备捷径仍兼容：backend="tuna9" 等价于 backend="qi", device="tuna9"
    assert resolve_target("tuna9") == ("qi", "tuna9")
    assert resolve_target("tuna17") == ("qi", "tuna17")
    assert resolve_target("qx") == ("qi", "qx")
    assert resolve_target("qi", "tuna9") == ("qi", "tuna9")
    assert resolve_target("qiskit") == ("qiskit", None)
    assert resolve_target("auto") == ("auto", None)


def test_device_only_valid_for_qi():
    # device 只对 qi 有效，其余引擎传 device 报中文错
    with pytest.raises(ValueError, match="backend='qi'"):
        resolve_target("qiskit", "tuna9")


def test_resolve_device_aliases():
    assert resolve_device("tuna9") == "Tuna-9"
    assert resolve_device("tuna17") == "Tuna-17"
    assert resolve_device("qx") == "QX emulator"
    assert resolve_device("Tuna-9") == "Tuna-9"  # 正式名透传
    assert resolve_device(None) is None


def test_device_shortcut_backend_device():
    assert get_backend("tuna9").device == "Tuna-9"
    assert get_backend("tuna17").device == "Tuna-17"
    assert get_backend("qx").device == "QX emulator"
    assert get_backend("qi").device is None  # 未指定时 run() 默认走 QX 云模拟器
    assert get_backend("qi", device="tuna9").device == "Tuna-9"


# ---------------------------------------------------------------------------
# 参数 / 动态电路拒绝（发生在延迟导入之前，离线可测）
# ---------------------------------------------------------------------------

def test_qi_rejects_noise():
    reset()
    qgate(X, 0)
    with pytest.raises(ValueError, match="noise"):
        _run(noise=0.1)


def test_qi_rejects_cwhile():
    reset()
    flag = creg("flag")
    with cwhile(flag, until=1):
        qgate(X, 0)
        flag.measure(0)
    with pytest.raises(NotImplementedError, match="cwhile"):
        _run()


def test_qi_rejects_cif():
    reset()
    qgate(X, 0)
    flag = creg("flag")
    flag.measure(0)
    cif(flag).then(X, 1).else_(I, 1)
    with pytest.raises(NotImplementedError, match="cif"):
        _run()


# ---------------------------------------------------------------------------
# 缺包时的清晰报错
# ---------------------------------------------------------------------------

def test_qi_missing_package_raises_import_error():
    try:
        import qiskit_quantuminspire  # noqa: F401

        pytest.skip("qiskit-quantuminspire 已安装，跳过缺包路径测试")
    except ImportError:
        pass
    reset()
    qgate(H, 0)
    with pytest.raises(ImportError, match="qiskit-quantuminspire"):
        _run()


# ---------------------------------------------------------------------------
# 计数转换
# ---------------------------------------------------------------------------

def test_hex_to_bitstring():
    assert _hex_to_bitstring("0x3", 2) == "11"
    assert _hex_to_bitstring("0x0", 3) == "000"
    assert _hex_to_bitstring("0x5", 3) == "101"
    assert _hex_to_bitstring("0xf", 4) == "1111"
