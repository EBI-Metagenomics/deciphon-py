import os
import shutil
import subprocess
import tarfile
import urllib.request
from pathlib import Path

PWD = Path(os.path.dirname(os.path.abspath(__file__)))
USER = "horta"
PROJECT = "deciphon"
VERSION = "0.5.0"
CMAKE_OPTS = [
    "-DCMAKE_BUILD_TYPE=Release",
    "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
    "-DBUILD_SHARED_LIBS=ON",
]


def rm(folder: Path, pattern: str):
    for filename in folder.glob(pattern):
        filename.unlink()


def get_cmake_bin():
    from cmake import CMAKE_BIN_DIR

    bins = [str(v) for v in Path(CMAKE_BIN_DIR).glob("cmake*")]
    return bins[0]


def cleanup_intree_artifacts():
    rm(PWD / "deciphon", "cffi.c")
    rm(PWD / "deciphon", "*.o")
    rm(PWD / "deciphon", "*.so")
    rm(PWD / "deciphon", "*.dylib")


def build_deps():
    ext_dir = PWD / ".ext_deps"
    shutil.rmtree(ext_dir, ignore_errors=True)

    prj_dir = ext_dir / f"{PROJECT}-{VERSION}"
    build_dir = prj_dir / "build"
    os.makedirs(build_dir, exist_ok=True)

    url = f"https://github.com/{USER}/{PROJECT}/archive/refs/tags/v{VERSION}.tar.gz"

    with urllib.request.urlopen(url) as rf:
        data = rf.read()

    tar_filename = f"{PROJECT}-{VERSION}.tar.gz"

    with open(ext_dir / tar_filename, "wb") as lf:
        lf.write(data)

    with tarfile.open(ext_dir / tar_filename) as tf:
        tf.extractall(ext_dir)

    cmake_bin = get_cmake_bin()
    subprocess.check_call(
        [cmake_bin, "-S", str(prj_dir), "-B", str(build_dir)] + CMAKE_OPTS
    )
    subprocess.check_call([cmake_bin, "--build", str(build_dir), "--config", "Release"])
    subprocess.check_call(
        [cmake_bin, "--install", str(build_dir), "--prefix", str(ext_dir)]
    )
    rm(ext_dir / "lib", "*.dylib")
    rm(ext_dir / "lib", "*.so*")
    rm(ext_dir / "lib64", "*.dylib")
    rm(ext_dir / "lib64", "*.so*")


if __name__ == "__main__":
    from cffi import FFI

    ffibuilder = FFI()

    cleanup_intree_artifacts()
    build_deps()
    # library_dirs = [PWD / ".ext_deps" / "lib", PWD / ".ext_deps" / "lib64"]
    library_dirs = [
        PWD / ".ext_deps" / f"deciphon-{VERSION}/build",
        PWD / ".ext_deps" / f"deciphon-{VERSION}/build/press",
        PWD / ".ext_deps" / "lib64",
    ]
    # include_dirs = [PWD / ".ext_deps" / "include"]
    # include_dirs = [PWD / ".ext_deps"]
    include_dirs = [
        PWD / ".ext_deps" / f"deciphon-{VERSION}",
        PWD / ".ext_deps" / f"deciphon-{VERSION}/build/_deps/lite-pack-src/include",
        PWD / ".ext_deps" / f"deciphon-{VERSION}/build/_deps/imm-src/include",
        PWD / ".ext_deps" / f"deciphon-{VERSION}/build/_deps/hmmer-reader-src/include",
        PWD / ".ext_deps" / f"deciphon-{VERSION}/build/_deps/elapsed-src/include",
        PWD / ".ext_deps" / f"deciphon-{VERSION}/build/_deps/logaddexp-src/include",
    ]

    with open(PWD / "deciphon" / "interface.h", "r") as f:
        interface_h = f.read()

    ffibuilder.cdef(interface_h)
    ffibuilder.set_source(
        "deciphon.cffi",
        """
        #include "press/press.h"
        """,
        language="c",
        libraries=["deciphon"],
        library_dirs=[str(d) for d in library_dirs if d.exists()],
        include_dirs=[str(d) for d in include_dirs if d.exists()],
    )
    ffibuilder.compile(verbose=True)
