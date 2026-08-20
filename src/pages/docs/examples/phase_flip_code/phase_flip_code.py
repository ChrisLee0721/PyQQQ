"""Correct phase-flip errors / 纠正相位翻转错误

3-qubit code corrects single phase-flip errors.
3 比特码纠正单个相位翻转错误。

## Application / 应用场景
- Quantum error correction (量子纠错)
- Phase protection (相位保护)
- NISQ algorithms (NISQ 算法)

## Output / 输出
Corrected logical state despite phase errors.
尽管有相位错误，纠正后的逻辑态。"""

from quonic.algorithms import phase_flip_code

result = phase_flip_code(error_qubit=0, shots=100)
print(result.counts)
