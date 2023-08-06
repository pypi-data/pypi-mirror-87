import ctypes
import enum
import inspect

import numpy
import pytest
import regex

import numpy_ipps._detail.dispatch
import numpy_ipps._detail.libipp
import numpy_ipps.initialization
import numpy_ipps.logical
import numpy_ipps.utils


orders = (8, int(numpy.ceil(numpy.log2(numpy_ipps.support.L1))))


class ipps_enum(enum.IntEnum):
    ndarray = 0
    cdata = 1
    size = 2
    shape = 3


def numpy_ipps_dict(array):
    return {
        "ndarray": array,
        "cdata": numpy_ipps._detail.libipp.ffi.from_buffer(array),
        "size": numpy_ipps._detail.libipp.ffi.cast("int", array.size),
        "shape": numpy_ipps._detail.libipp.ffi.new("int[]", array.shape),
    }


def indirect_dict(lhs, rhs):
    lhs["cdata"]
    lhs["size"]
    lhs["shape"]
    rhs["cdata"]
    rhs["size"]
    lhs["shape"]


@pytest.mark.parametrize("order", orders)
def test_indirect_dict(benchmark, order):
    lhs = numpy_ipps_dict(numpy.empty(1 << order))
    rhs = numpy_ipps_dict(numpy.empty(1 << order))
    benchmark(indirect_dict, lhs, rhs)


def numpy_ipps_list(array):
    return [
        array,
        numpy_ipps._detail.libipp.ffi.from_buffer(array),
        numpy_ipps._detail.libipp.ffi.cast("int", array.size),
        numpy_ipps._detail.libipp.ffi.new("int[]", array.shape),
    ]


def indirect_list_tuple(lhs, rhs):
    lhs[ipps_enum.cdata]
    lhs[ipps_enum.size]
    lhs[ipps_enum.shape]
    rhs[ipps_enum.cdata]
    rhs[ipps_enum.size]
    rhs[ipps_enum.shape]


@pytest.mark.parametrize("order", orders)
def test_indirect_list(benchmark, order):
    lhs = numpy_ipps_list(numpy.empty(1 << order))
    rhs = numpy_ipps_list(numpy.empty(1 << order))
    benchmark(indirect_list_tuple, lhs, rhs)


def numpy_ipps_tuple(array):
    return (
        array,
        numpy_ipps._detail.libipp.ffi.from_buffer(array),
        numpy_ipps._detail.libipp.ffi.cast("int", array.size),
        numpy_ipps._detail.libipp.ffi.new("int[]", array.shape),
    )


@pytest.mark.parametrize("order", orders)
def test_indirect_tuple(benchmark, order):
    lhs = numpy_ipps_tuple(numpy.empty(1 << order))
    rhs = numpy_ipps_tuple(numpy.empty(1 << order))
    benchmark(indirect_list_tuple, lhs, rhs)


class indirection_class:
    def __init__(self, array):
        self.ndarray = array
        self.cdata = numpy_ipps._detail.libipp.ffi.from_buffer(array)
        self.size = numpy_ipps._detail.libipp.ffi.cast("int", array.size)
        self.shape = numpy_ipps._detail.libipp.ffi.new("int[]", array.shape)


def indirect_class(lhs, rhs):
    lhs.cdata
    lhs.size
    lhs.shape
    rhs.cdata
    rhs.size
    rhs.shape


@pytest.mark.parametrize("order", orders)
def test_indirect_class(benchmark, order):
    lhs = indirection_class(numpy.empty(1 << order))
    rhs = indirection_class(numpy.empty(1 << order))
    benchmark(indirect_class, lhs, rhs)


class indirection_class_slots:
    __slots__ = (
        "ndarray",
        "cdata",
        "size",
        "shape",
    )

    def __init__(self, array):
        self.ndarray = array
        self.cdata = numpy_ipps._detail.libipp.ffi.from_buffer(array)
        self.size = numpy_ipps._detail.libipp.ffi.cast("int", array.size)
        self.shape = numpy_ipps._detail.libipp.ffi.new("int[]", array.shape)


@pytest.mark.parametrize("order", orders)
def test_indirect_class_slots(benchmark, order):
    lhs = indirection_class_slots(numpy.empty(1 << order))
    rhs = indirection_class_slots(numpy.empty(1 << order))
    benchmark(indirect_class, lhs, rhs)


