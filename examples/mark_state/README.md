# mark_state 标记态神谕

mark_state("10") 生成标记 |10>（qubit0=0, qubit1=1）的神谕回调，Grover 搜索放大它。

mark_state("10") builds an oracle callback marking |10> (qubit 0 = 0, qubit 1 = 1); Grover search amplifies it.

## 运行 Run

```bash
python examples/mark_state/mark_state.py
```

## 预期输出 Expected output

计数直方图几乎全部集中在 |10>。

The counts are almost entirely on |10>.
