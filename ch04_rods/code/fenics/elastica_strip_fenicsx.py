# elastica_strip_fenicsx.py -- Chapter 4: a thin plane-strain strip in FEniCSx (dolfinx 0.9), compared with the elastica.
# Printed in the book from line 4 on. Run: python3 elastica_strip_fenicsx.py
# Saint Venant--Kirchhoff strip L x h, clamped at x = 0, clamped and pushed by -Delta at x = L. P_c = 4 pi^2 EI/L^2.
import numpy as np
import ufl
from mpi4py import MPI
from petsc4py import PETSc
from scipy.special import ellipk, ellipe
from dolfinx import mesh, fem
from dolfinx.fem.petsc import NonlinearProblem, assemble_vector
from dolfinx.nls.petsc import NewtonSolver

L, h, E, nu = 1.0, 0.01, 1.0, 0.3
domain = mesh.create_rectangle(MPI.COMM_WORLD, [[0, -h / 2], [L, h / 2]], [400, 4],
                               mesh.CellType.quadrilateral)
V = fem.functionspace(domain, ("Lagrange", 2, (2,)))
u, v = fem.Function(V), ufl.TestFunction(V)
lmb, mu = E * nu / ((1 + nu) * (1 - 2 * nu)), E / (2 * (1 + nu))
F_ = ufl.Identity(2) + ufl.grad(u)
e = 0.5 * (F_.T * F_ - ufl.Identity(2))                        # Green--Lagrange strain
psi = 0.5 * lmb * ufl.tr(e)**2 + mu * ufl.inner(e, e)          # Saint Venant--Kirchhoff, plane strain
x = ufl.SpatialCoordinate(domain)
f = fem.Constant(domain, PETSc.ScalarType(1e-7))               # tiny lateral load in the shape of the mode
W = psi * ufl.dx - f * (1 - ufl.cos(2 * np.pi * x[0] / L)) * u[1] * ufl.dx
Fres = ufl.derivative(W, u, v)

left = fem.locate_dofs_geometrical(V, lambda X: np.isclose(X[0], 0.0))
right = fem.locate_dofs_geometrical(V, lambda X: np.isclose(X[0], L))
Vx, _ = V.sub(0).collapse(); Vy, _ = V.sub(1).collapse()
rx = fem.locate_dofs_geometrical((V.sub(0), Vx), lambda X: np.isclose(X[0], L))
ry = fem.locate_dofs_geometrical((V.sub(1), Vy), lambda X: np.isclose(X[0], L))
ux = fem.Function(Vx); uy = fem.Function(Vy)
bcs = [fem.dirichletbc(np.zeros(2, dtype=PETSc.ScalarType), left, V),
       fem.dirichletbc(ux, rx, V.sub(0)), fem.dirichletbc(uy, ry, V.sub(1))]
problem = NonlinearProblem(Fres, u, bcs=bcs)
newton = NewtonSolver(MPI.COMM_WORLD, problem)
newton.rtol, newton.atol, newton.max_it = 1e-10, 1e-12, 30

EI = E / (1 - nu**2) * h**3 / 12                               # per unit width, plane strain
Pc = 4 * np.pi**2 * EI / L**2
Rform = fem.form(Fres)
print(" Delta/L    P/Pc FE    P/Pc elastica (same bending shortening)")
ms = np.linspace(1e-6, 0.95, 4000)                             # closed form: Delta/L = 2 - 2E/K, P/Pc = (2K/pi)^2
dl, pl = 2 - 2 * ellipe(ms) / ellipk(ms), (2 * ellipk(ms) / np.pi)**2
for d in np.concatenate([np.linspace(1e-4, 3e-3, 6), np.linspace(0.01, 0.3, 8)]):
    ux.x.array[:] = -d * L
    newton.solve(u)
    r = assemble_vector(Rform).array                           # internal forces at the dofs
    P = -np.sum(r[rx[0]])                                      # reaction on the right edge, x components
    db = d - P / (E / (1 - nu**2) * h)                         # remove the axial shortening P L/(EA)
    pe = np.interp(db, dl, pl) if db > 0 else 1.0
    print(f"{d:8.4f}   {P/Pc:8.4f}   {pe:8.4f}")
