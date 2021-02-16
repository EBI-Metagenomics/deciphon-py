from __future__ import annotations

import nmm

from ._cdata import CData
from ._ffi import ffi, lib

__all__ = ["Partition"]


class Partition:
    def __init__(self, dcp_partition: CData):
        if dcp_partition == ffi.NULL:
            raise RuntimeError("`dcp_partition` is NULL.")
        self._dcp_partition = dcp_partition

    def read(self) -> nmm.Model:
        return nmm.wrap.nmm_model(lib.dcp_partition_read(self._dcp_partition))

    def reset(self):
        lib.dcp_partition_reset(self._dcp_partition)

    def eof(self) -> bool:
        return lib.dcp_partition_eof(self._dcp_partition)

    def nmodels(self) -> int:
        return lib.dcp_partition_nmodels(self._dcp_partition)
