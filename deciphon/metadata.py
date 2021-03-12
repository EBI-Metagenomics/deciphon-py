from __future__ import annotations

from typing import Type

from ._cdata import CData
from ._ffi import ffi, lib

__all__ = ["Metadata"]


class Metadata:
    def __init__(self, dcp_metadata: CData, own: bool):
        self._dcp_metadata = dcp_metadata
        self._own = own
        if self._dcp_metadata == ffi.NULL:
            raise RuntimeError("`dcp_metadata` is NULL.")

    @property
    def dcp_metadata(self) -> CData:
        return self._dcp_metadata

    @classmethod
    def create(cls: Type[Metadata], name: bytes, acc: bytes) -> Metadata:
        return cls(lib.dcp_metadata_create(name, acc), True)

    @property
    def acc(self) -> str:
        return ffi.string(lib.dcp_metadata_acc(self._dcp_metadata)).decode()

    @property
    def name(self) -> str:
        return ffi.string(lib.dcp_metadata_name(self._dcp_metadata)).decode()

    def __del__(self):
        if self._own and self._dcp_metadata != ffi.NULL:
            lib.dcp_metadata_destroy(self._dcp_metadata)
