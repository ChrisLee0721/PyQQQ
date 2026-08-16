"""算法模板：Grover 搜索 / VQE / QAOA / QPE。

每个模板只依赖 numpy / scipy，不绑定具体后端；采样类算法
（Grover、QPE）可切换 qiskit / cirq / pennylane 任意后端。
"""

from .grover import diffusion, grover, mark_state
from .hamiltonians import from_qiskit_nature
from .oracle import oracle
from .qaoa import qaoa_maxcut
from .qpe import qpe
from .quantum_counting import quantum_counting
from .shor import shor
from .vqe import vqe

__all__ = [
    "grover",
    "mark_state",
    "diffusion",
    "oracle",
    "quantum_counting",
    "shor",
    "vqe",
    "qaoa_maxcut",
    "from_qiskit_nature",
    "qpe",
]
