"""Noise model / 噪声模型

Noise model / 噪声模型"""

from quonic import NoiseModel, qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=NoiseModel(single=0.01, double=0.05))
