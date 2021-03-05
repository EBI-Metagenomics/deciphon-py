from __future__ import annotations

from typing import Type

from ._cdata import CData
from .dcp_profile import DCPProfile
from ._ffi import ffi, lib

__all__ = ["Input"]


class Input:
    def __init__(self, dcp_input: CData):
        if dcp_input == ffi.NULL:
            raise RuntimeError("`dcp_input` is NULL.")
        self._dcp_input = dcp_input

    @classmethod
    def create(cls: Type[Input], filepath: bytes) -> Input:
        return cls(lib.dcp_input_create(filepath))

    def read(self) -> DCPProfile:
        from . import wrap

        dcp_profile = lib.dcp_input_read(self._dcp_input)
        if dcp_profile == ffi.NULL:
            if lib.dcp_input_end(self._dcp_input):
                raise StopIteration
            raise RuntimeError("Could not read profile.")

        return wrap.dcp_profile(dcp_profile)

    def create_partition(self, part: int, nparts: int) -> Partition:
        dcp_partition = lib.dcp_input_create_partition(self._dcp_input, part, nparts)
        if dcp_partition == ffi.NULL:
            raise RuntimeError("Could not create partition.")
        return Partition(dcp_partition)

    def close(self):
        pass
        # err: int = lib.nmm_input_close(self._dcp_input)
        # if err != 0:
        #     raise RuntimeError("Could not close input.")

    def __del__(self):
        if self._dcp_input != ffi.NULL:
            lib.dcp_input_destroy(self._dcp_input)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        # self.close()
