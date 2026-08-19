"""Quantum Graph Neural Network demo.

Quantum version of GNN for graph-structured data.
Output: node/graph embeddings.
"""

from quonic.algorithms import qgnn_demo

result = qgnn_demo()
print(result.counts)
