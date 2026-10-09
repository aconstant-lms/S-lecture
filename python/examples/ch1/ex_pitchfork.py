# Chapter 1 -- pitchfork y' = r y - y^3: where the solution settles, and how slowly.
# Printed in the book from line 4 on (\lstinputlisting[firstline=4]).
# Run: python3 ex_pitchfork.py
import numpy as np
from scipy.integrate import solve_ivp

def f(t, y, r):
    return r * y - y**3

# 1. Final state for each r, after a small push to the left and to the right.
for r in [-0.5, -0.1, 0.1, 0.5, 1.0]:
    ends = [solve_ivp(f, [0, 200], [y0], args=(r,), rtol=1e-9).y[0, -1]
            for y0 in (-0.01, 0.01)]
    print(f"r = {r:5.2f}   final y = {ends[0]:+.4f}, {ends[1]:+.4f}"
          f"   sqrt(r) = {np.sqrt(max(r, 0.0)):.4f}")

# 2. Critical slowing down: time to fall from y = 1 to y = 0.1.
def reach(t, y, r):
    return y[0] - 0.1
reach.terminal = True

for r in [-1.0, -0.1, -0.01, 0.0]:
    sol = solve_ivp(f, [0, 1e4], [1.0], args=(r,), events=reach, rtol=1e-9)
    print(f"r = {r:6.2f}   time to reach 0.1: {sol.t_events[0][0]:7.2f}")
