# ex_stability.py -- Chapter 4: stability of the elastica branches by the second variation (a numerical look).
# Run: python3 ex_stability.py      (NumPy, SciPy). Pinned column, EI = L = 1, P_c = pi^2.
# Second variation  Q[v] = int (v'^2 - P cos(theta) v^2) ds  on the variations v that keep the far pin on the
# axis: int cos(theta) v ds = 0 (linearised w(1) = int sin(theta) ds = 0). Natural conditions v free at the ends.
import numpy as np
from scipy.special import ellipk, ellipj
from scipy.linalg import eigh, null_space

def branch(n, theta0):
    """Mode-n pinned elastica with end rotation theta0: theta(s) at the nodes, and P."""
    m = np.sin(theta0 / 2) ** 2
    q = 2 * n * ellipk(m)                          # sqrt(P): n half-swings in the length 1
    return (lambda s: 2 * np.arcsin(np.sqrt(m) * ellipj(q * s + ellipk(m), m)[0])), q ** 2

def spectrum(theta, P, ne=800, nev=4):
    """Lowest eigenvalues of the constrained second variation (P1 elements, mass-normalised)."""
    s = np.linspace(0, 1, ne + 1); h = 1 / ne
    sm = 0.5 * (s[:-1] + s[1:]); c = np.cos(theta(sm))           # midpoint rule per element
    K = np.zeros((ne + 1, ne + 1)); M = np.zeros_like(K); G = np.zeros_like(K); b = np.zeros(ne + 1)
    for e in range(ne):
        i = [e, e + 1]
        K[np.ix_(i, i)] += np.array([[1, -1], [-1, 1]]) / h
        Me = np.array([[2, 1], [1, 2]]) * h / 6
        M[np.ix_(i, i)] += Me; G[np.ix_(i, i)] += c[e] * Me
        b[i] += c[e] * h / 2
    Z = null_space(b[None, :])                                   # variations that respect the constraint
    lam = eigh(Z.T @ (K - P * G) @ Z, Z.T @ M @ Z, eigvals_only=True)
    return lam[:nev]

if __name__ == "__main__":
    print("straight column: number of negative eigenvalues")
    for p in (0.5, 1.5, 3.0, 5.0, 10.0):
        lam = spectrum(lambda s: 0 * s, p * np.pi**2, nev=6)
        print(f"  P/Pc = {p:4.1f}: {int((lam < 0).sum())} negative, lowest {lam[0]:+.3f}")
    for n in (1, 2, 3):
        print(f"mode {n} branch:  theta0   P/Pc     lowest eigenvalues        negative")
        for deg in (5, 30, 60, 90, 120, 128, 130.71, 133, 150, 170):
            th, P = branch(n, np.radians(deg))
            lam = spectrum(th, P)
            print(f"            {deg:7.2f}  {P/np.pi**2:7.3f}   " + " ".join(f"{x:+9.3f}" for x in lam[:3])
                  + f"     {int((lam < -1e-6).sum())}")
    # where does the first branch lose stability? bisection on the lowest eigenvalue
    f = lambda d: spectrum(*branch(1, np.radians(d)))[0]
    a, b = 120.0, 140.0
    for _ in range(30):
        c = 0.5 * (a + b); a, b = (c, b) if f(c) > 0 else (a, c)
    print(f"mode 1 loses stability at theta0 = {0.5*(a+b):.3f} deg (ends touch at 130.709 deg)")
