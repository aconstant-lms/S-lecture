# Chapter 1 -- imperfect pitchfork y' = h + y - y^3: slow sweep of h up and down.
# Printed in the book from line 4 on (\lstinputlisting[firstline=4]).
# Run: python3 ex_hysteresis.py
import numpy as np
from scipy.integrate import solve_ivp

def f(t, y, h):
    return h + y - y**3

def sweep(hs, y):
    """Follow the steady state while h takes the values hs, one after the other."""
    ys = []
    for h in hs:
        y = solve_ivp(f, [0, 100], [y], args=(h,), rtol=1e-9).y[0, -1]
        ys.append(y)
    return np.array(ys)

h_up = np.arange(-1.0, 1.0 + 1e-9, 0.005)
y_up = sweep(h_up, -1.3)                   # start on the lower branch
h_down = h_up[::-1]
y_down = sweep(h_down, y_up[-1])           # come back from the upper branch

i = np.argmax(np.abs(np.diff(y_up)))
j = np.argmax(np.abs(np.diff(y_down)))
print(f"jump up   between h = {h_up[i]:.3f} and {h_up[i+1]:.3f}: "
      f"y from {y_up[i]:+.3f} to {y_up[i+1]:+.3f}")
print(f"jump down between h = {h_down[j]:.3f} and {h_down[j+1]:.3f}: "
      f"y from {y_down[j]:+.3f} to {y_down[j+1]:+.3f}")
print(f"theory: h_c = 2/(3 sqrt 3) = {2 / (3 * np.sqrt(3)):.3f}")
