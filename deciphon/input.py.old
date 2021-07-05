from __future__ import annotations

from typing import Iterator, Type

from ._cdata import CData
from ._ffi import ffi, lib
from .dcp_profile import DCPProfile

__all__ = ["Input"]


class Input:
    def __init__(self, dcp_input: CData):
        self._dcp_input = dcp_input
        if self._dcp_input == ffi.NULL:
            raise RuntimeError("`dcp_input` is NULL.")

        # dcp_input_metadata(struct dcp_input const* input, uint32_t profid);

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

    @property
    def nprofiles(self) -> int:
        return lib.dcp_input_nprofiles(self._dcp_input)

    def reset(self):
        err: int = lib.dcp_input_reset(self._dcp_input)
        if err != 0:
            raise RuntimeError("Could not reset input.")

    def close(self):
        err: int = lib.dcp_input_close(self._dcp_input)
        if err != 0:
            raise RuntimeError("Could not close input.")

    def __iter__(self) -> Iterator[DCPProfile]:
        while True:
            try:
                yield self.read()
            except StopIteration:
                return

    def __del__(self):
        if self._dcp_input != ffi.NULL:
            lib.dcp_input_destroy(self._dcp_input)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del exception_type
        del exception_value
        del traceback
        self.close()
