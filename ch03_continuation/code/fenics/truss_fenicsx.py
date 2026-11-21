# truss_fenicsx.py -- Chapter 3: the two-bar truss in FEniCSx (dolfinx 0.9, petsc4py, slepc4py).
# Printed in the book from line 4 on. Run: python3 truss_fenicsx.py  (needs ../python/truss_fe.py)
# Energy in UFL; residual and tangent by derivative; linear buckling with SLEPc; arc-length by bordering.
import os, sys
import numpy as np
import ufl, basix.ufl
from mpi4py import MPI
from slepc4py import SLEPc
from dolfinx import mesh, fem
from dolfinx.fem.petsc import assemble_matrix, assemble_vector
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "python"))
from truss_fe import follow, locate                      # the same arc-length driver as in Python

# --- 1. two interval elements in the plane, EA = L = 1 ------------------------------------
phi = np.radians(30.0); s, c = np.sin(phi), np.cos(phi)
x = np.array([[-c, 0.0], [c, 0.0], [0.0, s]])
cells = np.array([[0, 2], [1, 2]], dtype=np.int64)
coord = ufl.Mesh(basix.ufl.element("Lagrange", "interval", 1, shape=(2,)))
domain = mesh.create_mesh(MPI.COMM_SELF, cells, x, coord)
V = fem.functionspace(domain, ("Lagrange", 1, (2,)))

# --- 2. the energy of a bar with Green strain, and its two derivatives --------------------
u, v, du = fem.Function(V), ufl.TestFunction(V), ufl.TrialFunction(V)
J = ufl.Jacobian(domain)[:, 0]
t0 = J / ufl.sqrt(ufl.dot(J, J))                          # unit vector along the bar
dS = lambda w: ufl.dot(ufl.grad(w), t0)                   # derivative along the bar
eps = ufl.dot(t0, dS(u)) + 0.5 * ufl.dot(dS(u), dS(u))    # Green strain of a bar
EA = 1.0
Pi = 0.5 * EA * eps**2 * ufl.dx                           # strain energy
F = fem.form(ufl.derivative(Pi, u, v))                    # internal forces: the weak form
K = fem.form(ufl.derivative(ufl.derivative(Pi, u, v), u, du))   # tangent stiffness

fixed = fem.locate_dofs_geometrical(V, lambda X: np.isclose(X[1], 0.0))
bcs = [fem.dirichletbc(np.zeros(2, dtype=np.float64), fixed, V)]
fixed_flat = np.concatenate([2 * fixed, 2 * fixed + 1])
apex = fem.locate_dofs_geometrical(V, lambda X: np.isclose(X[1], s))[0]
p = np.zeros(V.dofmap.index_map.size_local * 2); p[2 * apex + 1] = -1.0   # eta downwards

class Model:
    """The FEniCSx forms seen as the residual r(u, eta) and the tangent K(u) of the Python code."""
    p = p
    def residual(self, uu, eta):
        u.x.array[:] = uu
        r = assemble_vector(F).array.copy() - eta * self.p
        r[fixed_flat] = 0.0
        return r
    def tangent(self, uu):
        u.x.array[:] = uu
        A = assemble_matrix(K, bcs=bcs); A.assemble()
        return A.convert("dense").getDenseArray().copy()

# --- 3. linear buckling: K0 phi = eta (-K_sigma) phi, solved by SLEPc ----------------------
m = Model()
u1 = np.linalg.solve(m.tangent(np.zeros_like(p)), p)      # linear prebuckling, eta = 1
w1 = fem.Function(V); w1.x.array[:] = u1
N1 = EA * ufl.dot(t0, dS(w1))                             # its normal force (linear strain)
KG = fem.form(-N1 * ufl.dot(dS(du), dS(v)) * ufl.dx)      # -K_sigma: positive in compression
u.x.array[:] = 0.0
A = assemble_matrix(K, bcs=bcs); A.assemble()             # K0, with 1 on the fixed rows
B = assemble_matrix(KG, bcs=bcs, diagonal=0.0); B.assemble()   # 0 there: their eigenvalue is infinite
solver = SLEPc.EPS().create(MPI.COMM_SELF)
solver.setOperators(A, B)
solver.setProblemType(SLEPc.EPS.ProblemType.GNHEP)
solver.getST().setType(SLEPc.ST.Type.SINVERT)              # shift and invert about the target 0
solver.setTarget(0.0)
solver.setWhichEigenpairs(SLEPc.EPS.Which.TARGET_REAL)
solver.setDimensions(2)
solver.solve()
print("linear buckling loads:", sorted(solver.getEigenvalue(i).real for i in range(solver.getConverged())))

# --- 4. the nonlinear path by arc-length, and the limit point ------------------------------
path = follow(m, np.zeros_like(p), 0.0, 0.02, 80)
k = next(i for i in range(1, len(path)) if path[i][2] != path[i - 1][2])
uc, ec, mode, kind = locate(m, path[k - 1], path[k])
print(f"first critical point: eta = {ec:.5f} ({kind}); closed form {2 * s**3 / (3 * np.sqrt(3)):.5f}")
