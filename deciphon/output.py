from __future__ import annotations

from typing import Type

from .dcp_profile import DCPProfile

from ._cdata import CData
from ._ffi import ffi, lib

__all__ = ["Output"]


class Output:
    def __init__(self, dcp_output: CData):
        self._dcp_output = dcp_output
        if self._dcp_output == ffi.NULL:
            raise RuntimeError("`dcp_output` is NULL.")

    @classmethod
    def create(cls: Type[Output], filepath: bytes) -> Output:
        return cls(lib.dcp_output_create(filepath))

    def write(self, prof: DCPProfile):
        err: int = lib.dcp_output_write(self._dcp_output, prof.dcp_profile)
        if err != 0:
            raise RuntimeError("Could not write profile.")

    def close(self):
        err: int = lib.dcp_output_close(self._dcp_output)
        if err != 0:
            raise RuntimeError("Could not close output.")

    def __del__(self):
        if self._dcp_output != ffi.NULL:
            lib.dcp_output_destroy(self._dcp_output)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        self.close()
