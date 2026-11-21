# Chapter 1 -- pseudo-arclength continuation of F(y, r) = 0, written from scratch.
# Printed in the book from line 4 on (\lstinputlisting[firstline=4]).
# Run: python3 arclength.py
import numpy as np

def jacobian(F, x, eps=1e-7):
    """[J  F_r]: the n x (n+1) matrix dF/dx by central differences, x = (y, r)."""
    cols = []
    for j in range(len(x)):
        e = np.zeros(len(x)); e[j] = eps
        cols.append((F(x + e) - F(x - e)) / (2 * eps))
    return np.column_stack(cols)

def tangent(F, x, t_old):
    """Unit tangent t: [J F_r] t = 0, oriented so that t . t_old > 0."""
    A = np.vstack([jacobian(F, x), t_old])
    rhs = np.zeros(len(x)); rhs[-1] = 1.0
    t = np.linalg.solve(A, rhs)
    return t / np.linalg.norm(t)

def monitors(F, x, t):
    """det J (a zero eigenvalue) and det of the augmented Jacobian (branch points)."""
    JF = jacobian(F, x)
    return np.linalg.det(JF[:, :-1]), np.linalg.det(np.vstack([JF, t]))

def continuation(F, x0, t_guess, ds, nsteps, tol=1e-10, maxit=10):
    """Follow the curve F(x) = 0 from x0, starting in the direction of t_guess (Box 1.2)."""
    x = np.array(x0, float)
    t = tangent(F, x, np.array(t_guess, float))
    X, T, M = [x], [t], [monitors(F, x, t)]
    for k in range(nsteps):
        xp = x + ds * t                                # 1. predictor
        for it in range(maxit):                        # 2. Newton corrector
            R = np.append(F(xp), t @ (xp - x) - ds)    #    residual of the augmented system
            A = np.vstack([jacobian(F, xp), t])        #    augmented Jacobian
            dx = np.linalg.solve(A, -R)
            xp = xp + dx
            if np.linalg.norm(dx) < tol:
                break
        else:
            raise RuntimeError(f"no convergence at step {k}: reduce ds")
        x, t = xp, tangent(F, xp, t)                   # 3. new tangent
        X.append(x); T.append(t); M.append(monitors(F, x, t))   # 4. monitor
    return np.array(X), np.array(T), np.array(M)

def zeros(X, v):
    """Points where the monitor v changes sign, by linear interpolation."""
    i = np.flatnonzero(np.sign(v[:-1]) != np.sign(v[1:]))
    a = v[i] / (v[i] - v[i + 1])
    return X[i] + a[:, None] * (X[i + 1] - X[i])

if __name__ == "__main__":
    # 1. The S-curve y' = h + y - y^3, x = (y, h). A fold is where t_h changes sign.
    F = lambda x: np.array([x[1] + x[0] - x[0]**3])
    X, T, M = continuation(F, [-1.3, -1.3**3 + 1.3], [0, 1], 0.05, 70)
    for y, h in zeros(X, T[:, 1]):
        print(f"S-curve: fold at y = {y:+.4f}, h = {h:+.4f}")
    print(f"  theory: y = -+{1 / np.sqrt(3):.4f}, h = +-{2 / (3 * np.sqrt(3)):.4f}")
    print(f"  sign changes: det J {len(zeros(X, M[:, 0]))}, "
          f"augmented det {len(zeros(X, M[:, 1]))}")

    # 2. Imperfect bar, x = (theta, p), p = P/P_c: (theta - theta0) - p sin(theta) = 0.
    th0 = 0.1
    G = lambda x: np.array([x[0] - th0 - x[1] * np.sin(x[0])])
    th = -2.5
    X, T, M = continuation(G, [th, (th - th0) / np.sin(th)], [1, 0], 0.05, 100)
    for th, p in zeros(X, T[:, 1]):
        print(f"imperfect bar, theta0 = {th0}: fold of the complementary branch "
              f"at theta = {th:+.4f}, p = {p:.4f}")

    # 3. Perfect bar: follow the straight state theta = 0, detect the branch point
    #    (sign change of the augmented determinant), then step onto the buckled branch.
    H = lambda x: np.array([x[0] - x[1] * np.sin(x[0])])
    X, T, M = continuation(H, [0.0, 0.0], [0, 1], 0.1, 15)
    xb = zeros(X, M[:, 1])[0]
    print(f"perfect bar: branch point at p = {xb[1]:.4f} (theory 1)")
    tb = np.array([1.0, 0.0])                          # orthogonal to the straight branch
    Xb, Tb, Mb = continuation(H, xb + 0.05 * tb, tb, 0.1, 15)
    err = np.max(np.abs(Xb[1:, 1] - Xb[1:, 0] / np.sin(Xb[1:, 0])))
    print(f"  buckled branch up to theta = {Xb[-1, 0]:.2f}, p = {Xb[-1, 1]:.4f}; "
          f"max |p - theta/sin(theta)| = {err:.1e}")
