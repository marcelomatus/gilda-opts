"""Test linear problem."""
from math import isclose
from scipy.optimize import linprog
import numpy as np
import pyomo.environ as pyo

from gilda_opts import linear_problem as lpm


def test_lp_1():
    """Test LP 1."""
    lp = lpm.LinearProblem(scale_obj=1.0, solver='cbc')

    x = lp.add_col("x", c=-1)
    assert x == 0

    y = lp.add_col("y", c=-2)
    assert y == 1

    r1 = {}
    r1[0] = 2
    r1[1] = 1

    c1 = lp.add_row(r1, ub=20)
    assert c1 == 0

    r2 = {}
    r2[0] = -4
    r2[1] = 5

    c2 = lp.add_row(r2, ub=10)
    assert c2 == 1

    r3 = {}
    r3[0] = 1
    r3[1] = -2

    c3 = lp.add_row(r3, ub=2)
    assert c3 == 2

    assert lp.cols == 2
    assert lp.rows == 3

    A, rlb, rub, cul, cub, c = lp.sparse_model()  # pylint: disable=C0103,W0612

    assert np.array_equal(A.toarray(), np.array([[2, 1], [-4, 5], [1, -2]]))

    assert np.array_equal(rub, np.array([20, 10, 2]))

    lp.solve(keepfiles=False)

    assert lp.get_status() == 'ok'

    rel_tol = 1e-6
    assert isclose(lp.get_obj(), -20.7142856, rel_tol=rel_tol)

    #
    # scipy solution
    #
    obj = [-1, -2]
    #      ─┬  ─┬
    #       │   └┤ Coefficient for y
    #       └────┤ Coefficient for x

    lhs_ineq = [
        [2, 1],  # Red constraint left side
        [-4, 5],  # Blue constraint left side
        [1, -2]
    ]  # Yellow constraint left side

    rhs_ineq = [
        20,  # Red constraint right side
        10,  # Blue constraint right side
        2
    ]  # Yellow constraint right side

    bnd = [
        (0, float("inf")),  # Bounds of x
        (0, float("inf"))
    ]  # Bounds of y

    opt = linprog(c=obj,
                  A_ub=lhs_ineq,
                  b_ub=rhs_ineq,
                  bounds=bnd)

    assert isclose(lp.get_obj(), opt.fun, rel_tol=rel_tol)

    m = lp.model

    assert len(m.x) == 2
    assert isclose(pyo.value(m.x[0]), opt.x[0], rel_tol=rel_tol)
    assert isclose(pyo.value(m.x[1]), opt.x[1], rel_tol=rel_tol)

    assert len(m.constraints) == 3
    assert isclose(pyo.value(m.dual[m.constraints[0]]),
                   -0.928571428571429,
                   rel_tol=rel_tol)
    assert isclose(pyo.value(m.dual[m.constraints[1]]),
                   -0.214285714285714,
                   rel_tol=rel_tol)
