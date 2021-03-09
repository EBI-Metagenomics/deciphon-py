from __future__ import annotations

from pathlib import Path

from ._ffi import ffi, lib

__all__ = ["Server"]


class Server:
    def __init__(self, db_filepath: Path):

        self._dcp_server = ffi.NULL
        self._dcp_server = lib.dcp_server_create(bytes(db_filepath))
        if self._dcp_server == ffi.NULL:
            raise RuntimeError("`dcp_server` is NULL.")

    def scan(self, sequence: bytes):
        nresults = ffi.new("uint32_t[1]")
        results = lib.dcp_server_scan(self._dcp_server, sequence, nresults)
        alt_logliks = []
        profids = []
        for i in range(nresults[0]):
            alt_logliks.append(lib.dcp_result_alt_loglik(results[i]))
            profids.append(lib.dcp_result_profid(results[i]))
        return alt_logliks, profids

    def __del__(self):
        if self._dcp_server != ffi.NULL:
            lib.dcp_server_destroy(self._dcp_server)
