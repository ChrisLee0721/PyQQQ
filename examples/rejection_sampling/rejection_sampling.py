"""Rejection Sampling / 拒绝采样

Quantum-enhanced rejection sampling.
量子增强的拒绝采样。

## Application / 应用场景
- Sampling (采样)
- Distribution generation (分布生成)
- Monte Carlo (蒙特卡洛)

## Output / 输出
Samples from target distribution.
目标分布的样本。"""

from quonic.algorithms import rejection_sampling_demo

result = rejection_sampling_demo(n_samples=100)
print(result.counts)
