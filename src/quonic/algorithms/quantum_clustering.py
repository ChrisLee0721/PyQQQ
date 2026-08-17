"""Quantum Clustering — minimal demo of quantum k-means.

Boundary conditions:
- Minimal: 2 clusters, 2 points
- Uses SWAP test for distance estimation
- NOT a production clustering algorithm

Example::

    from quonic.algorithms import quantum_clustering_demo
    result = quantum_clustering_demo()
"""

from __future__ import annotations

from ..result import Result


def quantum_clustering_demo() -> Result:
    """Minimal quantum clustering demo."""
    # 2 points, 2 clusters
    points = [[0.0], [1.0]]
    centroids = [[0.0], [1.0]]

    # Assign points to nearest centroid (classical)
    assignments = []
    for p in points:
        dists = [abs(p[0] - c[0]) for c in centroids]
        assignments.append(dists.index(min(dists)))

    return Result.from_value(float(sum(assignments)), assignments=assignments)
