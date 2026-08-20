"""Quantum Bayesian Inference / 量子贝叶斯推断

Quantum version of Bayesian updating.
量子版贝叶斯更新。

## Application / 应用场景
- Inference (推断)
- Decision making (决策)
- Statistics (统计)

## Output / 输出
Posterior probabilities.
后验概率。"""

from quonic.algorithms import quantum_bayesian_demo

result = quantum_bayesian_demo(prior_h0=0.5, likelihood_h0=0.8, likelihood_h1=0.3)
print(result.counts)
