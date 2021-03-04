from __future__ import annotations

import imm
from typing import List, Type
from ._cdata import CData
from ._ffi import ffi, lib

__all__ = ["DCPProfile"]


class DCPProfile:
    def __init__(self, dcp_profile: CData, alphabet: imm.Alphabet):
        self._dcp_profile = dcp_profile
        if self._dcp_profile == ffi.NULL:
            raise RuntimeError("`dcp_profile` is NULL.")
        self._alphabet = alphabet
        self._models: List[imm.Model] = []

    @property
    def dcp_profile(self) -> CData:
        return self._dcp_profile

    @classmethod
    def create(cls: Type[DCPProfile], alphabet: imm.Alphabet) -> DCPProfile:
        return cls(lib.dcp_profile_create(alphabet.imm_abc), alphabet)

    def append_model(self, model: imm.Model):
        lib.dcp_profile_append_model(self._dcp_profile, model.imm_model)
        self._models.append(model)

    @property
    def alphabet(self):
        return self._alphabet

    @property
    def models(self):
        return self._models

    @property
    def profid(self) -> int:
        return lib.dcp_profile_id(self._dcp_profile)

    def __del__(self):
        if self._dcp_profile != ffi.NULL:
            lib.dcp_profile_free(self._dcp_profile)
