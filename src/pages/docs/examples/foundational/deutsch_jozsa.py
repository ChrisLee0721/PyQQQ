"""Constant or balanced function? / 常数还是平衡函数？

Determine if f is constant or balanced in one query.
一次查询确定 f 是常数还是平衡函数。

## Application / 应用场景
- Oracle complexity (预言机复杂度)
- Quantum advantage (量子优势)
- Function analysis (函数分析)

## Output / 输出
All zeros = constant, anything else = balanced.
全零 = 常数，其他 = 平衡。"""

from quonic.algorithms import deutsch_jozsa
from quonic.ir import GateOperation


# Constant oracle: f(x) = 0 for all x
def constant_oracle(circuit, n):
    pass


# Balanced oracle: f(x) = x_0
def balanced_oracle(circuit, n):
    circuit.add(GateOperation("cx", (0, n)))


print("=== Deutsch-Jozsa Algorithm ===\n")

result_const = deutsch_jozsa(3, constant_oracle, shots=100)
print(f"Constant oracle: is_balanced = {result_const.metadata['is_balanced']}")

result_bal = deutsch_jozsa(3, balanced_oracle, shots=100)
print(f"Balanced oracle: is_balanced = {result_bal.metadata['is_balanced']}")
