# ex_bearing.py -- Chapter 3: a shear-soft column (laminated rubber bearing) buckles in compression AND in tension.
# Printed in the book from line 4 on. Run: python3 ex_bearing.py  (NumPy, SciPy)
# Timoshenko beam, fields w (deflection) and theta (rotation of the plates); geometric form of Engesser or of Haringx.
import numpy as np
from scipy.linalg import eig

def matrices(n, L, EI, GA, form):
    """Linear elements for w and theta, one Gauss point for the shear term (no locking).
    a(v, v) = int EI theta'^2 + GA (w' - theta)^2 ;  b(v, v) = int w'^2 (Engesser) or w'^2 - (w' - theta)^2 (Haringx)."""
    h, N = L / n, 2 * (n + 1)                        # dofs (w_0, theta_0, w_1, theta_1, ...)
    A, B = np.zeros((N, N)), np.zeros((N, N))
    for e in range(n):
        d = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
        dw = np.array([-1, 0, 1, 0]) / h             # w' on the element
        dtheta = np.array([0, -1, 0, 1]) / h           # theta'
        theta = np.array([0, 0.5, 0, 0.5])             # theta at the midpoint
        gam = dw - theta                               # shear strain gamma = w' - theta
        ke = h * (EI * np.outer(dtheta, dtheta) + GA * np.outer(gam, gam))
        ge = h * np.outer(dw, dw)
        if form == "haringx": ge -= h * np.outer(gam, gam)
        A[np.ix_(d, d)] += ke; B[np.ix_(d, d)] += ge
    keep = [i for i in range(N) if i not in (0, 1, N - 1)]   # bearing: w(0) = 0, theta = 0 at both ends,
    return A[np.ix_(keep, keep)], B[np.ix_(keep, keep)]       # the top plate sways freely

def critical_loads(n, L, EI, GA, form):
    """a(v, v) = P b(v, v): the smallest positive P (compression) and the negative P closest to 0 (tension)."""
    A, B = matrices(n, L, EI, GA, form)
    P = eig(A, B, right=False)
    P = np.real(P[np.isfinite(P) & (np.abs(np.imag(P)) < 1e-9)])
    comp = P[P > 0].min()
    tens = P[P < 0].max() if np.any(P < 0) else None
    return comp, tens

if __name__ == "__main__":
    L, EI = 1.0, 1.0
    PE = np.pi**2 * EI / L**2
    for GA in [100.0, 10.0, 1.0]:                    # from a stiff column to a shear-soft bearing
        r = 1 + 4 * PE / GA
        haringx = (GA / 2 * (np.sqrt(r) - 1), -GA / 2 * (np.sqrt(r) + 1))
        engesser = PE / (1 + PE / GA)
        e = critical_loads(400, L, EI, GA, "engesser")
        h = critical_loads(400, L, EI, GA, "haringx")
        print(f"GA/P_E = {GA / PE:6.3f} | Engesser {engesser:7.4f}  FE {e[0]:7.4f}  tension {e[1]}"
              f" | Haringx {haringx[0]:7.4f} {haringx[1]:8.4f}  FE {h[0]:7.4f} {h[1]:8.4f}"
              f" | sqrt(P_E GA) {np.sqrt(PE * GA):7.4f}")
