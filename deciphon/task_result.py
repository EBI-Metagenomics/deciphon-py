from __future__ import annotations

from ._cdata import CData
from ._ffi import ffi, lib
from .result import Result

__all__ = ["TaskResult"]


class TaskResult:
    def __init__(self, dcp_results: CData):
        self._dcp_results = dcp_results
        if self._dcp_results == ffi.NULL:
            raise RuntimeError("`dcp_results` is NULL.")

        self._results = []
        r = lib.dcp_results_first(self._dcp_results)
        while r != ffi.NULL:
            self._results.append(Result(r))
            r = lib.dcp_results_next(self._dcp_results, r)

    @property
    def results(self):
        return self._results
