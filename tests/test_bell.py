"""贝尔态冒烟测试：H + CX 应得到约 50/50 的 |00> 和 |11>。"""

from pyqqq import qgate, qshow
from pyqqq.gates import H, CX


def test_bell_state(capsys):
    qgate(H, 0)
    qgate(CX, 0, 1)
    result = qshow(shots=1024)
    capsys.readouterr()  # 吞掉 qshow 的打印

    counts = result["counts"]
    assert set(counts) <= {"00", "11"}, f"贝尔态不应出现其他比特串：{counts}"
    total = sum(counts.values())
    assert "00" in counts and "11" in counts
    assert 0.4 < counts["00"] / total < 0.6
    assert 0.4 < counts["11"] / total < 0.6
