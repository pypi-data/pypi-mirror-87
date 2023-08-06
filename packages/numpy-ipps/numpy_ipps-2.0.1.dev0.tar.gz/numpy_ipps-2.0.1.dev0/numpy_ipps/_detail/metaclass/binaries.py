import numpy

import numpy_ipps._detail.debug
import numpy_ipps._detail.dispatch
import numpy_ipps._detail.metaclass.selector
import numpy_ipps.policies
import numpy_ipps.utils


class Binary(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps.policies.keep_all,
        candidates=numpy_ipps.policies.default_candidates,
        numpy_swap=False,
        force_numpy=False,
        signed_len=False,
    ):
        attrs["__slots__"] = (
            "_ipps_backend",
            "_ipps_callback_64",
            "_ipps_callback_Sfs",
            "_ipps_scale",
        )
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls.dtype_candidates = candidates
        cls._ipps_kind = numpy_ipps._detail.metaclass.selector.Kind.BINARY
        cls._ipps_policies = policies
        cls._ipps_signed_len = signed_len

        def cls_ipps_backend_64(
            self, src1_cdata, src2_cdata, dst_cdata, dst_size
        ):
            return self._ipps_callback_64(
                src1_cdata, src2_cdata, dst_cdata, 2 * int(dst_size)
            )

        cls._ipps_backend_64 = cls_ipps_backend_64

        def cls_ipps_backend_Sfs(
            self, src1_cdata, src2_cdata, dst_cdata, dst_size
        ):
            return self._ipps_callback_Sfs(
                src1_cdata, src2_cdata, dst_cdata, dst_size, self._ipps_scale
            )

        cls._ipps_backend_Sfs = cls_ipps_backend_Sfs

        if numpy_swap:

            def cls_numpy_backend(self, src1, src2, dst):
                numpy_backend(
                    src2.ndarray, src1.ndarray, dst.ndarray, casting="unsafe"
                )

        else:

            def cls_numpy_backend(self, src1, src2, dst):
                numpy_backend(
                    src1.ndarray, src2.ndarray, dst.ndarray, casting="unsafe"
                )

        cls._numpy_backend = cls_numpy_backend

        if force_numpy:
            if numpy_swap:

                def cls__call__(self, src1, src2, dst):
                    assert (
                        src1.ndarray.size == dst.ndarray.size
                    ), "src and dst size not compatible."
                    assert (
                        src2.ndarray.size == dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_backend(
                        src2.ndarray,
                        src1.ndarray,
                        dst.ndarray,
                        casting="unsafe",
                    )

            else:

                def cls__call__(self, src1, src2, dst):
                    assert (
                        src1.ndarray.size == dst.ndarray.size
                    ), "src and dst size not compatible."
                    assert (
                        src2.ndarray.size == dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_backend(
                        src1.ndarray,
                        src2.ndarray,
                        dst.ndarray,
                        casting="unsafe",
                    )

        else:

            def cls__call__(self, src1, src2, dst):
                assert (
                    src1.ndarray.size == dst.ndarray.size
                ), "src and dst size not compatible."
                assert (
                    src2.ndarray.size == dst.ndarray.size
                ), "src and dst size not compatible."

                numpy_ipps.status = self._ipps_backend(
                    src1.cdata, src2.cdata, dst.cdata, dst.size
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

    def __call__(cls, dtype, size=None):
        if numpy.dtype(dtype) not in cls.dtype_candidates:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "Numpy IPPS Function {} doesn't accept [ dtype : {} ].".format(
                    cls, dtype
                ),
            )

        self = super().__call__()

        if (
            cls._ipps_policies.bytes8[0] in numpy_ipps.policies.down_tags
            and numpy.dtype(dtype).itemsize == 8
        ):
            self._ipps_callback_64 = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                (
                    "void*",
                    "void*",
                    "void*",
                    "signed int" if cls._ipps_signed_len else "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )
            self._ipps_backend = self._ipps_backend_64
        elif numpy_ipps._detail.dispatch.is_scale(
            dtype, policies=cls._ipps_policies
        ):
            self._ipps_scale = numpy_ipps.utils.cast("int", 0)
            self._ipps_callback_Sfs = (
                numpy_ipps._detail.dispatch.ipps_function(
                    cls._ipps_backend_name,
                    (
                        "void*",
                        "void*",
                        "void*",
                        "signed int" if cls._ipps_signed_len else "int",
                    ),
                    dtype,
                    policies=cls._ipps_policies,
                )
            )
            self._ipps_backend = self._ipps_backend_Sfs
        else:
            self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                (
                    "void*",
                    "void*",
                    "void*",
                    "signed int" if cls._ipps_signed_len else "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )

        return self


class Binary_I(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps.policies.keep_all,
        candidates=numpy_ipps.policies.default_candidates,
        numpy_swap=False,
        force_numpy=False,
        signed_len=False,
    ):
        attrs["__slots__"] = (
            "_ipps_backend",
            "_ipps_callback_64",
            "_ipps_callback_Sfs",
            "_ipps_scale",
        )
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls.dtype_candidates = candidates
        cls._ipps_kind = numpy_ipps._detail.metaclass.selector.Kind.BINARY_I
        cls._ipps_policies = policies
        cls._ipps_signed_len = signed_len

        def cls_ipps_backend_64(self, src_cdata, src_dst_cdata, src_dst_size):
            return self._ipps_callback_64(
                src_cdata, src_dst_cdata, 2 * int(src_dst_size)
            )

        cls._ipps_backend_64 = cls_ipps_backend_64

        def cls_ipps_backend_Sfs(self, src_cdata, src_dst_cdata, src_dst_size):
            return self._ipps_callback_Sfs(
                src_cdata, src_dst_cdata, src_dst_size, self._ipps_scale
            )

        cls._ipps_backend_Sfs = cls_ipps_backend_Sfs

        if numpy_swap:

            def cls_numpy_backend(self, src, src_dst):
                assert (
                    src.ndarray.size == src_dst.ndarray.size
                ), "src and dst size not compatible."

                numpy_backend(
                    src_dst.ndarray,
                    src.ndarray,
                    src_dst.ndarray,
                    casting="unsafe",
                )

        else:

            def cls_numpy_backend(self, src, src_dst):
                assert (
                    src.ndarray.size == src_dst.ndarray.size
                ), "src and dst size not compatible."

                numpy_backend(
                    src.ndarray,
                    src_dst.ndarray,
                    src_dst.ndarray,
                    casting="unsafe",
                )

        cls._numpy_backend = cls_numpy_backend

        if force_numpy:
            if numpy_swap:

                def cls__call__(self, src, src_dst):
                    assert (
                        src.ndarray.size == src_dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_backend(
                        src_dst.ndarray,
                        src.ndarray,
                        src_dst.ndarray,
                        casting="unsafe",
                    )

            else:

                def cls__call__(self, src, src_dst):
                    assert (
                        src.ndarray.size == src_dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_backend(
                        src.ndarray,
                        src_dst.ndarray,
                        src_dst.ndarray,
                        casting="unsafe",
                    )

        else:

            def cls__call__(self, src, src_dst):
                assert (
                    src.ndarray.size == src_dst.ndarray.size
                ), "src and dst size not compatible."

                numpy_ipps.status = self._ipps_backend(
                    src.cdata, src_dst.cdata, src_dst.size
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

    def __call__(cls, dtype, size=None):
        if numpy.dtype(dtype) not in cls.dtype_candidates:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "Numpy IPPS Function {} doesn't accept [ dtype : {} ].".format(
                    cls, dtype
                ),
            )

        self = super().__call__()

        if (
            cls._ipps_policies.bytes8[0] in numpy_ipps.policies.down_tags
            and numpy.dtype(dtype).itemsize == 8
        ):
            self._ipps_callback_64 = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                (
                    "void*",
                    "void*",
                    "signed int" if cls._ipps_signed_len else "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )
            self._ipps_backend = self._ipps_backend_64
        elif numpy_ipps._detail.dispatch.is_scale(
            dtype, policies=cls._ipps_policies
        ):
            self._ipps_scale = numpy_ipps.utils.cast("int", 0)
            self._ipps_callback_Sfs = (
                numpy_ipps._detail.dispatch.ipps_function(
                    cls._ipps_backend_name,
                    (
                        "void*",
                        "void*",
                        "signed int" if cls._ipps_signed_len else "int",
                    ),
                    dtype,
                    policies=cls._ipps_policies,
                )
            )
            self._ipps_backend = self._ipps_backend_Sfs
        else:
            self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                (
                    "void*",
                    "void*",
                    "signed int" if cls._ipps_signed_len else "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )

        return self


class BinaryC(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps.policies.keep_all,
        candidates=numpy_ipps.policies.default_candidates,
        numpy_swap=False,
        force_numpy=False,
        signed_len=False,
    ):
        attrs["__slots__"] = (
            "_ipps_backend",
            "_ipps_callback_64",
            "_ipps_callback_Sfs",
            "_ipps_scale",
        )
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls.dtype_candidates = candidates
        cls._ipps_kind = numpy_ipps._detail.metaclass.selector.Kind.UNARY
        cls._ipps_policies = policies
        cls._ipps_signed_len = signed_len

        def cls_ipps_backend_64(self, src_cdata, value, dst_cdata, dst_size):
            return self._ipps_callback_64(
                src_cdata, value, dst_cdata, 2 * int(dst_size)
            )

        cls._ipps_backend_64 = cls_ipps_backend_64

        def cls_ipps_backend_Sfs(self, src_cdata, value, dst_cdata, dst_size):
            return self._ipps_callback_Sfs(
                src_cdata, value, dst_cdata, dst_size, self._ipps_scale
            )

        cls._ipps_backend_Sfs = cls_ipps_backend_Sfs

        if numpy_swap:

            def cls_numpy_backend(self, src, value, dst):
                numpy_backend(
                    value, src.ndarray, dst.ndarray, casting="unsafe"
                )

        else:

            def cls_numpy_backend(self, src, value, dst):
                numpy_backend(
                    src.ndarray, value, dst.ndarray, casting="unsafe"
                )

        cls._numpy_backend = cls_numpy_backend

        if force_numpy:
            if numpy_swap:

                def cls__call__(self, src, value, dst):
                    assert (
                        src.ndarray.size == dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_backend(
                        value, src.ndarray, dst.ndarray, casting="unsafe"
                    )

            else:

                def cls__call__(self, src, value, dst):
                    assert (
                        src.ndarray.size == dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_backend(
                        src.ndarray, value, dst.ndarray, casting="unsafe"
                    )

        else:

            def cls__call__(self, src, value, dst):
                assert (
                    src.ndarray.size == dst.ndarray.size
                ), "src and dst size not compatible."

                numpy_ipps.status = self._ipps_backend(
                    src.cdata, value, dst.cdata, dst.size
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

    def __call__(cls, dtype, size=None):
        if numpy.dtype(dtype) not in cls.dtype_candidates:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "Numpy IPPS Function {} doesn't accept [ dtype : {} ].".format(
                    cls, dtype
                ),
            )

        self = super().__call__()

        if (
            cls._ipps_policies.bytes8[0] in numpy_ipps.policies.down_tags
            and numpy.dtype(dtype).itemsize == 8
        ):
            self._ipps_callback_64 = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                (
                    "void*",
                    numpy_ipps._detail.dispatch.as_ctype_str(
                        dtype, policies=cls._ipps_policies
                    ),
                    "void*",
                    "signed int" if cls._ipps_signed_len else "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )
            self._ipps_backend = self._ipps_backend_64
        elif numpy_ipps._detail.dispatch.is_scale(
            dtype, policies=cls._ipps_policies
        ):
            self._ipps_scale = numpy_ipps.utils.cast("int", 0)
            self._ipps_callback_Sfs = (
                numpy_ipps._detail.dispatch.ipps_function(
                    cls._ipps_backend_name,
                    (
                        "void*",
                        numpy_ipps._detail.dispatch.as_ctype_str(
                            dtype, policies=cls._ipps_policies
                        ),
                        "void*",
                        "signed int" if cls._ipps_signed_len else "int",
                    ),
                    dtype,
                    policies=cls._ipps_policies,
                )
            )
            self._ipps_backend = self._ipps_backend_Sfs
        else:
            self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                (
                    "void*",
                    numpy_ipps._detail.dispatch.as_ctype_str(
                        dtype, policies=cls._ipps_policies
                    ),
                    "void*",
                    "signed int" if cls._ipps_signed_len else "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )

        return self


class BinaryC_I(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps.policies.keep_all,
        candidates=numpy_ipps.policies.default_candidates,
        numpy_swap=False,
        force_numpy=False,
        signed_len=False,
    ):
        attrs["__slots__"] = (
            "_ipps_backend",
            "_ipps_callback_64",
            "_ipps_callback_Sfs",
            "_ipps_scale",
        )
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls.dtype_candidates = candidates
        cls._ipps_kind = numpy_ipps._detail.metaclass.selector.Kind.UNARY_I
        cls._ipps_policies = policies
        cls._ipps_signed_len = signed_len

        def cls_ipps_backend_64(self, value, src_dst_cdata, src_dst_size):
            return self._ipps_callback_64(
                value, src_dst_cdata, 2 * int(src_dst_size)
            )

        cls._ipps_backend_64 = cls_ipps_backend_64

        def cls_ipps_backend_Sfs(self, value, src_dst_cdata, src_dst_size):
            return self._ipps_callback_Sfs(
                value, src_dst_cdata, src_dst_size, self._ipps_scale
            )

        cls._ipps_backend_Sfs = cls_ipps_backend_Sfs

        if numpy_swap:

            def cls_numpy_backend(self, value, src_dst):
                numpy_backend(
                    value, src_dst.ndarray, src_dst.ndarray, casting="unsafe"
                )

        else:

            def cls_numpy_backend(self, value, src_dst):
                numpy_backend(
                    src_dst.ndarray, value, src_dst.ndarray, casting="unsafe"
                )

        cls._numpy_backend = cls_numpy_backend

        if force_numpy:
            if numpy_swap:

                def cls__call__(self, value, src_dst):
                    numpy_backend(
                        value,
                        src_dst.ndarray,
                        src_dst.ndarray,
                        casting="unsafe",
                    )

            else:

                def cls__call__(self, value, src_dst):
                    numpy_backend(
                        src_dst.ndarray,
                        value,
                        src_dst.ndarray,
                        casting="unsafe",
                    )

        else:

            def cls__call__(self, value, src_dst):
                numpy_ipps.status = self._ipps_backend(
                    value, src_dst.cdata, src_dst.size
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

    def __call__(cls, dtype, size=None):
        if numpy.dtype(dtype) not in cls.dtype_candidates:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "Numpy IPPS Function {} doesn't accept [ dtype : {} ].".format(
                    cls, dtype
                ),
            )

        self = super().__call__()

        if (
            cls._ipps_policies.bytes8[0] in numpy_ipps.policies.down_tags
            and numpy.dtype(dtype).itemsize == 8
        ):
            self._ipps_callback_64 = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                (
                    numpy_ipps._detail.dispatch.as_ctype_str(
                        dtype, policies=cls._ipps_policies
                    ),
                    "void*",
                    "signed int" if cls._ipps_signed_len else "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )
            self._ipps_backend = self._ipps_backend_64
        elif numpy_ipps._detail.dispatch.is_scale(
            dtype, policies=cls._ipps_policies
        ):
            self._ipps_scale = numpy_ipps.utils.cast("int", 0)
            self._ipps_callback_Sfs = (
                numpy_ipps._detail.dispatch.ipps_function(
                    cls._ipps_backend_name,
                    (
                        numpy_ipps._detail.dispatch.as_ctype_str(
                            dtype, policies=cls._ipps_policies
                        ),
                        "void*",
                        "signed int" if cls._ipps_signed_len else "int",
                    ),
                    dtype,
                    policies=cls._ipps_policies,
                )
            )
            self._ipps_backend = self._ipps_backend_Sfs
        else:
            self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                (
                    numpy_ipps._detail.dispatch.as_ctype_str(
                        dtype, policies=cls._ipps_policies
                    ),
                    "void*",
                    "signed int" if cls._ipps_signed_len else "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )

        return self


class BinaryAccuracy(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps.policies.keep_all,
        candidates=numpy_ipps.policies.float_candidates,
        accuracies=numpy_ipps.policies.default_accuracies,
        numpy_swap=False,
        force_numpy=False,
    ):
        attrs["__slots__"] = ("_ipps_backend",)
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls.dtype_candidates = candidates
        cls.ipps_accuracies = accuracies
        cls._ipps_kind = numpy_ipps._detail.metaclass.selector.Kind.BINARY
        cls._ipps_policies = policies

        if numpy_swap:

            def cls_numpy_backend(self, src1, src2, dst):
                numpy_backend(
                    src2.ndarray, src1.ndarray, dst.ndarray, casting="unsafe"
                )

        else:

            def cls_numpy_backend(self, src1, src2, dst):
                numpy_backend(
                    src1.ndarray, src2.ndarray, dst.ndarray, casting="unsafe"
                )

        cls._numpy_backend = cls_numpy_backend

        if force_numpy:
            if numpy_swap:

                def cls__call__(self, src1, src2, dst):
                    assert (
                        src1.ndarray.size == dst.ndarray.size
                    ), "src and dst size not compatible."
                    assert (
                        src2.ndarray.size == dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_backend(
                        src2.ndarray,
                        src1.ndarray,
                        dst.ndarray,
                        casting="unsafe",
                    )

            else:

                def cls__call__(self, src1, src2, dst):
                    assert (
                        src1.ndarray.size == dst.ndarray.size
                    ), "src and dst size not compatible."
                    assert (
                        src2.ndarray.size == dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_backend(
                        src1.ndarray,
                        src2.ndarray,
                        dst.ndarray,
                        casting="unsafe",
                    )

        else:

            def cls__call__(self, src1, src2, dst):
                assert (
                    src1.ndarray.size == dst.ndarray.size
                ), "src and dst size not compatible."
                assert (
                    src2.ndarray.size == dst.ndarray.size
                ), "src and dst size not compatible."

                numpy_ipps.status = self._ipps_backend(
                    src1.cdata, src2.cdata, dst.cdata, dst.size
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

    def __call__(cls, dtype, accuracy=None, size=None):
        if numpy.dtype(dtype) not in cls.dtype_candidates:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "Numpy IPPS Function {} doesn't accept [ dtype : {} ].".format(
                    cls, dtype
                ),
            )

        self = super().__call__()

        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                cls._ipps_backend_name,
                dtype,
                accuracy=cls.ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
            policies=cls._ipps_policies,
        )

        return self


class BinaryAccuracy_I(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps.policies.keep_all,
        candidates=numpy_ipps.policies.float_candidates,
        accuracies=numpy_ipps.policies.default_accuracies,
        numpy_swap=False,
        reverse=False,
        force_numpy=False,
    ):
        attrs["__slots__"] = ("_ipps_backend",)
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls.dtype_candidates = candidates
        cls.ipps_accuracies = accuracies
        cls._ipps_kind = numpy_ipps._detail.metaclass.selector.Kind.BINARY_I
        cls._ipps_policies = policies

        if numpy_swap:

            def cls_numpy_backend(self, src, src_dst):
                numpy_backend(
                    src_dst.ndarray,
                    src.ndarray,
                    src_dst.ndarray,
                    casting="unsafe",
                )

        else:

            def cls_numpy_backend(self, src, src_dst):
                numpy_backend(
                    src.ndarray,
                    src_dst.ndarray,
                    src_dst.ndarray,
                    casting="unsafe",
                )

        cls._numpy_backend = cls_numpy_backend

        if force_numpy:
            if numpy_swap:

                def cls__call__(self, src, src_dst):
                    assert (
                        src.ndarray.size == src_dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_backend(
                        src_dst.ndarray,
                        src.ndarray,
                        src_dst.ndarray,
                        casting="unsafe",
                    )

            else:

                def cls__call__(self, src, src_dst):
                    assert (
                        src.ndarray.size == src_dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_backend(
                        src.ndarray,
                        src_dst.ndarray,
                        src_dst.ndarray,
                        casting="unsafe",
                    )

        else:
            if reverse:

                def cls__call__(self, src, src_dst):
                    assert (
                        src.ndarray.size == src_dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_ipps.status = self._ipps_backend(
                        src_dst.cdata, src.cdata, src_dst.cdata, src_dst.size
                    )
                    assert (
                        numpy_ipps.status == 0
                    ), "DEBUG: Bad Intel IPP Signal status {}".format(
                        numpy_ipps.status
                    )

            else:

                def cls__call__(self, src, src_dst):
                    assert (
                        src.ndarray.size == src_dst.ndarray.size
                    ), "src and dst size not compatible."

                    numpy_ipps.status = self._ipps_backend(
                        src.cdata, src_dst.cdata, src_dst.cdata, src_dst.size
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

    def __call__(cls, dtype, accuracy=None, size=None):
        if numpy.dtype(dtype) not in cls.dtype_candidates:
            numpy_ipps._detail.debug.log_and_raise(
                RuntimeError,
                "Numpy IPPS Function {} doesn't accept [ dtype : {} ].".format(
                    cls, dtype
                ),
            )

        self = super().__call__()

        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                cls._ipps_backend_name,
                dtype,
                accuracy=cls.ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
            policies=cls._ipps_policies,
        )

        return self
