"""贝尔态冒烟测试：H + CX 应得到约 50/50 的 |00> 和 |11>。"""

from quonic import CouplingMap, qgate, qshow
from quonic.gates import CX, H


def test_bell_state(capsys):
    qgate(H, 0)
    qgate(CX, 0, 1)
    result = qshow(shots=1024)
    capsys.readouterr()  # 吞掉 qshow 的打印

    counts = result.counts
    assert set(counts) <= {"00", "11"}, f"贝尔态不应出现其他比特串：{counts}"
    total = sum(counts.values())
    assert "00" in counts and "11" in counts
    assert 0.4 < counts["00"] / total < 0.6
    assert 0.4 < counts["11"] / total < 0.6


def test_coupling_map_routing(capsys):
    # GHZ(3) 含非相邻的 CX(0,2)，在一维链上需 SWAP 路由，结果仍是 |000>+|111>
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(CX, 0, 2)
    result = qshow(coupling_map=CouplingMap.from_line(3), backend="native", shots=1024)
    capsys.readouterr()

    counts = result.counts
    assert set(counts) <= {"000", "111"}, f"路由后不应出现其他比特串：{counts}"
    assert "000" in counts and "111" in counts
