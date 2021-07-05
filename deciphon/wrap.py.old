import nmm

from ._cdata import CData
from ._ffi import lib
from .dcp_profile import DCPProfile
from .metadata import Metadata

__all__ = ["dcp_profile"]


def dcp_profile(ptr: CData) -> DCPProfile:
    nmm_profile = lib.dcp_profile_nmm_profile(ptr)
    prof = nmm.wrap.nmm_profile(nmm_profile)
    mt = Metadata(lib.dcp_profile_metadata(ptr))
    return DCPProfile(ptr, prof, mt)
