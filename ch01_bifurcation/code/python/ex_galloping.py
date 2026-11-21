# Chapter 1 -- galloping of a square prism: Hopf point and amplitude, checked by integration.
# Printed in the book from line 4 on (\lstinputlisting[firstline=4]).
# Run: python3 ex_galloping.py
import numpy as np
from scipy.integrate import solve_ivp

rho, d, m = 1.25, 0.10, 10.0           # air density kg/m^3, side m, mass per length kg/m
w, zeta = 2 * np.pi * 2.0, 0.005        # natural frequency 2 Hz, damping ratio
A1, A3 = 2.69, 168.0                    # lift polynomial C_y = A1 a - A3 a^3 (Parkinson & Smith)

Uc = 4 * m * zeta * w / (rho * d * A1)
print(f"critical wind speed U_c = {Uc:.2f} m/s")

def amplitude(U):
    """Energy balance (first Lyapunov coefficient): A^2 = 4 gamma / (3 beta w^2)."""
    gamma = rho * d * A1 * U / (2 * m) - 2 * zeta * w
    beta = rho * d * A3 / (2 * m * U)
    return np.sqrt(max(gamma, 0.0) * 4 / (3 * beta * w**2))

def simulate(U, T=1500.0):
    def rhs(t, z):
        x, v = z
        force = rho * d / (2 * m) * (A1 * U * v - A3 * v**3 / U)
        return [v, -w**2 * x - 2 * zeta * w * v + force]
    s = solve_ivp(rhs, [0, T], [0.01, 0], rtol=1e-8, atol=1e-10, max_step=0.01)
    return np.max(np.abs(s.y[0, s.t > T - 20]))

for U in [0.9 * Uc, 1.1 * Uc, 1.5 * Uc, 2.0 * Uc]:
    print(f"U = {U:5.2f} m/s   amplitude: theory {amplitude(U):.4f} m, "
          f"integration {simulate(U):.4f} m")
