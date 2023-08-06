"""Intel IPP Signal constants."""
import numpy_ipps.utils


class float32:
    """float32 constants."""

    __slots__ = ()

    minabs = numpy_ipps.utils.cast("float", 1.175494351e-38)


class float64:
    """float64 constants."""

    __slots__ = ()

    minabs = numpy_ipps.utils.cast("double", 2.2250738585072014e-308)
