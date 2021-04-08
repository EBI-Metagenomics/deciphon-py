from __future__ import annotations

from nmm import DNAAlphabet, IUPACAminoAlphabet

from ._ffi import ffi, lib
from .codon_table import CodonTable
from .result import Result

__all__ = ["Task"]


class Task:
    def __init__(
        self, loglik: bool, null: bool, multiple_hits: bool, hmmer3_compat: bool
    ):
        self._cfg = ffi.new("struct dcp_task_cfg[1]")
        self._cfg[0].loglik = loglik
        self._cfg[0].null = null
        self._cfg[0].multiple_hits = multiple_hits
        self._cfg[0].hmmer3_compat = hmmer3_compat

        self._dcp_task = ffi.NULL
        self._dcp_task = lib.dcp_task_create(self._cfg[0])
        if self._dcp_task == ffi.NULL:
            raise RuntimeError("`dcp_task` is NULL.")

        self._task_result = None

    def end(self):
        return lib.dcp_task_end(self._dcp_task)

    def read(self):
        dcp_result = lib.dcp_task_read(self._dcp_task)
        if dcp_result == ffi.NULL:
            return None
        abc = DNAAlphabet()
        codon_table = CodonTable(abc, IUPACAminoAlphabet())
        return Result(dcp_result, codon_table)

    @property
    def dcp_task(self):
        return self._dcp_task

    def add_seq(self, sequence: bytes):
        lib.dcp_task_add_seq(self._dcp_task, sequence)

    # @property
    # def result(self):
    #     if self._task_result is None:
    #         abc = DNAAlphabet()
    #         codon_table = CodonTable(abc, IUPACAminoAlphabet())
    #         dcp_task_results = lib.dcp_task_results(self._dcp_task)
    #         self._task_result = TaskResult(dcp_task_results, codon_table)
    #     return self._task_result

    # def reset(self):
    #     lib.dcp_task_reset(self._dcp_task)

    # def __del__(self):
    #     if self._dcp_task != ffi.NULL:
    #         lib.dcp_task_destroy(self._dcp_task)
