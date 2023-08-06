import _accupy
import numpy

from .sums import fsum, ksum

# def dot2(x, y, prod2=prod2_fma):
#     '''Algorithm 5.3. Dot product in twice the working precision.
#     in <https://doi.org/10.1137/030601818>.
#     '''
#     p, s = prod2(x[0], y[0])
#     n = len(x)
#     for k in range(1, n):
#         h, r = prod2(x[k], y[k])
#         p, q = knuth_sum(p, h)
#         s += q+r
#     return p + s


def kdot(x, y, K=2):
    """Algorithm 5.10. Dot product algorithm in K-fold working precision,
    K >= 3.
    """
    xx = x.reshape(-1, x.shape[-1])
    yy = y.reshape(y.shape[0], -1)

    xx = numpy.ascontiguousarray(xx)
    yy = numpy.ascontiguousarray(yy)

    r = _accupy.kdot_helper(xx, yy).reshape((-1,) + x.shape[:-1] + y.shape[1:])
    return ksum(r, K - 1)


def fdot(x, y):
    """Algorithm 5.10. Dot product algorithm in K-fold working precision,
    K >= 3.
    """
    xx = x.reshape(-1, x.shape[-1])
    yy = y.reshape(y.shape[0], -1)

    xx = numpy.ascontiguousarray(xx)
    yy = numpy.ascontiguousarray(yy)

    r = _accupy.kdot_helper(xx, yy).reshape((-1,) + x.shape[:-1] + y.shape[1:])
    return fsum(r)
