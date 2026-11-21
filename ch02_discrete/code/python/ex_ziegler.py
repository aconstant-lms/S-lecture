# ex_ziegler.py -- Chapter 2: Ziegler's column under a follower load, with and without damping.
# Run: python3 ex_ziegler.py   (NumPy).  Units: m = k = l = 1, p = P l / k, damping c.
# Masses 2m (joint) and m (tip), springs k, angles of the two bars from the vertical.
import numpy as np

M = np.array([[3.0, 1.0], [1.0, 1.0]])                 # mass matrix / (m l^2)
C0 = np.array([[2.0, -1.0], [-1.0, 1.0]])              # dampers in the two hinges

def K(p):
    """Linearised stiffness / k: springs minus the follower load (not symmetric)."""
    return np.array([[2.0 - p, -1.0 + p], [-1.0, 1.0]])

def growth_rates(p, c=0.0):
    """Eigenvalues of the first-order system for (angles, angular velocities)."""
    A = np.block([[np.zeros((2, 2)), np.eye(2)],
                  [-np.linalg.solve(M, K(p)), -np.linalg.solve(M, c * C0)]])
    return np.linalg.eigvals(A)

def critical(c, p_hi=4.0, n=4000):
    """First load at which a growth rate gets a positive real part (then bisection)."""
    ps = np.linspace(1e-3, p_hi, n)
    unstable = [growth_rates(p, c).real.max() > 1e-12 for p in ps]
    i = unstable.index(True)
    a, b = ps[i - 1], ps[i]
    for _ in range(50):
        mid = (a + b) / 2
        a, b = (a, mid) if growth_rates(mid, c).real.max() > 1e-12 else (mid, b)
    return (a + b) / 2

if __name__ == "__main__":
    print(f"det K(p) = {np.linalg.det(K(0.7)):.3f} for every p: no divergence, no adjacent equilibrium")
    # undamped: det(K - w^2 M) = 2 s^2 + (2p - 7) s + 1 with s = w^2
    for p in [0.0, 1.0, 2.0, 2.1]:
        s = np.roots([2, 2 * p - 7, 1])
        print(f"p = {p:3.1f}: omega^2 = {np.round(s, 4)}")
    print(f"flutter, undamped : p_f = {critical(0.0):.5f}   (7/2 - sqrt 2 = {3.5 - np.sqrt(2):.5f})")
    for c in [1e-1, 1e-2, 1e-3, 1e-4]:
        print(f"flutter, c = {c:6.0e}: p_f = {critical(c):.5f}")
