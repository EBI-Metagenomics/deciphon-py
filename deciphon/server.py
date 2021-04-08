from __future__ import annotations

from pathlib import Path

from ._ffi import ffi, lib
from .metadata import Metadata
from .task import Task

__all__ = ["Server"]


class Server:
    def __init__(self, db_filepath: Path):

        self._dcp_server = ffi.NULL
        self._dcp_server = lib.dcp_server_create(bytes(db_filepath))
        if self._dcp_server == ffi.NULL:
            raise RuntimeError("`dcp_server` is NULL.")

        ids = range(lib.dcp_server_nprofiles(self._dcp_server))
        ptrs = [lib.dcp_server_metadata(self._dcp_server, i) for i in ids]
        self._metadatas = [Metadata(ptr, False) for ptr in ptrs]

    def start(self):
        assert lib.dcp_server_start(self._dcp_server) == 0

    def stop(self):
        lib.dcp_server_stop(self._dcp_server)

    def join(self):
        assert lib.dcp_server_join(self._dcp_server) == 0

    def add_task(self, task: Task):
        lib.dcp_server_add_task(self._dcp_server, task.dcp_task)

    def metadata(self, profid: int):
        return self._metadatas[profid]

    def free_result(self, result):
        lib.dcp_server_free_result(self._dcp_server, result.dcp_result)

    def free_task(self, task):
        lib.dcp_server_free_task(self._dcp_server, task.dcp_task)

    @property
    def nprofiles(self) -> int:
        return lib.dcp_server_nprofiles(self._dcp_server)

    def __del__(self):
        if self._dcp_server != ffi.NULL:
            lib.dcp_server_destroy(self._dcp_server)
