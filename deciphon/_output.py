from __future__ import annotations

from typing import Type

from nmm import Model

from ._cdata import CData
from ._ffi import ffi, lib

__all__ = ["Output"]


class Output:
    def __init__(self, dcp_output: CData):
        if dcp_output == ffi.NULL:
            raise RuntimeError("`dcp_output` is NULL.")
        self._dcp_output = dcp_output

    @classmethod
    def create(cls: Type[Output], filepath: bytes, nmodels: int) -> Output:
        return cls(lib.dcp_output_create(filepath, nmodels))

    def write(self, model: Model):
        err: int = lib.dcp_output_write(self._dcp_output, model.nmm_model)
        if err != 0:
            raise RuntimeError("Could not write model.")

    def close(self):
        err: int = lib.dcp_output_close(self._dcp_output)
        if err != 0:
            raise RuntimeError("Could not close output.")

    def __del__(self):
        if self._dcp_output != ffi.NULL:
            # self.close()
            lib.dcp_output_destroy(self._dcp_output)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        # self.close()
