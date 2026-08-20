"""Steane Code / Steane 码

[[7,1,3]] CSS code, corrects arbitrary single-qubit errors.
[[7,1,3]] CSS 码，纠正任意单比特错误。

## Application / 应用场景
- Quantum error correction (量子纠错)
- Fault tolerance (容错)
- Logical gates (逻辑门)

## Output / 输出
Corrected logical qubit.
纠正后的逻辑比特。"""

from quonic.algorithms import steane_code

result = steane_code(error_qubit=0, shots=100)
print(result.counts)
