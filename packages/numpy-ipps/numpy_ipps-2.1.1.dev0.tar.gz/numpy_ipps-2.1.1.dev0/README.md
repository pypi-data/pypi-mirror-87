## Introduction

Numpy Intel IPP Signal is a Python wrapper for Intel IPP Signal functions.

## Principles

Numpy Intel IPP Signal is based on a __Setup__ and __Payoff__ strategy
* __Setup__ : First Numpy data buffers and Intel IPP Signal operations are 
setup, this step can be slow.
* __Payoff__ : Then operations are executed as fast as possible with Intel IPP 
Signal or Numpy backend functions.  

This strategy suits to deal with stream of data for example.

## Example

```python
# Two Numpy data buffers
src1 = numpy.ones(100, dtype=numpy.float32)
src2 = numpy.zeros(100, dtype=numpy.float32)

# A result buffer
dst = numpy.empty(100, dtype=numpy.float32)

# Intel IPP Signal Mul operation
mul = numpy_ipps.Mul(dtype=numpy.float32)

# Unpack Numpy buffer for fast access
with numpy_ipps.utils.context(src1, src2, dst):
    mul(src1, src2, dst)  # Fast multiplication: dst[n] <- src1[n] * src2[n]
```

## Constructor parameters

Some parameters are often needed by the __Setup__ step:

### `dtype`

To properly select the Intel IPP Signal backend function, the type of the data 
has to be known.

### `size`

For some operations, the size of the data has to be known to switch between 
Intel IPP Signal and Numpy backend.

### `accuracy`

Most of Intel IPP Signal operations on float can be operated at three different
levels.

## List of operations

See more details at [ReadTheDocs.io](https://numpy-intel-ipp-signal.readthedocs.io/).
