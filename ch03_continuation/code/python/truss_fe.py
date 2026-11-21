# truss_fe.py -- Chapter 3: a finite element code for bars with Green strain, written from scratch.
# Printed in the book from line 4 on. Run: python3 truss_fe.py  (NumPy, SciPy). Used by ex_truss.py.
# Residual, tangent, K0 and K_sigma, linear buckling, Riks/Crisfield arc-length, inertia, branch switching.
import numpy as np
from scipy.linalg import eigh, ldl, solve

class Bars:
    """Pin-jointed bars, energy E = sum EA L eps^2 / 2 - eta p.u, eps = (|x|^2 - |X|^2) / (2 L^2)."""
    def __init__(self, X, elems, EA, free, p):
        self.X, self.el, self.EA = np.array(X, float), elems, EA
        self.free, self.p = np.array(free), np.array(p, float)   # free dofs and load vector
        self.ndof = 2 * len(self.X)

    def _loop(self, u):
        U = np.zeros(self.ndof); U[self.free] = u
        for i, j in self.el:
            d = [2 * i, 2 * i + 1, 2 * j, 2 * j + 1]
            Xe = self.X[j] - self.X[i]; L2 = Xe @ Xe
            x = Xe + U[d[2:]] - U[d[:2]]                      # current bar vector
            eps = (x @ x - L2) / (2 * L2)
            yield d, x, np.sqrt(L2), self.EA * eps            # dofs, x, L, normal force N

    def _gather(self, F):
        return F[np.ix_(self.free, self.free)] if F.ndim == 2 else F[self.free]

    def energy(self, u, eta):
        return sum(N**2 * L / (2 * self.EA) for _, _, L, N in self._loop(u)) - eta * self.p @ u

    def fint(self, u):
        F = np.zeros(self.ndof)
        for d, x, L, N in self._loop(u):
            f = N * x / L                                      # dE/dx_j = N L deps/dx_j
            F[d[:2]] -= f; F[d[2:]] += f
        return self._gather(F)

    def residual(self, u, eta):
        return self.fint(u) - eta * self.p

    def tangent(self, u, geometric=True, material=True):
        """K = sum (EA/L) x x^T / L^2 (material)  +  (N/L) I (geometric), on [[k, -k], [-k, k]]."""
        K = np.zeros((self.ndof, self.ndof))
        for d, x, L, N in self._loop(u):
            k = material * self.EA / L**3 * np.outer(x, x) + geometric * N / L * np.eye(2)
            K[np.ix_(d, d)] += np.block([[k, -k], [-k, k]])
        return self._gather(K)

    def K0(self):
        return self.tangent(np.zeros(len(self.free)))

    def Ksigma(self):
        """Geometric stiffness of the linear prebuckling state for eta = 1 (Box 3.2)."""
        u1 = solve(self.K0(), self.p)                          # linear solution, unit load
        K = np.zeros((self.ndof, self.ndof)); U = np.zeros(self.ndof); U[self.free] = u1
        for i, j in self.el:
            d = [2 * i, 2 * i + 1, 2 * j, 2 * j + 1]
            Xe = self.X[j] - self.X[i]; L = np.linalg.norm(Xe)
            N = self.EA * Xe @ (U[d[2:]] - U[d[:2]]) / L**2   # linearised normal force
            k = N / L * np.eye(2)
            K[np.ix_(d, d)] += np.block([[k, -k], [-k, k]])
        return self._gather(K)

def linear_buckling(m):
    """(K0 + eta K_sigma) phi = 0, solved as -K_sigma phi = mu K0 phi, eta = 1/mu (mu > 0)."""
    mu, Phi = eigh(-m.Ksigma(), m.K0())
    keep = mu > 1e-12
    order = np.argsort(1 / mu[keep])
    return (1 / mu[keep])[order], Phi[:, keep][:, order]

def negative_pivots(K):
    """Inertia: number of negative eigenvalues of K = L D L^T, read on D (Sylvester)."""
    _, D, _ = ldl(K)
    return int(np.sum(np.linalg.eigvalsh(D) < 0))   # D is block diagonal (1x1 and 2x2 blocks)

def newton(m, u, eta, tol=1e-12, maxit=30):
    """Load control: Newton at fixed eta (fails beyond a limit point)."""
    for _ in range(maxit):
        r = m.residual(u, eta)
        if np.linalg.norm(r) < tol: return u, True
        u = u - solve(m.tangent(u), r)
    return u, False

