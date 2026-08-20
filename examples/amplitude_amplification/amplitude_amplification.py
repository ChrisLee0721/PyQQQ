"""Amplify probability of target state / 放大目标态概率

Like Grover but with custom state preparation. Boosts success probability.
类似 Grover 但支持自定义态制备。提升成功概率。

## Application / 应用场景
- Quantum algorithms (量子算法)
- State preparation (态制备)
- Error mitigation (错误缓解)

## Output / 输出
Target state probability amplified from p to ~1.
目标态概率从 p 放大到 ~1。"""

from quonic.algorithms import amplitude_amplification, mark_state

oracle_fn = mark_state("11")
result = amplitude_amplification(2, oracle_fn, shots=1024)
print(result.counts)
