"""Quantum Walk / 量子行走

Quantum analogue of random walk, spreads quadratically faster.
随机行走的量子类比，二次方更快扩展。

## Application / 应用场景
- Search algorithms (搜索算法)
- Graph algorithms (图算法)
- Transport phenomena (输运现象)

## Output / 输出
Position distribution after n steps.
n 步后的位置分布。"""

from quonic.algorithms import quantum_walk

result = quantum_walk(n_positions=5, steps=10, shots=1024)
print(result.counts)
