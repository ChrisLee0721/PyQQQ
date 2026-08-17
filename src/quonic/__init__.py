"""QuoNic — quantum programming, as simple as writing Python."""

from . import gates
from ._i18n import get_language, set_language
from .compare import qeq, qgt, qlt
from .compiler import RoutingError, compile, decompose, groverize
from .noise import NoiseModel, depolarizing
from .qgate import qgate
from .qif import cif, controlled, creg, cwhile, qif
from .qint import QInt, mul
from .qshow import qshow, qshow_all
from .readout import ReadoutCalibration, calibrate
from .result import Result
from .stack import reset
from .topology import CouplingMap
from .zne import ZNEResult, fold, zne

__version__ = "0.3.0"

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
    "qshow_all",
    "reset",
    "gates",
    "QInt",
    "Result",
    "NoiseModel",
    "depolarizing",
    "CouplingMap",
    "RoutingError",
    "compile",
    "decompose",
    "groverize",
    "zne",
    "fold",
    "ZNEResult",
    "calibrate",
    "ReadoutCalibration",
    "get_language",
    "set_language",
    "__version__",
]
