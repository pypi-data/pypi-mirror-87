"""Utility classes and functions."""
import ctypes
import gc
import inspect

import regex

import numpy_ipps._detail.debug as _debug
import numpy_ipps._detail.libipp as _libipp


cast = _libipp.ffi.cast
new = _libipp.ffi.new


class ndarray:
    """Wrapper class for numpy.ndarray for cffi."""

    __slots__ = (
        "ndarray",
        "cdata",
        "size",
        "shape",
    )

    def __init__(self, array=None):
        if __debug__ and array is not None and not array.flags["C_CONTIGUOUS"]:
            _debug.log_and_raise(
                AssertionError, "Array is not C_CONTIGUOUS.", name=__name__
            )

        self.ndarray = array
        self.cdata = cast(
            "void*",
            0 if array is None else _libipp.ffi.from_buffer(array),
        )
        self.size = cast("int", 0 if array is None else array.size)
        self.shape = new("int[]", (0,) if array is None else array.shape)

    def __repr__(self):
        return "<numpy_ipps.ndarray '{}' 0x{:016x} size {}>".format(
            self.ndarray.dtype, int(cast("int", self.cdata)), int(self.size)
        )


def swap_ndarray(ndarray_lhs, ndarray_rhs):
    """Swap two ndarray wrapper."""
    if __debug__ and int(ndarray_lhs.size) != int(ndarray_rhs.size):
        _debug.log_and_raise(
            AssertionError,
            "Incompatible size arrays {} != {}.".format(
                int(ndarray_lhs.size), int(ndarray_rhs.size)
            ),
            name=__name__,
        )

    ndarray_tmp = ndarray_lhs.ndarray
    cdata_tmp = ndarray_lhs.cdata

    ndarray_lhs.ndarray = ndarray_rhs.ndarray
    ndarray_lhs.cdata = ndarray_rhs.cdata

    ndarray_rhs.ndarray = ndarray_tmp
    ndarray_rhs.cdata = cdata_tmp


class context:
    """Context manager for user-friendly access."""

    __slots__ = (
        "symbols",
        "_gc_reenable",
        "_outer_frame",
        "_outer_frame_ptr",
        "_PyFrame_flag",
    )
    _pattern = regex.compile(
        r".*context\s*\(((?:[^,()]+)(?:,[^,()]+)*)\).*", regex.V1
    )

    def __init__(self, *args):
        self._outer_frame = inspect.currentframe().f_back
        self._outer_frame_ptr = ctypes.py_object(self._outer_frame)
        self._PyFrame_flag = ctypes.c_int(0)
        self.symbols = (
            regex.search(
                context._pattern,
                inspect.getframeinfo(self._outer_frame).code_context[0],
            )
            .group(1)
            .replace(" ", "")
            .split(",")
        )
        self._gc_reenable = gc.isenabled()

    def _LocalsToFast(self):
        ctypes.pythonapi.PyFrame_LocalsToFast(
            self._outer_frame_ptr, self._PyFrame_flag
        )

    def __enter__(self):
        if self._gc_reenable:
            gc.disable()

        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = ndarray(
                self._outer_frame.f_locals[symbol]
            )
            self._LocalsToFast()

    def __exit__(self, *args):
        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = self._outer_frame.f_locals[
                symbol
            ].ndarray
            self._LocalsToFast()

        if self._gc_reenable:
            gc.enable()

        return False
