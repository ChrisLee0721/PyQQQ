"""QInt 量子整数寄存器测试。"""

from quonic import QInt, qshow


def test_qint_load(capsys):
    QInt(3, value=5)
    result = qshow(shots=1024)
    capsys.readouterr()
    assert result.counts == {"101": 1024}


def test_qint_superpose_add(capsys):
    x = QInt(3, value=1)
    x.h()
    x += 3
    result = qshow(shots=1024)
    capsys.readouterr()

    # 均匀叠加再加常数仍是均匀叠加
    total = sum(result.counts.values())
    assert len(result.counts) == 8
    for c in result.counts.values():
        assert 0.08 < c / total < 0.18, f"{result.counts}"


def test_qint_no_overlap(capsys):
    # 两个 QInt 应占据不重叠的量子比特：|3>|1> -> "0111"
    QInt(2, value=3)
    QInt(2, value=1)
    result = qshow(shots=1024)
    capsys.readouterr()
    assert result.counts == {"0111": 1024}


def test_qint_sub(capsys):
    # 5 - 3 = 2 = |010>
    x = QInt(3, value=5)
    x -= 3
    result = qshow(shots=1024)
    capsys.readouterr()
    assert result.counts == {"010": 1024}


def test_qint_add_modulo(capsys):
    # 5 + 3 = 8 ≡ 0 (mod 8) = |000>
    x = QInt(3, value=5)
    x += 3
    result = qshow(shots=1024)
    capsys.readouterr()
    assert result.counts == {"000": 1024}
