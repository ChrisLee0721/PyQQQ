"""Noise simulation / 噪声模拟

Noise simulation / 噪声模拟"""

from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=0.05)
