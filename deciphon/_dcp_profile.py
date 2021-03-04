from __future__ import annotations


from imm import Alphabet, Model

from typing import List, Type
from ._cdata import CData
from ._ffi import ffi, lib

__all__ = ["DCPProfile"]


class DCPProfile:
    def __init__(self, dcp_profile: CData, alphabet: Alphabet):
        self._dcp_profile = dcp_profile
        if self._dcp_profile == ffi.NULL:
            raise RuntimeError("`dcp_profile` is NULL.")
        self._alphabet = alphabet
        self._models: List[Model] = []

    @property
    def dcp_profile(self) -> CData:
        return self._dcp_profile

    @classmethod
    def create(cls: Type[DCPProfile], alphabet: Alphabet) -> DCPProfile:
        return cls(lib.dcp_profile_create(alphabet.imm_abc), alphabet)

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def profid(self) -> int:
        return lib.dcp_profile_id(self._dcp_profile)

    @property
    def nmodels(self) -> int:
        return lib.dcp_profile_nmodels(self._dcp_profile)

    def get_model(self, i: int) -> int:
        return self._models[i]

    def __del__(self):
        if self._dcp_profile != ffi.NULL:
            lib.dcp_profile_destroy(self._dcp_profile)
