# plate_residual.py -- Chapter 5: a welded plate that buckles under its own residual stresses (no load).
# Run: python3 plate_residual.py     (NumPy, SciPy). Numbers of Section 5.6 and its exercises.
# Simply supported plate a x b, thickness t. Residual stress sigma_x(y) only, compression positive:
# tension sigma_t in two bands of width c along the welded edges y = 0 and y = b, compression sigma_c
# in between, with sigma_c (b - 2c) = 2 c sigma_t (no force). The residual field is scaled by eta and the
# linear buckling eigenproblem K a = eta G a of Chapter 3 is solved by Ritz with sine modes.
import numpy as np
from scipy.linalg import eigh
from scipy.integrate import quad


def k_residual(c_over_b, aspect=None, N=30):
    """Buckling coefficient k = sigma_c,cr b^2 t / (pi^2 D) of the compression band, minimised over the
    length of the half-waves (long plate). With c = 0 the stress is uniform and k = 4."""
    b = 1.0
    c = c_over_b * b
    sc = 1.0
    st = sc * (b - 2 * c) / (2 * c) if c > 0 else 0.0
    sig = lambda y: sc if c <= y <= b - c else -st
    n = np.arange(1, N + 1)
    # G_np = int_0^b sigma(y) sin(n pi y/b) sin(p pi y/b) dy, piecewise exact by quadrature
    G0 = np.zeros((N, N))
    for i in range(N):
        for j in range(i, N):
            f = lambda y: np.sin(n[i] * np.pi * y) * np.sin(n[j] * np.pi * y)
            v = sum(s * quad(f, lo, hi, limit=200)[0]
                    for s, lo, hi in ((-st, 0, c), (sc, c, b - c), (-st, b - c, b)) if hi > lo)
            G0[i, j] = G0[j, i] = v
    best = np.inf
    lams = [aspect] if aspect else np.linspace(0.2, 2.0, 91)     # half-wave length / b
    for lam in lams:
        q = np.pi / lam                                          # m pi / a
        K = np.diag((q**2 + (n * np.pi)**2)**2) * b / 2          # D = 1 per unit (a/2 cancels)
        G = q**2 * G0                                            # t sigma = eta (D pi^2/b^2 t) ... see below
        mu = eigh(G, K, eigvals_only=True)                       # mu = 1/eta; K is positive definite
        if mu[-1] > 0:                                           # the tension bands make G indefinite
            best = min(best, 1 / mu[-1])
    return best / np.pi**2                                       # sigma_c t b^2/(pi^2 D)


if __name__ == "__main__":
    print(f"check, uniform compression (c = 0): k = {k_residual(0.0):.4f} (exact 4)")
    for cb in (0.05, 0.10, 0.15, 0.20):
        print(f"tension bands c/b = {cb:.2f}: k = {k_residual(cb):.3f}, tension in the bands = "
              f"{(1 - 2*cb)/(2*cb):.2f} x the compression")
    # a welded steel plate, b/t = 100 and 150, bands c/b = 0.1
    E, nu = 210e3, 0.3
    for bt in (60, 100, 150):
        k = k_residual(0.10)
        s = k * np.pi**2 * E / (12 * (1 - nu**2)) / bt**2
        print(f"b/t = {bt}: the compression band buckles on its own at sigma_c = {s:.0f} MPa")
    # thin tube: classical axial buckling stress, local over about sqrt(R t)
    for Rt in (100, 500, 1000):
        print(f"tube R/t = {Rt}: classical stress E/(sqrt(3(1-nu^2)) R/t) = {E/np.sqrt(3*(1-nu**2))/Rt:.0f} MPa,"
              f" half-wave {np.pi/(12*(1-nu**2))**0.25:.2f} sqrt(R t)")
