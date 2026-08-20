"""Shor's 9-qubit Code / Shor 9 比特码

First quantum error correction code, corrects arbitrary errors.
第一个量子纠错码，纠正任意错误。

## Application / 应用场景
- Quantum error correction (量子纠错)
- Fault tolerance (容错)
- Quantum memory (量子存储)

## Output / 输出
Corrected logical qubit.
纠正后的逻辑比特。"""

from quonic.algorithms import shor_code

result = shor_code(error_qubit=0, shots=100)
print(result.counts)
