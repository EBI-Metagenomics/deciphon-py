from math import inf, isinf, isnan, nan

from ._ffi import lib

# from typing import Iterable
# from array import array
# from ._float import array_type_code


# from .build_ext import imm_float

__all__ = [
    "add",
    "invalid",
    "is_valid",
    "is_zero",
    # "normalize",
    "zero",
]


def add(a: float, b: float) -> float:
    return lib.imm_lprob_add(a, b)


def zero() -> float:
    return -inf


def invalid() -> float:
    return nan


def is_zero(x: float):
    return isinf(x) and x < 0


def is_valid(x: float):
    return not isnan(x)


# def normalize(arr: Iterable[float]):
#     pyarr = list(arr)
#     size = len(pyarr)
#     carr = ffi.new(f"{imm_float}[{size}]", pyarr)

#     err: int = lib.imm_lprob_normalize(carr, size)
#     if err != 0:
#         raise RuntimeError("Failed to normalize.")

#     return array(array_type_code, carr)
