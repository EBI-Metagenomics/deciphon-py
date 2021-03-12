from __future__ import annotations

from ._cdata import CData
from ._ffi import ffi, lib

__all__ = ["Result"]


class Result:
    def __init__(self, dcp_result: CData):
        self._dcp_result = dcp_result
        if self._dcp_result == ffi.NULL:
            raise RuntimeError("`dcp_result` is NULL.")

    @property
    def profid(self) -> int:
        return lib.dcp_result_profid(self._dcp_result)

    @property
    def seqid(self) -> int:
        return lib.dcp_result_seqid(self._dcp_result)

    @property
    def alt_loglik(self) -> float:
        return lib.dcp_result_alt_loglik(self._dcp_result)

    @property
    def alt_stream(self):
        return ffi.string(lib.dcp_result_alt_stream(self._dcp_result)).decode()

    @property
    def alt_codon_stream(self):
        return ffi.string(lib.dcp_result_alt_codon_stream(self._dcp_result)).decode()

    @property
    def null_loglik(self) -> float:
        return lib.dcp_result_null_loglik(self._dcp_result)

    @property
    def null_stream(self):
        return ffi.string(lib.dcp_result_null_stream(self._dcp_result)).decode()

    @property
    def null_codon_stream(self):
        return ffi.string(lib.dcp_result_null_codon_stream(self._dcp_result)).decode()

    def __del__(self):
        if self._dcp_result != ffi.NULL:
            lib.dcp_result_destroy(self._dcp_result)
