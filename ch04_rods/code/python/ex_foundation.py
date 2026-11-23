# ex_foundation.py -- Chapter 4: beam on an elastic (Winkler) foundation.
# Run: python3 ex_foundation.py     (NumPy, SymPy). Wavelength selection, mode jumps,
# post-buckling of the elastica with and without the foundation (two-harmonic Ritz).
import numpy as np
import sympy as sp

# 1. Linear buckling: P(q) = EI q^2 + k/q^2. Units EI = k = 1: q_c = 1, P_c = 2.
#    Finite pinned beam of length L: q = n pi/L, P_n/P_c = (m^2 + 1/m^2)/2, m = n pi/L.
#    The first mode jumps from n to n+1 where P_n = P_{n+1}: L/pi = sqrt(n (n+1)).
for n in range(1, 5):
    print(f"mode {n} -> {n+1} at L/pi = sqrt({n*(n+1)}) = {np.sqrt(n*(n+1)):.4f}")
Pn = lambda n, L: 0.5 * ((n * np.pi / L) ** 2 + (L / (n * np.pi)) ** 2)
for L in (2.0, 5.0, 10.0, 30.0):
    n = min(range(1, 40), key=lambda n: Pn(n, L))
    print(f"L = {L:5.1f}: first mode n = {n:2d}, P/P_c = {Pn(n, L):.4f}, "
          f"half-wavelength L/n = {L/n:.3f} (pi = {np.pi:.3f})")

# 2. Post-buckling, two-harmonic Ritz with the quartic energy in the arclength s.
#    w' = sin(theta): theta'^2 = w''^2 (1 + w'^2), 1 - cos(theta) = w'^2/2 + w'^4/8,
#    springs per unit base length: dx = cos(theta) ds = (1 - w'^2/2) ds.
s, A, B, P = sp.symbols("s A B P", real=True)

def path(found, period, P0):
    w = A * sp.cos(s) + B * sp.cos(3 * s)
    wp, wpp = sp.diff(w, s), sp.diff(w, s, 2)
    dens = sp.Rational(1, 2) * wpp**2 * (1 + wp**2) - P * (wp**2 / 2 + wp**4 / 8)
    if found:
        dens += sp.Rational(1, 2) * w**2 * (1 - wp**2 / 2)
    E = sp.integrate(sp.expand(dens), (s, 0, period))
    b = sp.solve(sp.diff(E, B).subs(P, P0), B)[0]            # B = O(A^3)
    E2 = sp.series(E.subs(B, b), A, 0, 5).removeO()
    return sp.simplify(sp.solve(sp.diff(E2, A) / A, P)[0] / P0)

free = path(False, 2 * sp.pi, 1)          # pinned column, L = pi: w = A cos s on a half-wave
found = path(True, 2 * sp.pi, 2)          # periodic beam on the foundation
print("free elastica:   P/P_c =", free, " ~ 1 +", sp.series(free, A, 0, 3).coeff(A, 2), "A^2")
print("with foundation: P/P_c =", found, " ~ 1 +", sp.series(found, A, 0, 3).coeff(A, 2), "A^2")

# 3. A rail as an order of magnitude (vertical bending, crude Winkler model), UIC 60.
E, I, Ar, alpha, k = 210e9, 3055e-8, 76.7e-4, 1.2e-5, 30e6   # SI; k per unit length per rail
Pc = 2 * np.sqrt(k * E * I)
lam = 2 * np.pi * (E * I / k) ** 0.25
print(f"rail: P_c = {Pc/1e3:.0f} kN, wavelength {lam:.2f} m, "
      f"temperature rise for P_c: {Pc/(E*Ar*alpha):.0f} K")
