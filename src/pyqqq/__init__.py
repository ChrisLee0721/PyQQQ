"""PyQQQ —— 量子编程，像写 Python 一样简单。"""

from .qgate import qgate
from .qshow import qshow
from .stack import reset
from . import gates

__version__ = "0.1.0"

__all__ = ["qgate", "qshow", "reset", "gates", "__version__"]
