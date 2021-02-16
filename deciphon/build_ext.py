import os
from os.path import join
from typing import List

import imm.build_ext
import nmm.build_ext
from cffi import FFI

ffibuilder = FFI()
libs = ["deciphon"]

ffibuilder.include(imm.build_ext.ffibuilder)
ffibuilder.include(nmm.build_ext.ffibuilder)

folder = os.path.dirname(os.path.abspath(__file__))

with open(join(folder, "deciphon.h"), "r") as f:
    ffibuilder.cdef(f.read())

extra_link_args: List[str] = []
if "DECIPHON_EXTRA_LINK_ARGS" in os.environ:
    extra_link_args += os.environ["DECIPHON_EXTRA_LINK_ARGS"].split(os.pathsep)

ffibuilder.set_source(
    "deciphon._ffi",
    r"""
    #include "deciphon/deciphon.h"
    """,
    libraries=libs,
    extra_link_args=extra_link_args,
    language="c",
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
