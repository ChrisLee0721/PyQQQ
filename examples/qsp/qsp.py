"""Quantum Signal Processing demo.

Core subroutine for quantum singular value transformation.
Output: transformed signal.
"""

from quonic.algorithms import qsp_demo

result = qsp_demo(angle=0.785)
print(result.counts)
