"""QuoNic — quantum programming, as simple as writing Python."""

from . import gates
from ._i18n import get_language, set_language
from .analysis import CircuitReport, analyze
from .batch import run_batch
from .compare import qeq, qgt, qlt
from .compiler import RoutingError, compile, decompose, groverize, optimize
from .encoding import amplitude_encode, angle_encode
from .gradients import numerical_gradient, param_shift
from .noise import NoiseModel, depolarizing
from .parameters import Parameter, bind_batch, bind_params
from .qgate import qgate
from .qif import cif, controlled, creg, cwhile, qif
from .qint import QInt, mul
from .qshow import qshow, qshow_all, run_circuits
from .readout import ReadoutCalibration, calibrate
from .result import Result
from .stack import reset
from .stepper import StepExecutor
from .topology import CouplingMap
from .zne import ZNEResult, fold, zne

__version__ = "0.8.0"

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
    "run_circuits",
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
    "optimize",
    "analyze",
    "CircuitReport",
    "param_shift",
    "numerical_gradient",
    "Parameter",
    "bind_params",
    "bind_batch",
    "run_batch",
    "angle_encode",
    "amplitude_encode",
    "StepExecutor",
    "zne",
    "fold",
    "ZNEResult",
    "calibrate",
    "ReadoutCalibration",
    "get_language",
    "set_language",
    "__version__",
]
