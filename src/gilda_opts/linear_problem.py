"""Contains the linear problem module."""
import numpy as np
import pyomo.environ as pyo
import pyomo.kernel as pmo
from scipy.sparse import dok_matrix


def guid(*uids):
    """Generate an uid valid for use as a LP name."""
    g = ''
    for i in uids:
        g += ':' + str(i) if g else str(i)
    return g


class LinearProblem:
    """
    Represents a linear problem interface class and its interaction with the solver.

    Attributes:
    -----------
    A:   Constraint Matrix
    c:   cost vector
    clb: col lower boundary vector
    cub: col upper boundary vector
    rlb: row lower boundary vector
    rub: row upper boundary vector
    """

    inf = float("inf")

    def __init__(self, scale_obj=1.0, solver='cbc', integer_mode=True):
        """Construct a linear problem."""
        self.scale_obj = scale_obj
        self.solver = solver
        self.integer_mode = integer_mode

        self.A = {}  # pylint: disable=C0103
        self.c = {}
        self.clb = {}
        self.cub = {}
        self.rlb = {}
        self.rub = {}

        self.rnames = {}
        self.cnames = {}
        self.ctypes = {}

        self.rpos = {}
        self.cpos = {}

        self.cols = 0
        self.rows = 0

        self.model = None
        self.result = None

    def numcols(self):
        """Return the number of columns or variables."""
        return self.cols

    def numrows(self):
        """Return the number of rows or constraints."""
        return self.rows

    def add_col(self, name=None, lb=0, ub=inf, c=0, ctype=0):
        """Add one column or variable to the LP problem."""
        j = self.cols
        self.clb[j] = lb
        self.cub[j] = ub
        self.c[j] = c
        self.ctypes[j] = ctype
        self.cnames[j] = name
        self.cpos[name] = j

        self.cols += 1
        return j

    def add_row(self, row={}, name=None, lb=-inf, ub=inf):  # pylint: disable=W0102
        """Add one column or constraint to the LP problem."""
        i = self.rows
        for j, v in row.items():
            self.A[i, j] = v

        self.rlb[i] = lb
        self.rub[i] = ub
        self.rnames[i] = name
        self.rpos[name] = i

        self.rows += 1
        return i

    def add_rhs_row(self, row={}, name=None, rhs=0):  # pylint: disable=W0102
        """Add one column or constraint to the LP problem providing the RHS."""
        return self.add_row(row, name=name, lb=rhs, ub=rhs)

    def set_coeff(self, i, j, v):
        """Set the constraint matrix coefficient."""
        self.A[i, j] = v

    def set_objc(self, j, cv):
        """Set the variable cost for a given variable."""
        self.c[j] = cv

    def set_col_lb(self, j, clb):
        """Set the lower boundary for a given variable."""
        self.clb[j] = clb

    def set_col_ub(self, j, cub):
        """Set the upper boundary for a given variable."""
        self.cub[j] = cub

    def set_col(self, j, value):
        """Set the column or variable value."""
        self.clb[j] = value
        self.cub[j] = value

    def get_row_rhs(self, i):
        """Get the row RHS."""
        return self.rlb.get(i, 0)

    def set_row_rhs(self, i, v):
        """Set the row RHS."""
        self.rlb[i] = v
        self.rub[i] = v

    def sparse_model(self):
        """Calculate the sparse model."""
        A = dok_matrix((self.rows, self.cols))  # pylint: disable=C0103
        for ij, v in self.A.items():
            if v != 0:
                A[ij] = v

        rlb = np.ndarray(self.rows, dtype=float)
        for k, v in self.rlb.items():
            rlb[k] = v

        rub = np.ndarray(self.rows, dtype=float)
        for k, v in self.rub.items():
            rub[k] = v

        clb = np.ndarray(self.cols, dtype=float)
        for k, v in self.clb.items():
            clb[k] = v

        cub = np.ndarray(self.cols, dtype=float)
        for k, v in self.cub.items():
            cub[k] = v

        c = np.ndarray(self.cols, dtype=float)
        for k, v in self.c.items():
            c[k] = v

        return A, rlb, rub, clb, cub, c

    def pyomo_model(self):
        """Calculate the pyomo model."""
        m = pmo.block()
        m.rows = range(self.rows)
        m.cols = range(self.cols)
        m.A, m.rlb, m.rub, m.clb, m.cub, m.c = self.sparse_model()

        m.x = pmo.variable_list()
        for j in m.cols:
            dtype = (pmo.IntegerSet
                     if self.integer_mode and self.ctypes[j] else pmo.RealSet)
            xj = pmo.variable(
                lb=m.clb[j],
                ub=m.cub[j],
                domain_type=dtype,
            )
            m.x.append(xj)

        m.dual = pmo.suffix(direction=pmo.suffix.IMPORT)

        m.constraints = pmo.matrix_constraint(m.A, lb=m.rlb, ub=m.rub, x=m.x)

        scale = 1.0 / self.scale_obj
        m.obj = pmo.objective(expr=sum(
            (scale * m.c[col]) * m.x[col] for col in m.cols))

        m.cnames = self.cnames
        m.rnames = self.rnames

        m.cpos = self.cpos
        m.rpos = self.rpos

        return m

    def solve(
        self,
        solver=None,
        keepfiles=False,
        solver_options=None,
    ):
        """Solve the LP problem."""
        self.model = self.pyomo_model()

        solver = solver if solver is not None \
            else self.solver

        self.solver = pmo.SolverFactory(solver)
        options_string = solver_options if solver_options is not None else ""
        self.result = self.solver.solve(self.model,
                                        options_string=options_string,
                                        keepfiles=keepfiles)

        return self.result

    def get_col_ub(self, j):
        """Get the column or variable upper bound."""
        return self.cub[j]

    def get_col_lb(self, j):
        """Get the column or variable upperlow bound."""
        return self.clb[j]

    def get_status(self):
        """Get the solver status."""
        return self.result.solver.status

    def get_time(self):
        """Get the solution time."""
        return self.result.solver.time

    def get_col_at(self, index):
        """Get the solution value at the given index."""
        return pyo.value(self.model.x[index])

    def get_col_sol(self, indexes):
        """Get the solution values for a given indexes list."""
        x = np.ndarray(len(indexes))
        for k, j in enumerate(indexes):
            x[k] = self.get_col_at(j)

        return x

    def get_dual_at(self, i):
        """Get the dual value at the given index."""
        return pyo.value(
            self.model.dual[self.model.constraints[i]]) * self.scale_obj

    def get_dual_sol(self, indexes):
        """Get the dual values for a given indexes list."""
        y = np.ndarray(len(indexes))
        for k, i in enumerate(indexes):
            y[k] = self.get_dual_at(i)

        return y

    def get_obj(self):
        """Get the objective function value."""
        return float(pyo.value(self.model.obj) * self.scale_obj)
