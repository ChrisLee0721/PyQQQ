"""Quantum Transformer demo.

Quantum attention mechanism for sequence modeling.
Output: attention weights.
"""

from quonic.algorithms import qtransformer_demo

result = qtransformer_demo()
print(result.counts)
