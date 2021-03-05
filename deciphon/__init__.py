from importlib import import_module as _import_module

from .press import press
from .input import Input
from .output import Output
from . import example, test

try:
    from ._ffi import lib
except Exception as e:
    _ffi_err = """
It is likely caused by a broken installation of this package.
Please, make sure you have a C compiler and try to uninstall
and reinstall the package again."""

    raise RuntimeError(str(e) + _ffi_err)

try:
    __version__ = getattr(_import_module("deciphon._version"), "version", "x.x.x")
except ModuleNotFoundError:
    __version__ = "x.x.x"


__all__ = [
    "Input",
    "Output",
    "__version__",
    "example",
    "lib",
    "press",
    "test",
]
