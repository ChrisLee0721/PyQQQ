"""Correct bit-flip errors / 纠正比特翻转错误

3-qubit code corrects single bit-flip errors.
3 比特码纠正单个比特翻转错误。

## Application / 应用场景
- Quantum error correction (量子纠错)
- Fault-tolerant computing (容错计算)
- NISQ algorithms (NISQ 算法)

## Output / 输出
Corrected logical state despite physical errors.
尽管有物理错误，纠正后的逻辑态。"""

from quonic.algorithms import bit_flip_code

print("=== Bit-flip Error Correction ===\n")

for error_qubit in [0, 1, 2]:
    result = bit_flip_code(error_qubit=error_qubit, shots=100)
    print(f"Error on qubit {error_qubit}: counts = {result.counts}")
