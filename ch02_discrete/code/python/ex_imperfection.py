# ex_imperfection.py -- Chapter 2: imperfection-sensitivity curves, exact against asymptotic.
# Run: python3 ex_imperfection.py   (NumPy, SciPy; part 2 reuses Chapter 1's arclength.py)
# Loads are scaled by the critical load; xi_bar is the initial tilt (or Augusti's eps).
import os, sys
import numpy as np
from scipy.optimize import minimize_scalar

# --- 1. exact equilibrium paths p(theta) = P/P_c of the imperfect systems -------------
def p_lateral(th, th0):          # bar with a horizontal spring, tilt th0 (unstable symmetric)
    return (1 - np.sin(th0) / np.sin(th)) * np.cos(th)

def p_inclined(th, th0):         # bar with a 45-degree spring, tilt th0 (asymmetric)
    l = lambda t: np.sqrt((np.sin(t) + 1)**2 + np.cos(t)**2)       # spring length / L
    dl = lambda t: np.cos(t) / l(t)                                 # d l / d theta
    return (l(th) - l(th0)) * dl(th) / np.sin(th) / 0.5            # P_c = kL/2

def p_augusti(u, eps):           # Augusti column, equal springs, 45-degree plane
    return (1 - eps / u) / (1 + u**2 / 3)

def max_load(p, th0, hi=1.5):
    """Largest load on the natural path, which starts at th0 and grows with theta."""
    r = minimize_scalar(lambda t: -p(t, th0), bounds=(th0 * 1.0001, hi), method="bounded")
    return -r.fun

# --- 2. asymptotic power laws (Section "Imperfection sensitivity") -------------------
law_half = lambda xb, eta1: 1 - 2 * np.sqrt(-eta1 * xb)                 # eta1 in units of eta_c
law_23 = lambda xb, eta2: 1 - 1.5 * (-eta2)**(1 / 3) * np.abs(xb)**(2 / 3)

if __name__ == "__main__":
    print(" xi_bar   inclined: exact  1/2-law | lateral: exact  2/3-law | Augusti: exact  2/3-law")
    for xb in [1e-4, 1e-3, 1e-2, 3e-2]:
        print(f"{xb:7.0e}   {max_load(p_inclined, xb):14.4f} {law_half(xb, -0.75):8.4f} |"
              f" {max_load(p_lateral, xb):13.4f} {law_23(xb, -1.0):8.4f} |"
              f" {max_load(p_augusti, xb):13.4f} {law_23(xb, -2 / 3):8.4f}")

    # --- 3. the steep two-bar truss (phi = 65 deg) with a sideways load, by continuation
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "ch01_bifurcation", "code", "python"))
    from arclength import continuation, zeros
    phi = np.radians(65); s, c = np.sin(phi), np.cos(phi)
    def F(x, e):                  # x = (u, v, lam), EA = L = 1; horizontal force e*lam
        u, v, lam = x
        e1 = ((c + u)**2 + (s - v)**2 - 1) / 2
        e2 = ((c - u)**2 + (s - v)**2 - 1) / 2
        return np.array([e1 * (u + c) + e2 * (u - c) - e * lam,
                         e1 * (v - s) + e2 * (v - s) - lam])
    R = np.sqrt(3 * s**2 - 2)
    print(f"\ntwo-bar truss, phi = 65 deg: bifurcation at lam = {2 * c**2 * R:.4f},"
          f" limit point of the symmetric path at lam = {2 / (3 * np.sqrt(3)) * s**3:.4f}")
    for e in [1e-4, 1e-3, 1e-2]:
        X, T, M = continuation(lambda x: F(x, e), [0, 0, 0], [0, 0, 1], 0.01, 400)
        lam_max = zeros(X, T[:, 2])[0][2]
        print(f"  sideways load {e:5.0e} x lam: maximum load {lam_max:.4f}")
