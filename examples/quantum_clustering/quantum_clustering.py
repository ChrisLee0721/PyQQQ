"""Quantum Clustering / 量子聚类

Quantum algorithm for unsupervised clustering.
无监督聚类的量子算法。

## Application / 应用场景
- Data analysis (数据分析)
- Customer segmentation (客户细分)
- Anomaly detection (异常检测)

## Output / 输出
Cluster assignments.
聚类分配。"""

from quonic.algorithms import quantum_clustering_demo

result = quantum_clustering_demo()
print(result.counts)
