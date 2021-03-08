import nmm

from ._cdata import CData
from ._ffi import lib
from .dcp_profile import DCPProfile

__all__ = ["dcp_profile"]


def dcp_profile(ptr: CData) -> DCPProfile:
    nmm_profile = lib.dcp_profile_nmm_profile(ptr)
    prof = nmm.wrap.nmm_profile(nmm_profile)
    return DCPProfile(ptr, prof)
