# elastica.py -- Chapter 4: the pinned Euler elastica, exact (elliptic) and by shooting.
# Run: python3 elastica.py      (NumPy, SciPy). Units: EI = L = 1, so P_c = pi^2.
# Uses ../../../ch01_bifurcation/code/python/arclength.py for the continuation.
import os, sys
import numpy as np
from scipy.special import ellipk, ellipe
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ---------- exact solution (Section 4.3): k = sin(theta0/2), m = k^2 ----------
def exact(theta0):
    """P/P_c, mid deflection w/L, end shortening Delta/L for end rotation theta0."""
    m = np.sin(theta0 / 2) ** 2
    K, E = ellipk(m), ellipe(m)
    p = (2 * K / np.pi) ** 2                  # P/P_c, since sqrt(P/EI) L = 2K
    wmid = np.sqrt(m) / K                     # w_max/L = 2k sqrt(EI/P)/L = k/K
    delta = 2 - 2 * E / K                     # Delta/L = 1 - x(L)/L
    return p, wmid, delta

def shape(theta0, n=201):
    """Coordinates x(s), w(s) of the exact shape (by integrating the ODE)."""
    p, _, _ = exact(theta0)
    return integrate(theta0, p * np.pi ** 2, n)

# ---------- shooting (Exercise "Computer: the elastica by shooting") ----------
def integrate(theta0, P, n=201):
    """theta'' = -P sin(theta), theta(0) = theta0, theta'(0) = 0 (pinned end, no moment)."""
    rhs = lambda s, y: [y[1], -P * np.sin(y[0]), np.cos(y[0]), np.sin(y[0])]
    sol = solve_ivp(rhs, (0, 1), [theta0, 0, 0, 0], t_eval=np.linspace(0, 1, n),
                    rtol=1e-11, atol=1e-12)
    return sol.y[2], sol.y[3]                 # x(s), w(s)

def miss(theta0, P):
    """Shooting residual: the far end must have no moment, theta'(1) = 0."""
    rhs = lambda s, y: [y[1], -P * np.sin(y[0])]
    sol = solve_ivp(rhs, (0, 1), [theta0, 0], rtol=1e-11, atol=1e-12)
    return sol.y[1, -1]

def shoot(theta0):
    """First load P > P_c for which the shot lands with zero moment at s = 1."""
    p_exact = exact(theta0)[0] * np.pi ** 2
    return brentq(lambda P: miss(theta0, P), np.pi ** 2 * 1.0000001, 1.5 * p_exact + 1)

if __name__ == "__main__":
    print("theta0   P/Pc exact   P/Pc shoot   Koiter 1+t^2/8   w/L      Delta/L")
    for deg in (10, 20, 40, 60, 90, 120, 130.7, 150, 170):
        t = np.radians(deg)
        p, wm, d = exact(t)
        ps = shoot(t) / np.pi ** 2
        print(f"{deg:6.1f}  {p:11.6f}  {ps:11.6f}  {1 + t*t/8:13.6f}  {wm:7.4f}  {d:8.4f}")
    # ends touch when x(L) = 0, i.e. 2E(m) = K(m)
    m = brentq(lambda m: 2 * ellipe(m) - ellipk(m), 0.5, 0.99)
    print(f"ends touch: theta0 = {np.degrees(2*np.arcsin(np.sqrt(m))):.2f} deg, "
          f"P/Pc = {(2*ellipk(m)/np.pi)**2:.4f}")
    # one per cent above P_c
    t1 = brentq(lambda t: exact(t)[0] - 1.01, 0.01, 1.0)
    print(f"P/Pc = 1.01 at theta0 = {np.degrees(t1):.2f} deg, w/L = {exact(t1)[1]:.4f}")
    # continuation of the shooting residual with the code of Chapter 1
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "ch01_bifurcation", "code", "python"))
    from arclength import continuation
    F = lambda x: np.array([miss(x[0], x[1])])          # unknowns (theta0, P)
    t0 = 0.05
    X = continuation(F, [t0, exact(t0)[0] * np.pi ** 2], [1.0, 0.0], 0.1, 160)[0]
    X = np.array(X)
    err = max(abs(X[i, 1] / np.pi ** 2 - exact(X[i, 0])[0]) for i in range(len(X)))
    print(f"continuation: {len(X)} points up to theta0 = {np.degrees(X[-1,0]):.1f} deg, "
          f"max |P/Pc - exact| = {err:.2e}")