def arclength_step(m, u, eta, du_old, deta_old, ds, psi=1.0, method="crisfield", tol=1e-11, maxit=25):
    """One step of Box 3.3. Bordering: two solves with K per iteration, never the augmented matrix."""
    pp = m.p @ m.p
    up = solve(m.tangent(u), m.p)                                  # tangent: K up = p
    deta = ds / np.sqrt(up @ up + psi**2 * pp)
    if up @ du_old + psi**2 * pp * deta * deta_old < 0: deta = -deta  # keep the direction of travel
    Du, Deta = deta * up, deta                                     # predictor
    Du0, Deta0 = Du.copy(), Deta
    for it in range(maxit):
        r = m.residual(u + Du, eta + Deta)
        if np.linalg.norm(r) < tol and it > 0: return u + Du, eta + Deta, Du, Deta, it
        K = m.tangent(u + Du)
        dur, dup = solve(K, -r), solve(K, m.p)                   # the two solves
        if method == "riks":                                      # normal plane: linear in d_eta
            de = -(Du0 @ dur) / (Du0 @ dup + psi**2 * pp * Deta0)
        else:                                                     # sphere: quadratic in d_eta
            a = dup @ dup + psi**2 * pp
            b = 2 * (Du + dur) @ dup + 2 * psi**2 * pp * Deta
            c = (Du + dur) @ (Du + dur) + psi**2 * pp * Deta**2 - ds**2
            disc = b * b - 4 * a * c
            if disc < 0: return None
            roots = [(-b + sg * np.sqrt(disc)) / (2 * a) for sg in (1, -1)]
            # Crisfield's choice: the root whose increment stays closest to the previous one
            de = max(roots, key=lambda e: (Du + dur + e * dup) @ Du + psi**2 * pp * (Deta + e) * Deta)
        Du, Deta = Du + dur + de * dup, Deta + de
    return None

def follow(m, u, eta, ds, nsteps, du0=None, deta0=1.0, **kw):
    """Arc-length path with step halving; records the inertia of K at every point."""
    du_old = np.zeros_like(u) if du0 is None else du0
    deta_old, path = deta0, [(u.copy(), eta, negative_pivots(m.tangent(u)))]
    for _ in range(nsteps):
        h = ds
        while (out := arclength_step(m, u, eta, du_old, deta_old, h, **kw)) is None:
            h /= 2
            if h < ds / 64: return path
        u, eta, du_old, deta_old, _ = out
        path.append((u.copy(), eta, negative_pivots(m.tangent(u))))
    return path

def locate(m, a, b, tol=1e-10):
    """Bisection on the segment between two path points where the inertia changes (L6, slide 3).
    Each trial point is corrected onto the path by Newton at fixed eta, or at fixed u_k if needed."""
    (ua, ea, na), (ub, eb, _) = a, b
    for _ in range(80):
        t = 0.5; um, em = ua + t * (ub - ua), ea + t * (eb - ea)
        k = np.argmax(np.abs(ub - ua))                             # control the largest component
        x = np.append(um, em)
        for _ in range(30):                                        # Newton with u_k fixed
            r = m.residual(x[:-1], x[-1])
            A = np.column_stack([m.tangent(x[:-1]), -m.p])
            A = np.vstack([A, np.eye(len(x))[k]]); rhs = np.append(-r, 0.0)
            x = x + solve(A, rhs)
            if np.linalg.norm(r) < 1e-13: break
        um, em = x[:-1], x[-1]
        if negative_pivots(m.tangent(um)) == na: ua, ea = um, em
        else: ub, eb = um, em
        if np.linalg.norm(ub - ua) + abs(eb - ea) < tol: break
    uc, ec = (ua + ub) / 2, (ea + eb) / 2
    lam, V = np.linalg.eigh(m.tangent(uc))
    mode = V[:, 0]
    kind = "limit point" if abs(mode @ m.p) > 1e-6 * np.linalg.norm(m.p) else "bifurcation"
    return uc, ec, mode, kind

def switch(m, uc, ec, mode, ds, tol=1e-12):
    """Branch switching: step ds along the mode, corrector on the plane mode.(u - u_c) = ds."""
    u, eta = uc + ds * mode, ec
    for _ in range(30):
        r = m.residual(u, eta)
        if np.linalg.norm(r) < tol: break
        A = np.vstack([np.column_stack([m.tangent(u), -m.p]), np.append(mode, 0.0)])
        dx = solve(A, np.append(-r, 0.0))
        u, eta = u + dx[:-1], eta + dx[-1]
    return u, eta

def von_mises(phi_deg, e=0.0):
    """Two-bar truss of Chapter 2: supports (-c, 0), (c, 0), apex (0, s); EA = L = 1.
    Free dofs: apex (u_x, u_y) = (u, -v). Load eta downwards plus a sideways load e eta."""
    s, c = np.sin(np.radians(phi_deg)), np.cos(np.radians(phi_deg))
    return Bars([(-c, 0), (c, 0), (0, s)], [(0, 2), (1, 2)], 1.0, [4, 5], [e, -1.0])

if __name__ == "__main__":
    m = von_mises(30)
    print("K0 =", m.K0().round(4).tolist(), " K_sigma =", m.Ksigma().round(4).tolist())
    print("linear buckling loads:", linear_buckling(m)[0].round(4))
