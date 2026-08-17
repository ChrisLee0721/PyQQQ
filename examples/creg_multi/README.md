# 多比特经典寄存器 creg(width=2)

`creg(name, width=2)` 生成持 2 比特的经典寄存器，寄存器值为 `0..3`。
`cwhile(reg, until=2)` 循环到寄存器 == 2，`loop.groverize()` 把 retry 循环编译成
静态 Grover 电路（成功概率从 1/4 放大到 1）；`cif(reg, 2)` 按寄存器整值分支。

`creg(name, width=2)` declares a 2-bit classical register holding integer values `0..3`.
`cwhile(reg, until=2)` loops until the register equals 2, and `loop.groverize()` compiles
the retry loop into a static Grover circuit (success probability amplified from 1/4 to 1);
`cif(reg, 2)` branches on the full register value.

## 运行 Run

```bash
python examples/creg_multi/creg_multi.py
```

## 预期输出 Expected output

`{'1010': 1024}`（ancilla 寄存器 "10" + 数据 "10"）和 `{'110': 256}`（q2 被 then 分支翻转）。

`{'1010': 1024}` (ancilla register "10" + data "10") and `{'110': 256}` (q2 flipped by the then branch).

## 注意 Note

`cwhile` 的 `until` 既可是整数寄存器值（`until=2`），也可是 "0/1" 比特串（`until="10"`，MSB 在前）。
多比特 creg v1 完整支持 native + qiskit；cirq / pennylane 的多比特判据暂不支持，会抛清晰的
「暂不支持多比特 creg」错误。

`cwhile`'s `until` accepts either an integer register value (`until=2`) or a "0/1" bitstring
(`until="10"`, MSB first). Multi-bit creg is fully supported on native + qiskit; cirq / pennylane
multi-bit predicates are not yet supported and raise a clear "multi-bit creg unsupported" error.
