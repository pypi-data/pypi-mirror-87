"""Logical Functions."""
import numpy as _numpy

import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies


_logical_policies = numpy_ipps.policies.Policies(
    bytes1=numpy_ipps.policies.TagPolicy.UNSIGNED,
    bytes2=numpy_ipps.policies.TagPolicy.UNSIGNED,
    bytes4=numpy_ipps.policies.TagPolicy.INTEGER_UNSIGNED,
    bytes8=numpy_ipps.policies.TagPolicy.DOWN_UNSIGNED,
)
_shift_candidates = (
    _numpy.uint8,
    _numpy.int16,
    _numpy.uint16,
    _numpy.int32,
)


class And(
    metaclass=_binaries.Binary,
    ipps_backend="And",
    numpy_backend=_numpy.bitwise_and,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """And Function.

    ``dst[n]  <-  src1[n] & src2[n]``
    """

    pass


class _And_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="And_I",
    numpy_backend=_numpy.bitwise_and,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """And_I Function.

    ``src_dst[n]  <-  src_dst[n] & src[n]``
    """

    pass


class AndC(
    metaclass=_binaries.BinaryC,
    ipps_backend="AndC",
    numpy_backend=_numpy.bitwise_and,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """AndC Function.

    ``dst[n]  <-  src[n] & value``
    """

    pass


class AndC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="AndC_I",
    numpy_backend=_numpy.bitwise_and,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """AndC_I Function.

    ``src_dst[n]  <-  src_dst[n] & value``
    """

    pass


class Or(
    metaclass=_binaries.Binary,
    ipps_backend="Or",
    numpy_backend=_numpy.bitwise_or,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """Or Function.

    ``dst[n]  <-  src1[n] | src2[n]``
    """

    pass


class _Or_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Or_I",
    numpy_backend=_numpy.bitwise_or,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """Or_I Function.

    ``src_dst[n]  <-  src_dst[n] | src[n]``
    """

    pass


class OrC(
    metaclass=_binaries.BinaryC,
    ipps_backend="OrC",
    numpy_backend=_numpy.bitwise_or,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """OrC Function.

    ``dst[n]  <-  src[n] | value``
    """

    pass


class OrC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="OrC_I",
    numpy_backend=_numpy.bitwise_or,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """OrC_I Function.

    ``src_dst[n]  <-  src_dst[n] | value``
    """

    pass


class Xor(
    metaclass=_binaries.Binary,
    ipps_backend="Xor",
    numpy_backend=_numpy.bitwise_xor,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """Xor Function.

    ``dst[n]  <-  src1[n] ^ src2[n]``
    """

    pass


class Xor_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Xor_I",
    numpy_backend=_numpy.bitwise_xor,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """Xor_I Function.

    ``src_dst[n]  <-  src_dst[n] ^ src[n]``
    """

    pass


class XorC(
    metaclass=_binaries.BinaryC,
    ipps_backend="XorC",
    numpy_backend=_numpy.bitwise_xor,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """XorC Function.

    ``dst[n]  <-  src[n] ^ value``
    """

    pass


class XorC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="XorC_I",
    numpy_backend=_numpy.bitwise_xor,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """XorC_I Function.

    ``src_dst[n]  <-  src_dst[n] ^ value``
    """

    pass


class LShiftC(
    metaclass=_binaries.BinaryC,
    ipps_backend="LShiftC",
    numpy_backend=_numpy.left_shift,
    candidates=_shift_candidates,
):
    """LShiftC Function."""

    pass


class _LShiftC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="LShiftC_I",
    numpy_backend=_numpy.left_shift,
    candidates=_shift_candidates,
):
    """LShiftC_I Function."""

    pass


class RShiftC(
    metaclass=_binaries.BinaryC,
    ipps_backend="RShiftC",
    numpy_backend=_numpy.right_shift,
    candidates=_shift_candidates,
):
    """RShiftC Function."""

    pass


class RShiftC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="RShiftC_I",
    numpy_backend=_numpy.right_shift,
    candidates=_shift_candidates,
):
    """RShiftC_I Function."""

    pass


class Not(
    metaclass=_unaries.Unary,
    ipps_backend="Not",
    numpy_backend=_numpy.invert,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """Not Function.

    ``dst[n]  <-  ~src[n]``
    """

    pass


class Not_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Not_I",
    numpy_backend=_numpy.invert,
    policies=_logical_policies,
    candidates=numpy_ipps.policies.int_candidates,
):
    """Not_I Function.

    ``src_dst[n]  <-  ~src_dst[n]``
    """

    pass
