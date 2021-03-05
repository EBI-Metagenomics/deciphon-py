from __future__ import annotations

import imm
import nmm
from typing import List, Type
from ._cdata import CData
from ._ffi import ffi, lib

__all__ = ["DCPProfile"]


class DCPProfile:
    def __init__(self, dcp_profile: CData, profile: nmm.Profile):
        self._dcp_profile = dcp_profile
        if self._dcp_profile == ffi.NULL:
            raise RuntimeError("`dcp_profile` is NULL.")
        self._profile = profile
        self._models: List[imm.Model] = []

    @property
    def dcp_profile(self) -> CData:
        return self._dcp_profile

    @classmethod
    def create(cls: Type[DCPProfile], alphabet: nmm.BaseAlphabet) -> DCPProfile:
        dcp_profile = lib.dcp_profile_create(alphabet.imm_abc)
        prof = nmm.wrap.nmm_profile(lib.dcp_profile_nmm_profile(dcp_profile), alphabet)
        return cls(dcp_profile, prof)

    def append_model(self, model: imm.Model):
        lib.dcp_profile_append_model(self._dcp_profile, model.imm_model)
        self._models.append(model)

    @property
    def alphabet(self):
        return self._profile._alphabet

    @property
    def models(self):
        return self._models

    @property
    def profid(self) -> int:
        return lib.dcp_profile_id(self._dcp_profile)

    def __del__(self):
        if self._dcp_profile != ffi.NULL:
            lib.dcp_profile_free(self._dcp_profile)
