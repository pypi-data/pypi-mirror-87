"""Fast Fourier Transform Functions."""
import collections.abc as _abc
import logging as _logging

import numpy as _numpy
import scipy.signal as _signal

import numpy_ipps._detail.debug as _debug
import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps.policies
import numpy_ipps.signal
import numpy_ipps.utils


class _FIR_FFT_R:
    """FIR Function -- FFT Real implementation."""

    __slots__ = (
        "_ipps_fft",
        "_ipps_ifft",
        "_ipps_backend_mul",
        "_ipps_kernel",
        "_ipps_spectrum",
    )
    dtype_candidates = numpy_ipps.policies.no_complex_candidates

    def __init__(self, kernel, order):
        self._ipps_fft = numpy_ipps.FFTFwd(order, kernel.dtype)
        self._ipps_ifft = numpy_ipps.FFTInv(order, kernel.dtype)
        self._ipps_backend_mul = numpy_ipps._detail.dispatch.ipps_function(
            "MulPerm_I",
            (
                "void*",
                "void*",
                "int",
            ),
            kernel.dtype,
        )

        kernel_pad = numpy_ipps.utils.ndarray(
            _numpy.zeros(1 << order, dtype=kernel.dtype)
        )
        kernel_pad.ndarray[: kernel.size] = kernel.flatten()
        self._ipps_kernel = numpy_ipps.utils.ndarray(
            _numpy.empty(1 << order, dtype=kernel.dtype)
        )
        self._ipps_fft(kernel_pad, self._ipps_kernel)

        self._ipps_spectrum = numpy_ipps.utils.ndarray(
            _numpy.empty(1 << order, dtype=kernel.dtype)
        )
        _logging.getLogger(__name__).info(
            "FFT allocations: working buffer {}o.".format(
                2 * kernel.dtype.itemsize * (1 << order)
            )
        )

    def __call__(self, src, dst):
        self._ipps_fft(src, self._ipps_spectrum)
        numpy_ipps.status = self._ipps_backend_mul(
            self._ipps_kernel.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spectrum.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        self._ipps_ifft(self._ipps_spectrum, dst)

    def _numpy_backend(self, src, dst):
        raise NotImplementedError


class _FIR_FFT_C:
    """FIR Function -- FFT Complex implementation."""

    __slots__ = (
        "_ipps_fft",
        "_ipps_ifft",
        "_ipps_mul",
        "_ipps_kernel",
        "_ipps_spectrum_in",
        "_ipps_spectrum_out",
    )
    dtype_candidates = numpy_ipps.policies.complex_candidates
    ipps_accuracies = numpy_ipps.Mul.ipps_accuracies

    def __init__(self, kernel, order, accuracy=None):
        self._ipps_fft = numpy_ipps.FFTFwd(order, kernel.dtype)
        self._ipps_ifft = numpy_ipps.FFTInv(order, kernel.dtype)
        self._ipps_mul = numpy_ipps.Mul(
            dtype=kernel.dtype,
            size=1 << order,
            accuracy=accuracy
            if accuracy in numpy_ipps.Mul.ipps_accuracies
            else None,
        )

        kernel_pad = numpy_ipps.utils.ndarray(
            _numpy.zeros(1 << order, dtype=kernel.dtype)
        )
        kernel_pad.ndarray[: kernel.size] = kernel.flatten()
        self._ipps_kernel = numpy_ipps.utils.ndarray(
            _numpy.empty(1 << order, dtype=kernel.dtype)
        )
        self._ipps_fft(kernel_pad, self._ipps_kernel)

        self._ipps_spectrum_in = numpy_ipps.utils.ndarray(
            _numpy.empty(1 << order, dtype=kernel.dtype)
        )
        self._ipps_spectrum_out = numpy_ipps.utils.ndarray(
            _numpy.empty(1 << order, dtype=kernel.dtype)
        )
        _logging.getLogger(__name__).info(
            "FFT allocations: working buffer {}o.".format(
                2 * kernel.dtype.itemsize * (1 << order)
            )
        )

    def __call__(self, src, dst):
        self._ipps_fft(src, self._ipps_spectrum_in)
        self._ipps_mul(
            self._ipps_kernel, self._ipps_spectrum_in, self._ipps_spectrum_out
        )
        self._ipps_ifft(self._ipps_spectrum_out, dst)

    def _numpy_backend(self, src, dst):
        raise NotImplementedError


class FIR:
    """Fir Function.

    ``dst  <-  convolve( src, kernel )``
    """

    __slots__ = (
        "_ipps_backend",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
        "_ipps_kernel",
        "_ipps_dlySrc",
        "_ipps_dlyDst",
        "_ipps_method",
        "_numpy_method",
        "_numpy_broadcast",
        "_numpy_factor",
        "_numpy_phase",
    )
    dtype_candidates = numpy_ipps.policies.float_candidates

    def __init__(
        self,
        kernel,
        method=numpy_ipps.Method.DIRECT,
        continuous=False,
        rate=None,
    ):
        if (
            __debug__
            and rate is not None
            and not isinstance(rate, _abc.Sequence)
        ):
            _debug.log_and_raise(
                AssertionError,
                "FIR rate should be a pair.",
                name=__name__,
            )

        if rate is not None and rate[0] == 1:
            rate = None

        if rate is None:
            self._numpy_factor, self._numpy_phase = 1, 0
        else:
            if __debug__ and method is numpy_ipps.Method.FFT:
                _debug.log_and_raise(
                    AssertionError,
                    "Method for Multi-rate FIR should be Method.DIRECT.",
                    name=__name__,
                )
            self._numpy_factor, self._numpy_phase = rate

        if method is numpy_ipps.Method.DIRECT:
            self._ipps_method = numpy_ipps.utils.cast("int", 0x00000001)
            self._numpy_method = "direct"
        elif method is numpy_ipps.Method.FFT:
            self._ipps_method = numpy_ipps.utils.cast("int", 0x00000002)
            self._numpy_method = "fft"
        else:
            raise RuntimeError("Unknown method {}".format(method))

        self._ipps_kernel = numpy_ipps.utils.ndarray(kernel)
        self._numpy_broadcast = -kernel.size + 1

        if self._ipps_kernel.ndarray.dtype == _numpy.float32:
            ipps_type = numpy_ipps.utils.cast("int", 13)
        elif self._ipps_kernel.ndarray.dtype == _numpy.float64:
            ipps_type = numpy_ipps.utils.cast("int", 19)
        elif self._ipps_kernel.ndarray.dtype == _numpy.complex64:
            ipps_type = numpy_ipps.utils.cast("int", 14)
        elif self._ipps_kernel.ndarray.dtype == _numpy.complex128:
            ipps_type = numpy_ipps.utils.cast("int", 20)
        else:
            raise RuntimeError(
                "Unknown dtype {}".format(self._ipps_kernel.ndarray.dtype)
            )

        if continuous:
            self._ipps_dlySrc = numpy_ipps.utils.ndarray(
                _numpy.zeros(kernel.size - 1, dtype=kernel.dtype)
            )
            self._ipps_dlyDst = numpy_ipps.utils.ndarray(
                _numpy.empty(kernel.size - 1, dtype=kernel.dtype)
            )
        else:
            self._ipps_dlySrc = numpy_ipps.utils.ndarray()
            self._ipps_dlyDst = numpy_ipps.utils.ndarray()

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fir_getsize = _dispatch.ipps_function(
            "FIRSRGetSize" if rate is None else "FIRMRGetSize",
            ("int",)
            + (tuple() if rate is None else ("int", "int"))
            + ("int", "int*", "int*"),
        )
        ipps_fir_init = _dispatch.ipps_function(
            "FIRSRInit" if rate is None else "FIRMRInit",
            ("void*", "int")
            + (("int",) if rate is None else ("int", "int", "int", "int"))
            + ("void*",),
            self._ipps_kernel.ndarray.dtype,
        )

        if rate is None:
            numpy_ipps.status = ipps_fir_getsize(
                self._ipps_kernel.size,
                ipps_type,
                ipps_spec_size,
                ipps_buffer_size,
            )
        else:
            up_factor = numpy_ipps.utils.cast("int", 1)
            down_factor = numpy_ipps.utils.cast("int", rate[0])
            numpy_ipps.status = ipps_fir_getsize(
                self._ipps_kernel.size,
                up_factor,
                down_factor,
                ipps_type,
                ipps_spec_size,
                ipps_buffer_size,
            )
        _debug.assert_status(
            numpy_ipps.status, message="Get FIR size", name=__name__
        )

        self._ipps_mem_spec = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_spec_size[0], dtype=_numpy.uint8)
        )
        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )
        _logging.getLogger(__name__).info(
            "FFT allocations: specification {}o -- working buffer {}o.".format(
                ipps_spec_size[0], ipps_buffer_size[0]
            )
        )

        if rate is None:
            numpy_ipps.status = ipps_fir_init(
                self._ipps_kernel.cdata,
                self._ipps_kernel.size,
                self._ipps_method,
                self._ipps_mem_spec.cdata,
            )
        else:
            up_phase = numpy_ipps.utils.cast("int", 0)
            down_phase = numpy_ipps.utils.cast("int", rate[1])
            numpy_ipps.status = ipps_fir_init(
                self._ipps_kernel.cdata,
                self._ipps_kernel.size,
                up_factor,
                up_phase,
                down_factor,
                down_phase,
                self._ipps_mem_spec.cdata,
            )
        _debug.assert_status(
            numpy_ipps.status, message="Init FFT", name=__name__
        )

        self._ipps_backend = _dispatch.ipps_function(
            "FIRSR" if rate is None else "FIRMR",
            (
                "void*",
                "void*",
                "int",
                "void*",
                "void*",
                "void*",
                "void*",
            ),
            kernel.dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
            self._ipps_mem_spec.cdata,
            self._ipps_dlySrc.cdata,
            self._ipps_dlyDst.cdata,
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.utils.swap_ndarray(self._ipps_dlySrc, self._ipps_dlyDst)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _signal.convolve(
            src.ndarray,
            self._ipps_kernel.ndarray,
            mode="full",
            method=self._numpy_method,
        )[self._numpy_phase : self._numpy_broadcast : self._numpy_factor]
