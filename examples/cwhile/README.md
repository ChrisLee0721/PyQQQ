# creg + cwhile 测量反馈循环

`creg(name)` 声明一个具名经典寄存器，`flag.measure(0)` 把 qubit 0 的测量结果
存进去；`cwhile(flag, until=0)` 反复执行循环体，直到 `flag == 0` 才退出。这是
repeat-until-success（RUS）动态电路的核心原语。

`creg(name)` declares a named classical register; `flag.measure(0)` stores the
measurement of qubit 0 into it; `cwhile(flag, until=0)` repeats the body until
`flag == 0`. This is the core primitive for repeat-until-success dynamic circuits.

## 运行 Run

```bash
python examples/cwhile/cwhile.py
```

## 预期输出 Expected output

几乎确定测到 `|0>`：每次 H+measure 有 50% 概率测到 0，循环直到测到 0 才退出，
所以退出时 qubit 0 必然已坍缩到 `|0>`。迭代次数随机，结果确定。

Almost surely `|0>`: each H+measure yields 0 with 50% probability, and the loop
exits only once it sees 0, so qubit 0 is guaranteed to have collapsed to `|0>`.
The iteration count is random; the outcome is deterministic.

## 注意 Note

经典反馈循环（cwhile）逐 shot 动态执行，只有 native 后端支持；qiskit / cirq /
pennylane 后端会抛 `NotImplementedError`。
