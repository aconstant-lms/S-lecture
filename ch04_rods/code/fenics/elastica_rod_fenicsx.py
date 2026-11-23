# elastica_rod_fenicsx.py -- Chapter 4: the elastica as a 1D finite element model in FEniCSx (dolfinx 0.9).
# Printed in the book from line 4 on. Run: python3 elastica_rod_fenicsx.py
# Unknown: the angle theta(s), P1 elements; clamped--sliding rod theta(0) = theta(L) = 0, so P_c = pi^2 EI/L^2.
import numpy as np
import ufl
from mpi4py import MPI
from petsc4py import PETSc
from scipy.special import ellipk
from scipy.optimize import brentq
from dolfinx import mesh, fem
from dolfinx.fem.petsc import NonlinearProblem
from dolfinx.nls.petsc import NewtonSolver

EI, L, ne = 1.0, 1.0, 200
domain = mesh.create_interval(MPI.COMM_WORLD, ne, [0.0, L])
V = fem.functionspace(domain, ("Lagrange", 1))
th, v = fem.Function(V), ufl.TestFunction(V)
P = fem.Constant(domain, PETSc.ScalarType(0.0))

# --- the energy (eq. rd-elastica-energy) and its first variation ---------------------------
W = (0.5 * EI * ufl.inner(ufl.grad(th), ufl.grad(th)) - P * (1 - ufl.cos(th))) * ufl.dx
F = ufl.derivative(W, th, v)
ends = fem.locate_dofs_geometrical(V, lambda x: np.isclose(x[0], 0.0) | np.isclose(x[0], L))
bcs = [fem.dirichletbc(PETSc.ScalarType(0.0), ends, V)]
problem = NonlinearProblem(F, th, bcs=bcs)
newton = NewtonSolver(MPI.COMM_WORLD, problem)
newton.rtol, newton.atol, newton.max_it = 1e-12, 1e-12, 50

# --- load control above P_c, starting from the mode (the branch is stable: Newton stays on it)
Pc = np.pi**2 * EI / L**2
th.interpolate(lambda x: 0.3 * np.sin(np.pi * x[0] / L))
mid = fem.locate_dofs_geometrical(V, lambda x: np.isclose(x[0], L / 2))[0]
exact_alpha = lambda p: 2 * np.arcsin(np.sqrt(brentq(lambda m: (2 * ellipk(m) / np.pi)**2 - p, 1e-12, 0.999999)))
print("  P/Pc    alpha FE (deg)   alpha exact (deg)")
for p in (1.01, 1.05, 1.2, 1.5, 2.0, 3.0):
    P.value = p * Pc
    newton.solve(th)
    a = abs(th.x.array[mid])
    print(f"{p:6.2f}   {np.degrees(a):12.4f}   {np.degrees(exact_alpha(p)):14.4f}")
