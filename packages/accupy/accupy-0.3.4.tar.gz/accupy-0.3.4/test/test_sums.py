import dufte
import matplotlib.pyplot as plt
import numpy
import perfplot
import pytest

import accupy


@pytest.mark.parametrize("cond", [1.0, 1.0e15])
def test_ksum2(cond):
    p, ref, _ = accupy.generate_ill_conditioned_sum(100, cond)
    assert abs(accupy.ksum(p, K=2) - ref) < 1.0e-15 * abs(ref)


@pytest.mark.parametrize("cond", [1.0, 1.0e15, 1.0e30])
def test_ksum3(cond):
    p, ref, _ = accupy.generate_ill_conditioned_sum(100, cond)
    assert abs(accupy.ksum(p, K=3) - ref) < 1.0e-15 * abs(ref)


@pytest.mark.parametrize("cond", [1.0, 1.0e15, 1.0e30, 1.0e35])
def test_fsum(cond):
    p, ref, _ = accupy.generate_ill_conditioned_sum(100, cond)
    assert abs(accupy.fsum(p) - ref) < 1.0e-15 * abs(ref)


def test_accuracy_comparison_illcond(filename=None, target_conds=None):
    plt.style.use(dufte.style)

    if target_conds is None:
        target_conds = [10 ** k for k in range(1, 2)]

    kernels = [
        sum,
        numpy.sum,
        accupy.kahan_sum,
        lambda p: accupy.ksum(p, K=2),
        lambda p: accupy.ksum(p, K=3),
        accupy.fsum,
    ]
    labels = [
        "sum",
        "numpy.sum",
        "accupy.kahan_sum",
        "accupy.ksum[2]",
        "accupy.ksum[3]",
        "accupy.fsum",
    ]
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"][: len(labels)]

    data = numpy.empty((len(target_conds), len(kernels)))
    condition_numbers = numpy.empty(len(target_conds))
    numpy.random.seed(0)
    for k, target_cond in enumerate(target_conds):
        p, ref, C = accupy.generate_ill_conditioned_sum(1000, target_cond)
        condition_numbers[k] = C
        data[k] = [abs(kernel(p) - ref) / abs(ref) for kernel in kernels]

    # sort
    s = numpy.argsort(condition_numbers)
    condition_numbers = condition_numbers[s]
    data = data[s]

    for label, color, d in zip(labels, colors, data.T):
        plt.loglog(condition_numbers, d, label=label, color=color)

    dufte.legend()
    plt.xlabel("condition number")
    plt.ylabel("relative error")
    # plt.gca().set_aspect(1.3)

    # plt.show()
    # <https://stackoverflow.com/a/10154763/353337>
    if filename:
        plt.savefig(filename, transparent=True, bbox_inches="tight")


def test_speed_comparison1(filename=None, n_range=None):
    plt.style.use(dufte.style)

    if n_range is None:
        n_range = [2 ** k for k in range(2)]

    numpy.random.seed(0)
    perfplot.plot(
        setup=lambda n: numpy.random.rand(n, 100),
        kernels=[
            sum,
            lambda p: numpy.sum(p, axis=0),
            accupy.kahan_sum,
            lambda p: accupy.ksum(p, K=2),
            lambda p: accupy.ksum(p, K=3),
            accupy.fsum,
        ],
        labels=[
            "sum",
            "numpy.sum",
            "accupy.kahan_sum",
            "accupy.ksum[2]",
            "accupy.ksum[3]",
            "accupy.fsum",
        ],
        n_range=n_range,
        xlabel="n",
    )
    plt.title("Sum(random(n, 100))")

    # plt.show()
    if filename:
        plt.savefig(filename, transparent=True, bbox_inches="tight")


def test_speed_comparison2(filename=None, n_range=None):
    plt.style.use(dufte.style)

    if n_range is None:
        n_range = [2 ** k for k in range(2)]

    numpy.random.seed(0)
    perfplot.plot(
        setup=lambda n: numpy.random.rand(100, n),
        kernels=[
            sum,
            lambda p: numpy.sum(p, axis=0),
            accupy.kahan_sum,
            lambda p: accupy.ksum(p, K=2),
            lambda p: accupy.ksum(p, K=3),
            accupy.fsum,
        ],
        labels=[
            "sum",
            "numpy.sum",
            "accupy.kahan_sum",
            "accupy.ksum[2]",
            "accupy.ksum[3]",
            "accupy.fsum",
        ],
        n_range=n_range,
        xlabel="n",
    )
    plt.title("Sum(random(100, n))")

    # plt.show()
    if filename:
        plt.savefig(filename, transparent=True, bbox_inches="tight")


def test_knuth_sum():
    a16 = numpy.float16(1.0e1)
    b16 = numpy.float16(1.0e-1)
    x16, y16 = accupy.knuth_sum(a16, b16)
    xy = numpy.float64(x16) + numpy.float64(y16)
    ab = numpy.float64(a16) + numpy.float64(b16)
    assert abs(xy - ab) < 1.0e-15 * ab


def test_decker_sum():
    a16 = numpy.float16(1.0e1)
    b16 = numpy.float16(1.0e-1)
    x16, y16 = accupy.decker_sum(a16, b16)
    xy = numpy.float64(x16) + numpy.float64(y16)
    ab = numpy.float64(a16) + numpy.float64(b16)
    assert abs(xy - ab) < 1.0e-15 * ab


def test_discontiguous():
    x = numpy.random.rand(3, 10).T
    accupy.ksum(x.T)
    accupy.fsum(x.T)


if __name__ == "__main__":
    # test_accuracy_comparison_illcond(
    #     "accuracy-sum.svg", [10 ** k for k in range(0, 37, 1)]
    # )
    # test_speed_comparison1("speed-comparison1.svg", n_range=[2 ** k for k in range(15)])
    test_speed_comparison2("speed-comparison2.svg", n_range=[2 ** k for k in range(15)])
