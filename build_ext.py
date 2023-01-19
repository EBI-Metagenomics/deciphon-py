import os
import shutil
import sys
import tarfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from subprocess import check_call

PWD = Path(os.path.dirname(os.path.abspath(__file__)))
DST = PWD / ".ext_deps"

CMAKE_OPTS = [
    "-DCMAKE_PREFIX_PATH=",
    "-DCMAKE_BUILD_TYPE=Release",
    "-DBUILD_SHARED_LIBS=ON",
]

CPM_OPTS = ["-DCPM_USE_LOCAL_PACKAGES=ON"]

EXTRA = {
    "linux": ["-Wl,-rpath,$ORIGIN/../.ext_deps/lib"],
    "macos": ["-Wl,-rpath,@loader_path/../.ext_deps/lib"],
}


@dataclass
class Dependency:
    user: str
    project: str
    version: str
    cmake_opts: list[str]


DEPS = [
    Dependency("horta", "logaddexp", "2.1.14", CMAKE_OPTS),
    Dependency("horta", "elapsed", "3.1.2", CMAKE_OPTS),
    Dependency("EBI-Metagenomics", "lip", "0.5.0", CMAKE_OPTS),
    Dependency("EBI-Metagenomics", "hmr", "0.6.0", CMAKE_OPTS),
    Dependency("EBI-Metagenomics", "imm", "2.1.10", CMAKE_OPTS + CPM_OPTS),
    Dependency("EBI-Metagenomics", "deciphon", "0.3.6", CMAKE_OPTS + CPM_OPTS),
]


def rm(folder: Path, pattern: str):
    for filename in folder.glob(pattern):
        filename.unlink()


def get_cmake_bin():
    from cmake import CMAKE_BIN_DIR

    bins = [str(v) for v in Path(CMAKE_BIN_DIR).glob("cmake*")]
    return bins[0]


def cleanup_intree_artifacts():
    rm(PWD / "deciphon", "cffi.*")
    rm(PWD / "deciphon", "*.o")
    rm(PWD / "deciphon", "*.so")
    rm(PWD / "deciphon", "*.dylib")


def cleanup_ext_deps():
    shutil.rmtree(DST, ignore_errors=True)


def build_dep(dep: Dependency):
    prj_dir = DST / f"{dep.project}-{dep.version}"
    bld_dir = prj_dir / "build"
    os.makedirs(bld_dir, exist_ok=True)

    url = f"https://github.com/{dep.user}/{dep.project}/archive/refs/tags/v{dep.version}.tar.gz"

    with urllib.request.urlopen(url) as rf:
        data = rf.read()

    tar_filename = f"{dep.project}-{dep.version}.tar.gz"

    with open(DST / tar_filename, "wb") as lf:
        lf.write(data)

    with tarfile.open(DST / tar_filename) as tf:
        tf.extractall(DST)

    cmake = get_cmake_bin()
    check_call([cmake, "-S", str(prj_dir), "-B", str(bld_dir)] + dep.cmake_opts)
    check_call([cmake, "--build", str(bld_dir), "--config", "Release"])
    check_call([cmake, "--install", str(bld_dir), "--prefix", str(DST)])


def osname() -> str:
    if sys.platform.startswith("linux"):
        return "linux"
    if sys.platform.startswith("darwin"):
        return "macos"
    assert False


if __name__ == "__main__":
    from cffi import FFI

    ffibuilder = FFI()

    cleanup_intree_artifacts()
    cleanup_ext_deps()

    for dep in DEPS:
        build_dep(dep)

    library_dirs = [DST / "lib", DST / "lib64"]
    include_dirs = [DST / "include"]

    with open(PWD / "deciphon" / "interface.h", "r") as f:
        interface_h = f.read()

    ffibuilder.cdef(interface_h)
    ffibuilder.set_source(
        "deciphon.cffi",
        """
        #include "deciphon/deciphon.h"
        """,
        language="c",
        libraries=["deciphon"],
        library_dirs=[str(d) for d in library_dirs if d.exists()],
        include_dirs=[str(d) for d in include_dirs if d.exists()],
        extra_link_args=EXTRA[osname()],
    )
    ffibuilder.compile(verbose=True)
