"""pytest 全局 fixture：每个测试前后重置全局电路栈，消除跨测试状态污染。

qgate() / qshow() 依赖全局电路栈（stack.py），测试按字母序执行时，
前一个测试残留的电路会污染后一个测试。这里统一在测试前后 reset()。
"""

import pytest

from quonic import reset


@pytest.fixture(autouse=True)
def _reset_global_circuit():
    reset()
    yield
    reset()
