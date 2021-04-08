from __future__ import annotations

from nmm import Codon

from ._cdata import CData
from ._ffi import ffi, lib
from .codon_table import CodonTable

__all__ = ["Result"]


class Result:
    def __init__(self, dcp_result: CData, codon_table: CodonTable):
        self._dcp_result = dcp_result
        if self._dcp_result == ffi.NULL:
            raise RuntimeError("`dcp_result` is NULL.")
        self._codon_table = codon_table

    @property
    def dcp_result(self):
        return self._dcp_result

    @property
    def profid(self) -> int:
        return lib.dcp_result_profid(self._dcp_result)

    @property
    def seqid(self) -> int:
        return lib.dcp_result_seqid(self._dcp_result)

    @property
    def alt_loglik(self) -> float:
        return lib.dcp_result_loglik(self._dcp_result, 0)

    @property
    def alt_stream(self):
        dcp_string = lib.dcp_result_path(self._dcp_result, 0)
        data = lib.dcp_string_data(dcp_string)
        # size = lib.dcp_string_size(dcp_string)
        return ffi.string(data).decode()

    @property
    def alt_codon_stream(self):
        dcp_string = lib.dcp_result_codons(self._dcp_result, 0)
        data = lib.dcp_string_data(dcp_string)
        # size = lib.dcp_string_size(dcp_string)
        return ffi.string(data).decode()

    @property
    def alt_amino_stream(self):
        base_abc = self._codon_table.base_alphabet
        cstream = self.alt_codon_stream
        aminos = []
        for i in range(0, len(cstream), 3):
            codon = Codon.create(cstream[i : i + 3].encode(), base_abc)
            amino = self._codon_table.amino_acid(codon)
            aminos.append(amino.decode())
        return "".join(aminos)

    @property
    def null_loglik(self) -> float:
        return lib.dcp_result_loglik(self._dcp_result, 1)

    @property
    def null_stream(self):
        dcp_string = lib.dcp_result_path(self._dcp_result, 1)
        data = lib.dcp_string_data(dcp_string)
        # size = lib.dcp_string_size(dcp_string)
        return ffi.string(data).decode()

    @property
    def null_codon_stream(self):
        dcp_string = lib.dcp_result_codons(self._dcp_result, 1)
        data = lib.dcp_string_data(dcp_string)
        # size = lib.dcp_string_size(dcp_string)
        return ffi.string(data).decode()

    @property
    def null_amino_stream(self):
        base_abc = self._codon_table.base_alphabet
        cstream = self.null_codon_stream
        aminos = []
        for i in range(0, len(cstream), 3):
            codon = Codon.create(cstream[i : i + 3].encode(), base_abc)
            amino = self._codon_table.amino_acid(codon)
            aminos.append(amino.decode())
        return "".join(aminos)
