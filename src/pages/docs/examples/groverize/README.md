# cwhile → groverize 振幅放大编译

`cwhile(flag, until=0)` 是 repeat-until-success（RUS）动态循环，逐 shot 反馈重试，
只有 native 后端能跑。`with cwhile(...) as loop:` 拿到循环对象后 `loop.groverize()`
把它**编译成静态 Grover 电路**：延迟测量（`cmeasure` → `CX(q, ancilla)`）+ 振幅放大，
把单次成功概率 p 从 1/4 放大到 ~1，变成固定深度、无中段反馈的电路，任何后端
（含真机）都能跑。对纯酉循环体，`success_prob` 会自动推断，无需手算 p。

`cwhile(flag, until=0)` is a repeat-until-success dynamic loop that retries shot-by-shot,
runnable only on the native backend. Capturing the loop object with `with cwhile(...) as
loop:` and calling `loop.groverize()` compiles it into a static Grover circuit — deferred
measurement (`cmeasure` → `CX(q, ancilla)`) plus amplitude amplification, lifting the
single-shot success probability p from 1/4 to ~1, yielding a fixed-depth, feedback-free
circuit runnable on any backend (including real hardware). For a purely unitary body,
`success_prob` is inferred automatically — no manual p.

## 运行 Run

```bash
python examples/groverize/groverize.py
```

## 预期输出 Expected output

`{'00': 1024}`：Ry(2π/3) 后测 q0 成功（q0 == 0）的概率是 p = 1/4，Grover 化后集中到
`|00>`，1024 shot 全部命中成功态。

`{'00': 1024}`: after Ry(2π/3), measuring q0 succeeds (q0 == 0) with p = 1/4; after
Grover-ization the counts collapse onto `|00>`, all 1024 shots hitting the success state.

## 注意 Note

`groverize` 的前提：循环体必须纯酉，且以单个 `flag.measure(q)` 结尾（成功判据）。
不满足会抛错并引导回 native 的逐 shot `cwhile`。对纯酉循环体，`success_prob` 由
模拟自动推断；若需覆盖，也可显式传入 `loop.groverize(success_prob=0.25)`。

`groverize`'s precondition: the loop body must be purely unitary and end with a single
`flag.measure(q)` (the success criterion). Violating it raises an error that guides you
back to native shot-by-shot `cwhile`. For a purely unitary body, `success_prob` is
inferred by simulation; override it explicitly via `loop.groverize(success_prob=0.25)`.
