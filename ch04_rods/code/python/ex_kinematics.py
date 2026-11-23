# ex_kinematics.py -- Chapter 4: three kinematics, three post-buckling laws (Triantafyllidis H3, author's slide 11).
# Run: python3 ex_kinematics.py      (NumPy, SciPy). Pinned column, EI = L = 1, inextensible limit.
# Bending equation for phi = w' (or theta) with N (1 + v') = -P along the beam:
#   small rotations   e = v' + w'^2/2              : phi'' + P phi = 0              (linear: flat branch)
#   "improved"        e = v' + (v'^2 + w'^2)/2     : phi'' + P phi/sqrt(1-phi^2) = 0
#   exact (elastica)  stretch and true curvature   : theta'' + P sin(theta) = 0
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

models = {
    "small rotations": lambda p: p,
    "improved strain": lambda p: p / np.sqrt(1 - p * p),
    "elastica":        np.sin,
}

def miss(f, a0, P):
    """Shoot from the pinned end with end slope a0 and zero moment; return the moment at s = 1."""
    sol = solve_ivp(lambda s, y: [y[1], -P * f(y[0])], (0, 1), [a0, 0], rtol=1e-11, atol=1e-12)
    return sol.y[1, -1]

for name, f in models.items():
    for a0 in (0.05, 0.1, 0.2):
        if name == "small rotations":
            P = np.pi ** 2                      # every amplitude at the same load
        else:
            P = brentq(lambda P: miss(f, a0, P), 0.5 * np.pi ** 2, 1.5 * np.pi ** 2)
        c = (P / np.pi ** 2 - 1) / a0 ** 2
        print(f"{name:16s} end slope {a0:4.2f}: P/P_c = {P/np.pi**2:.6f}, (P/P_c - 1)/a0^2 = {c:+.4f}")
