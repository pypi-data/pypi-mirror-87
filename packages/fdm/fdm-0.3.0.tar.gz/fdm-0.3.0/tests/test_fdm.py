import numpy as np
import pytest

from fdm import forward_fdm, backward_fdm, central_fdm, FDM
from fdm.fdm import _estimate_magnitude
from .util import approx


def test_estimate_magnitude():
    assert _estimate_magnitude(lambda x: x, 0) == 0.1
    assert _estimate_magnitude(lambda x: x, 1) == 1


def test_construction():
    with pytest.raises(ValueError):
        FDM([-1, 0, 1], 3)


def test_correctness():
    for f in [forward_fdm, backward_fdm, central_fdm]:
        approx(f(10, 1)(np.sin, 1), np.cos(1))
        approx(f(10, 2)(np.sin, 1), -np.sin(1))

        approx(f(10, 1)(np.exp, 1), np.exp(1))
        approx(f(10, 2)(np.exp, 1), np.exp(1))

        approx(f(10, 1)(np.sqrt, 1), 0.5)
        approx(f(10, 2)(np.sqrt, 1), -0.25)


def test_estimation():
    m = central_fdm(2, 1)

    assert m.eps is None
    assert m.bound is None
    assert m.step is None
    assert m.acc is None

    m.estimate()

    assert isinstance(m.eps, float)
    assert isinstance(m.bound, float)
    assert isinstance(m.step, float)
    assert isinstance(m.acc, float)

    m(np.sin, 0, step=1e-3)

    assert m.eps is None
    assert m.bound is None
    assert isinstance(m.step, float)
    assert m.acc is None


def test_adaptation():
    def f(x):
        return 1 / x

    def df(x):
        return -1 / x ** 2

    err1 = np.abs(forward_fdm(3, 1, adapt=0)(f, 1e-3) - df(1e-3))
    err2 = np.abs(forward_fdm(3, 1, adapt=1)(f, 1e-3) - df(1e-3))

    # Check that adaptation helped.
    assert err2 <= 1e-2 * err1

    # Check that adaptation gets it right.
    assert err2 <= 1e-4


def test_order_monotonicity():
    err_ref = 1e-4

    for i in range(3, 8):
        err = np.abs(central_fdm(i, 2, condition=1)(np.sin, 1) + np.sin(1))

        # Check that it did better than the previous estimator.
        assert err <= err_ref

        err_ref = err


def test_stability():
    assert central_fdm(2, 1, adapt=0)(lambda x: 0.0, 1.0) == 0.0
    assert central_fdm(2, 1, adapt=1, step_max=np.inf)(lambda x: x, 1.0) == 1.0


def test_factor():
    assert (
        central_fdm(3, 1, factor=5).estimate().eps
        == 5 * central_fdm(3, 1, factor=1).estimate().eps
    )


def test_step_max():
    assert central_fdm(20, 1, step_max=np.inf).estimate().step > 0.1
    assert central_fdm(20, 1, step_max=0.1).estimate().step == 0.1


def test_case_cosc():
    def cosc(x):
        if x == 0:
            return 0.0
        else:
            return np.cos(np.pi * x) / x - np.sin(np.pi * x) / (np.pi * x ** 2)

    approx(central_fdm(5, 1)(cosc, 0), -np.pi ** 2 / 3, atol=1e-9)
    approx(central_fdm(10, 1, adapt=2)(cosc, 0), -np.pi ** 2 / 3, atol=5e-13)
