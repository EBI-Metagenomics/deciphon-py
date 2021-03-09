from __future__ import annotations

from typing import Type

import imm
import nmm

from ._cdata import CData
from ._ffi import ffi, lib
from .metadata import Metadata

__all__ = ["DCPProfile"]


class DCPProfile:
    def __init__(self, dcp_profile: CData, profile: nmm.Profile, metadata: Metadata):
        self._dcp_profile = dcp_profile
        if self._dcp_profile == ffi.NULL:
            raise RuntimeError("`dcp_profile` is NULL.")
        self._profile = profile
        self._metadata = metadata

    @property
    def dcp_profile(self) -> CData:
        return self._dcp_profile

    @classmethod
    def create(
        cls: Type[DCPProfile], alphabet: nmm.BaseAlphabet, metadata: Metadata
    ) -> DCPProfile:
        dcp_profile = lib.dcp_profile_create(alphabet.imm_abc, metadata.dcp_metadata)
        prof = nmm.wrap.nmm_profile(lib.dcp_profile_nmm_profile(dcp_profile), alphabet)
        return cls(dcp_profile, prof, metadata)

    def append_model(self, model: imm.Model):
        self._profile.append_model(model)

    @property
    def alphabet(self):
        return self._profile.alphabet

    @property
    def metadata(self) -> Metadata:
        return self._metadata

    @property
    def models(self):
        return self._profile.models

    @property
    def profid(self) -> int:
        return lib.dcp_profile_id(self._dcp_profile)

    def __del__(self):
        if self._dcp_profile != ffi.NULL:
            lib.dcp_profile_free(self._dcp_profile)
