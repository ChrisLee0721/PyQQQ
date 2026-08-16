"""QuoNic —— 量子编程，像写 Python 一样简单。"""

from . import gates
from .compare import qeq, qgt, qlt
from .compiler import RoutingError, decompose
from .noise import NoiseModel, depolarizing
from .qgate import qgate
from .qif import cif, controlled, creg, cwhile, qif
from .qint import QInt, mul
from .qshow import qshow
from .result import Result
from .stack import reset
from .topology import CouplingMap

__version__ = "0.2.1"

__all__ = [
    "qgate",
    "qif",
    "cif",
    "controlled",
    "creg",
    "cwhile",
    "qlt",
    "qeq",
    "qgt",
    "mul",
    "qshow",
    "reset",
    "gates",
    "QInt",
    "Result",
    "NoiseModel",
    "depolarizing",
    "CouplingMap",
    "RoutingError",
    "decompose",
    "__version__",
]
