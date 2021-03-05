from importlib import import_module as _import_module

from .press import press
from .input import Input
from .output import Output
from . import example

try:
    __version__ = getattr(_import_module("deciphon._version"), "version", "x.x.x")
except ModuleNotFoundError:
    __version__ = "x.x.x"


__all__ = [
    "Input",
    "Output",
    "__version__",
    "example",
    "press",
]
