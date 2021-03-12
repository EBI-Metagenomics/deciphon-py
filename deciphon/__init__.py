from importlib import import_module as _import_module

from . import example, test
from .input import Input
from .legacy_result import legacy_result
from .output import Output
from .output_writer import OutputWriter
from .press import press
from .profile import ProfileID
from .result import Result
from .server import Server
from .task import Task
from .task_result import TaskResult

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
    "Result",
    "Server",
    "Task",
    "TaskResult",
    "__version__",
    "example",
    "legacy_result",
    "lib",
    "press",
    "test",
    "OutputWriter",
    "ProfileID",
]
