# ex_columns.py -- Chapter 4: Euler loads, effective lengths, the imperfect column, secant design.
# Run: python3 ex_columns.py     (NumPy, SciPy). All numbers of Section 4.2 and its exercises.
# Design data in SI after Hibbeler, Mechanics of Materials, Ch. 13 (Eqs. 13-5, 13-11, 13-19).
import numpy as np
from scipy.optimize import brentq

# 1. Four supports: the smallest root of the characteristic equation, P/(pi^2 EI/L^2).
#    w = C1 sin qx + C2 cos qx + C3 x + C4, q^2 = P/EI, L = 1.
roots = {
    "pinned-pinned":   np.pi,                                    # sin q = 0
    "clamped-pinned":  brentq(lambda q: np.tan(q) - q, 4.0, 4.6),  # tan q = q
    "clamped-clamped": 2 * np.pi,                                # sin(q/2) = 0, symmetric mode
    "clamped-free":    np.pi / 2,                                # cos q = 0
}
print("support            qL        P/(pi^2EI/L^2)   K = pi/qL")
for name, q in roots.items():
    print(f"{name:17s} {q:8.5f}   {(q/np.pi)**2:10.5f}      {np.pi/q:6.4f}")

# 2. The imperfect pinned column, w_bar = a sin(pi x/L): w = a p/(1 - p), p = P/P_c.
#    Southwell: delta/P = delta/P_c + a/P_c is a straight line in delta.
a = 0.002                                     # initial bow, 1/500 of the length
for p in (0.25, 0.5, 0.75, 0.9, 0.95):
    print(f"p = {p:4.2f}: added deflection {a*p/(1-p):.5f} L, amplification {1/(1-p):6.2f}")
P = np.array([0.5, 0.7, 0.8, 0.9])
delta = a * P / (1 - P)
slope = np.polyfit(delta, delta / P, 1)[0]
print(f"Southwell: slope of delta/P against delta = {slope:.6f} -> P_c = {1/slope:.6f}")

# 3. A steel tube in SI. Euler stress, limiting slenderness, secant formula.
E, sY = 200e9, 250e6                          # Pa
D, t, L = 0.1143, 0.006, 4.0                  # m: CHS 114.3 x 6, length 4 m
A = np.pi / 4 * (D**2 - (D - 2*t)**2)
I = np.pi / 64 * (D**4 - (D - 2*t)**4)
r = np.sqrt(I / A); c = D / 2
print(f"tube: A = {A*1e4:.2f} cm2, I = {I*1e8:.1f} cm4, r = {r*1e3:.1f} mm, L/r = {L/r:.1f}")
print(f"limiting slenderness (Euler stress = yield): {np.pi*np.sqrt(E/sY):.1f}")
for K, name in ((1.0, "pinned"), (0.7, "clamped-pinned"), (2.0, "clamped-free")):
    Pcr = np.pi**2 * E * I / (K * L)**2
    print(f"  {name:14s} K = {K}: P_cr = {Pcr/1e3:7.1f} kN, sigma_cr = {Pcr/A/1e6:6.1f} MPa")
Pc = np.pi**2 * E * I / L**2
for e in (0.002, 0.010, 0.020):                # eccentricity (m)
    smax = lambda P: P / A * (1 + e * c / r**2 / np.cos(L / (2 * r) * np.sqrt(P / (E * A))))
    Py = brentq(lambda P: smax(P) - sY, 1.0, Pc * 0.99999)
    print(f"secant formula, pinned, e = {e*1e3:2.0f} mm: first yield at P = {Py/1e3:.1f} kN "
          f"= {Py/Pc:.3f} P_c (squash load {sY*A/1e3:.1f} kN)")
