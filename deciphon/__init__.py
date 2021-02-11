from importlib import import_module as _import_module

try:
    __version__ = getattr(_import_module("deciphon._version"), "version", "x.x.x")
except ModuleNotFoundError:
    __version__ = "x.x.x"


__all__ = [
    "__version__",
]
