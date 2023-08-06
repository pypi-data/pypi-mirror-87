from .__about__ import __version__
from .dot import fdot, kdot
from .ill_cond import generate_ill_conditioned_dot_product, generate_ill_conditioned_sum
from .sums import decker_sum, distill, fsum, kahan_sum, knuth_sum, ksum

__all__ = [
    "__version__",
    "kdot",
    "fdot",
    "generate_ill_conditioned_sum",
    "generate_ill_conditioned_dot_product",
    "knuth_sum",
    "decker_sum",
    "distill",
    "ksum",
    "fsum",
    "kahan_sum",
]
