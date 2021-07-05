# import ctypes
# from .build_ext import imm_float
# import sys

# __all__ = ["array_type_code"]

# array_type_code = "d"


# def py_float_size() -> int:
#     if sys.float_info.mant_dig >= 52:
#         return 8
#     return 4


# imm_float_size = 0
# if f"{imm_float}" == "float":
#     imm_float_size = ctypes.sizeof(ctypes.c_float)
# elif f"{imm_float}" == "double":
#     imm_float_size = ctypes.sizeof(ctypes.c_double)
# else:
#     raise RuntimeError(f"Invalid imm_float: {imm_float}.")

# if imm_float_size != py_float_size():
#     raise RuntimeError(f"Invalid imm_float size ({imm_float_size}).")

# if imm_float_size == 8:
#     array_type_code = "d"
# else:
#     array_type_code = "f"
