# ex_ritz_column.py -- Chapter 3: the buckling load of the pinned column as a minimum, Ritz and finite elements.
# Printed in the book from line 4 on. Run: python3 ex_ritz_column.py  (NumPy, SciPy)
# a(w, w) = int EI w''^2,  b(w, w) = int w'^2,  P_c = min a / b = pi^2 EI / L^2  (EI = L = 1).
import numpy as np
from numpy.polynomial import polynomial as Pl
from scipy.linalg import eigh

def ritz_polynomials(M):
    """Trial functions x^k (1 - x), k = 1..M (they vanish at both ends). Exact integrals."""
    basis = [Pl.polymul([0] * k + [1], [1, -1]) for k in range(1, M + 1)]
    integ = lambda p: Pl.polyval(1.0, Pl.polyint(p))
    A = np.array([[integ(Pl.polymul(Pl.polyder(f, 2), Pl.polyder(g, 2))) for g in basis] for f in basis])
    B = np.array([[integ(Pl.polymul(Pl.polyder(f), Pl.polyder(g))) for g in basis] for f in basis])
    return eigh(A, B, eigvals_only=True)[0]

def hermite_fe(n):
    """n Hermite cubic beam elements: element stiffness (bending) and geometric matrices."""
    h, N = 1.0 / n, 2 * (n + 1)
    k = np.array([[12, 6 * h, -12, 6 * h], [6 * h, 4 * h**2, -6 * h, 2 * h**2],
                  [-12, -6 * h, 12, -6 * h], [6 * h, 2 * h**2, -6 * h, 4 * h**2]]) / h**3
    g = np.array([[36, 3 * h, -36, 3 * h], [3 * h, 4 * h**2, -3 * h, -h**2],
                  [-36, -3 * h, 36, -3 * h], [3 * h, -h**2, -3 * h, 4 * h**2]]) / (30 * h)
    A, B = np.zeros((N, N)), np.zeros((N, N))
    for e in range(n):
        d = slice(2 * e, 2 * e + 4); A[d, d] += k; B[d, d] += g
    keep = [i for i in range(N) if i not in (0, N - 2)]    # w = 0 at both ends
    return eigh(A[np.ix_(keep, keep)], B[np.ix_(keep, keep)], eigvals_only=True)

if __name__ == "__main__":
    exact = np.pi**2
    for M in (1, 2, 3, 4):
        P = ritz_polynomials(M)
        print(f"Ritz, {M} polynomial(s): P = {P:.6f}, error {100 * (P / exact - 1):.4f} %")
    prev = None
    for n in (1, 2, 4, 8, 16):
        P = hermite_fe(n)
        err = P[0] / exact - 1
        rate = "" if prev is None else f", rate {np.log2(prev / err):.2f}"
        print(f"Hermite FE, {n:2d} elements: P1 = {P[0]:.6f}, P2 = {P[1]:9.4f} (exact {4 * exact:.4f}),"
              f" error {100 * err:.2e} %{rate}")
        prev = err