class AssignNoSlots:
    def __init__(self, dtype=float):
        self.callback = numpy_ipps._detail.dispatch.ipps_function(
            "Copy",
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.initialization._init_policies,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self.callback(
            src.cdata,
            dst.cdata,
            dst.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)


class AssignSlots:
    __slots__ = ("callback",)

    def __init__(self, dtype=float):
        self.callback = numpy_ipps._detail.dispatch.ipps_function(
            "Copy",
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.initialization._init_policies,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self.callback(
            src.cdata,
            dst.cdata,
            dst.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize(
    "dtype", [numpy.int32, numpy.int64, numpy.float32, numpy.float64]
)
def test_ipps_assign_no_slots(benchmark, order, dtype):
    assign = AssignNoSlots(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(assign, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize(
    "dtype", [numpy.int32, numpy.int64, numpy.float32, numpy.float64]
)
def test_ipps_assign_slots(benchmark, order, dtype):
    assign = AssignSlots(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(assign, src, dst)


class context_ws:
    __slots__ = (
        "symbols",
        "_outer_frame",
        "_outer_frame_ptr",
        "_PyFrame_flag",
    )
    _pattern = regex.compile(
        r".*context_ws\s*\(((?:[^,()]+)(?:,[^,()]+)*)\).*", regex.V1
    )

    def __init__(self, *args):
        self._outer_frame = inspect.currentframe().f_back
        self._outer_frame_ptr = ctypes.py_object(self._outer_frame)
        self._PyFrame_flag = ctypes.c_int(0)
        self.symbols = (
            regex.search(
                context_ws._pattern,
                inspect.getframeinfo(self._outer_frame).code_context[0],
            )
            .group(1)
            .replace(" ", "")
            .split(",")
        )

    def _LocalsToFast(self):
        ctypes.pythonapi.PyFrame_LocalsToFast(
            self._outer_frame_ptr, self._PyFrame_flag
        )

    def __enter__(self):
        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = numpy_ipps.utils.ndarray(
                self._outer_frame.f_locals[symbol]
            )
            self._LocalsToFast()

    def __exit__(self, *args):
        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = self._outer_frame.f_locals[
                symbol
            ].ndarray
            self._LocalsToFast()
        return False


class context_ns:
    _pattern = regex.compile(
        r".*context_ns\s*\(((?:[^,()]+)(?:,[^,()]+)*)\).*", regex.V1
    )

    def __init__(self, *args):
        self._outer_frame = inspect.currentframe().f_back
        self._outer_frame_ptr = ctypes.py_object(self._outer_frame)
        self._PyFrame_flag = ctypes.c_int(0)
        self.symbols = (
            regex.search(
                context_ns._pattern,
                inspect.getframeinfo(self._outer_frame).code_context[0],
            )
            .group(1)
            .replace(" ", "")
            .split(",")
        )

    def _LocalsToFast(self):
        ctypes.pythonapi.PyFrame_LocalsToFast(
            self._outer_frame_ptr, self._PyFrame_flag
        )

    def __enter__(self):
        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = numpy_ipps.utils.ndarray(
                self._outer_frame.f_locals[symbol]
            )
            self._LocalsToFast()

    def __exit__(self, *args):
        for symbol in self.symbols:
            self._outer_frame.f_locals[symbol] = self._outer_frame.f_locals[
                symbol
            ].ndarray
            self._LocalsToFast()
        return False


def call_context_ns(assign, src, dst):
    with context_ns(src, dst):
        assign(src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize(
    "dtype", [numpy.int32, numpy.int64, numpy.float32, numpy.float64]
)
def test_context_ns(benchmark, order, dtype):
    assign = numpy_ipps.initialization.Assign(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    benchmark(call_context_ns, assign, src, dst)


def call_context_ws(assign, src, dst):
    with context_ws(src, dst):
        assign(src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize(
    "dtype", [numpy.int32, numpy.int64, numpy.float32, numpy.float64]
)
def test_context_ws(benchmark, order, dtype):
    assign = numpy_ipps.initialization.Assign(dtype=dtype)
    src = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    benchmark(call_context_ws, assign, src, dst)


class AndBare:
    __slots__ = ("callback",)

    def __init__(self, dtype=numpy.uint32):
        self.callback = numpy_ipps._detail.dispatch.ipps_function(
            "Add",
            (
                "void*",
                "void*",
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.logical._logical_policies,
        )

    def __call__(self, src1, src2, dst):
        numpy_ipps.status = self.callback(
            src1.cdata,
            src2.cdata,
            dst.cdata,
            dst.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)


class BinaryBase:
    __slots__ = "callback"

    def __init__(self, ipps_backend, dtype=numpy.uint32):
        self.callback = numpy_ipps._detail.dispatch.ipps_function(
            ipps_backend,
            (
                "void*",
                "void*",
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.logical._logical_policies,
        )

    def __call__(self, src1, src2, dst):
        numpy_ipps.status = self.callback(
            src1.cdata,
            src2.cdata,
            dst.cdata,
            dst.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)


class AndInherit(BinaryBase):
    __slots__ = tuple()

    def __init__(self, *args, **kwargs):
        super().__init__("And", *args, **kwargs)


class BinaryMeta(type):
    def __new__(mcs, name, bases, attrs, ipps_backend=None):
        attrs["__slots__"] = ("callback",)
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend = ipps_backend

        def cls__call__(self, src1, src2, dst):
            numpy_ipps.status = self.callback(
                src1.cdata,
                src2.cdata,
                dst.cdata,
                dst.size,
            )
            assert (
                numpy_ipps.status == 0
            ), "DEBUG: Bad Intel IPP Signal status {}".format(
                numpy_ipps.status
            )

        cls.__call__ = cls__call__

        return cls

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)

    def __call__(cls, dtype=numpy.uint32):
        self = super().__call__()

        self.callback = numpy_ipps._detail.dispatch.ipps_function(
            cls._ipps_backend,
            (
                "void*",
                "void*",
                "void*",
                "int",
            ),
            dtype,
            policies=numpy_ipps.logical._logical_policies,
        )

        return self


class AndMeta(metaclass=BinaryMeta, ipps_backend="And"):
    pass


@pytest.mark.parametrize("order", orders)
def test_call_bare(benchmark, order):
    and_bare = AndBare(dtype=numpy.uint32)
    src1 = numpy.empty(1 << order, dtype=numpy.uint32)
    src2 = numpy.empty(1 << order, dtype=numpy.uint32)
    dst = numpy.empty(1 << order, dtype=numpy.uint32)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(and_bare, src1, src2, dst)


@pytest.mark.parametrize("order", orders)
def test_call_inherit(benchmark, order):
    and_inherit = AndInherit(dtype=numpy.uint32)
    src1 = numpy.empty(1 << order, dtype=numpy.uint32)
    src2 = numpy.empty(1 << order, dtype=numpy.uint32)
    dst = numpy.empty(1 << order, dtype=numpy.uint32)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(and_inherit, src1, src2, dst)


@pytest.mark.parametrize("order", orders)
def test_call_meta(benchmark, order):
    and_meta = AndMeta(dtype=numpy.uint32)
    src1 = numpy.empty(1 << order, dtype=numpy.uint32)
    src2 = numpy.empty(1 << order, dtype=numpy.uint32)
    dst = numpy.empty(1 << order, dtype=numpy.uint32)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(and_meta, src1, src2, dst)


class IPPSFirFFT:
    __slots__ = (
        "_ipps_backend_fft",
        "_ipps_backend_ifft",
        "_ipps_backend_mul",
        "_ipps_spec",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
        "_ipps_kernel",
        "_ipps_spectrum",
    )

    def __init__(self, kernel, order, dtype=numpy.complex128):
        ipps_flag = numpy_ipps.utils.cast("int", 2)

        self._ipps_spec = numpy_ipps.utils.new("void**")

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_spec_buffer_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fft_getsize = numpy_ipps._detail.dispatch.ipps_function(
            "FFTGetSize-C",
            (
                "int",
                "int",
                "IppHintAlgorithm",
                "int*",
                "int*",
                "int*",
            ),
            dtype,
        )
        ipps_fft_init = numpy_ipps._detail.dispatch.ipps_function(
            "FFTInit-C",
            (
                "void**",
                "int",
                "int",
                "IppHintAlgorithm",
                "void*",
                "void*",
            ),
            dtype,
        )

        numpy_ipps.status = ipps_fft_getsize(
            order,
            ipps_flag,
            numpy_ipps._detail.libipp.ffi.typeof("IppHintAlgorithm").relements[
                "ippAlgHintNone"
            ],
            ipps_spec_size,
            ipps_spec_buffer_size,
            ipps_buffer_size,
        )

        self._ipps_mem_spec = numpy_ipps.utils.ndarray(
            numpy.empty(ipps_spec_size[0], dtype=numpy.uint8)
        )
        ipps_mem_init = numpy_ipps.utils.ndarray(
            numpy.empty(ipps_spec_buffer_size[0], dtype=numpy.uint8)
        )
        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            numpy.empty(ipps_buffer_size[0], dtype=numpy.uint8)
        )

        numpy_ipps.status = ipps_fft_init(
            self._ipps_spec,
            order,
            ipps_flag,
            numpy_ipps._detail.libipp.ffi.typeof("IppHintAlgorithm").relements[
                "ippAlgHintNone"
            ],
            self._ipps_mem_spec.cdata,
            ipps_mem_init.cdata,
        )

        self._ipps_backend_fft = numpy_ipps._detail.dispatch.ipps_function(
            "FFTFwd-CToC",
            (
                "void*",
                "void*",
                "void*",
                "void*",
            ),
            dtype,
        )
        self._ipps_backend_ifft = numpy_ipps._detail.dispatch.ipps_function(
            "FFTInv-CToC",
            (
                "void*",
                "void*",
                "void*",
                "void*",
            ),
            dtype,
        )

        self._ipps_backend_mul = numpy_ipps._detail.dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                "Mul",
                dtype,
                numpy_ipps.policies.Accuracy.LEVEL_3,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )

        kernel_pad = numpy_ipps.utils.ndarray(
            numpy.zeros(1 << order, dtype=dtype)
        )
        kernel_pad.ndarray[: kernel.size] = kernel.flatten()
        self._ipps_kernel = numpy_ipps.utils.ndarray(
            numpy.empty(1 << order, dtype=dtype)
        )
        numpy_ipps.status = self._ipps_backend_fft(
            kernel_pad.cdata,
            self._ipps_kernel.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )

        self._ipps_spectrum = numpy_ipps.utils.ndarray(
            numpy.empty(1 << order, dtype=dtype)
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend_fft(
            src.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_mul(
            self._ipps_kernel.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spectrum.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_ifft(
            self._ipps_spectrum.cdata,
            dst.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)


@pytest.mark.parametrize("order", orders)
def test_ipps_FirFFT(benchmark, order):
    fir_fft = IPPSFirFFT(
        (1 + numpy.random.rand(1 << 4)).astype(numpy.complex64),
        8,
        dtype=numpy.complex64,
    )
    src = (1 + numpy.random.rand(1 << order)).astype(numpy.complex64)
    dst = numpy.empty(1 << order, dtype=numpy.complex64)

    with numpy_ipps.utils.context(src, dst):
        benchmark(fir_fft, src, dst)


class IPPSFirFir:
    __slots__ = (
        "_ipps_backend",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
        "_ipps_null",
    )

    def __init__(self, kernel, method, dtype=numpy.complex128):
        ipps_flag = numpy_ipps.utils.cast("int", method)
        if dtype == numpy.float32:
            ipps_type = numpy_ipps.utils.cast("int", 13)
        elif dtype == numpy.float64:
            ipps_type = numpy_ipps.utils.cast("int", 19)
        elif dtype == numpy.complex64:
            ipps_type = numpy_ipps.utils.cast("int", 14)
        elif dtype == numpy.complex128:
            ipps_type = numpy_ipps.utils.cast("int", 20)
        self._ipps_null = numpy_ipps.utils.cast("void*", 0)

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fir_getsize = numpy_ipps._detail.dispatch.ipps_function(
            "FIRSRGetSize",
            (
                "int",
                "int",
                "int*",
                "int*",
            ),
        )
        ipps_fir_init = numpy_ipps._detail.dispatch.ipps_function(
            "FIRSRInit",
            (
                "void*",
                "int",
                "int",
                "void*",
            ),
            dtype,
        )

        numpy_ipps.status = ipps_fir_getsize(
            kernel.size,
            ipps_type,
            ipps_spec_size,
            ipps_buffer_size,
        )

        self._ipps_mem_spec = numpy_ipps.utils.ndarray(
            numpy.empty(ipps_spec_size[0], dtype=numpy.uint8)
        )
        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            numpy.empty(ipps_buffer_size[0], dtype=numpy.uint8)
        )

        with numpy_ipps.utils.context(kernel):
            numpy_ipps.status = ipps_fir_init(
                kernel.cdata,
                kernel.size,
                ipps_flag,
                self._ipps_mem_spec.cdata,
            )

        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            "FIRSR",
            (
                "void*",
                "void*",
                "int",
                "void*",
                "void*",
                "void*",
                "void*",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
            self._ipps_mem_spec.cdata,
            self._ipps_null,
            self._ipps_null,
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("method", (0x00000001, 0x00000002))
def test_ipps_FirFir(benchmark, order, method):
    fir_fir = IPPSFirFir(
        (1 + numpy.random.rand(1 << 4)).astype(numpy.complex64),
        method=method,
        dtype=numpy.complex64,
    )
    src = (1 + numpy.random.rand(1 << order)).astype(numpy.complex64)
    dst = numpy.empty(1 << order, dtype=numpy.complex64)

    with numpy_ipps.utils.context(src, dst):
        benchmark(fir_fir, src, dst)
