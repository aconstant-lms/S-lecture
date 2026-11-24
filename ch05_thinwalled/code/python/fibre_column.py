# fibre_column.py -- Chapter 5: maximum load of a bowed, residually stressed, elastic-plastic column.
# Run: python3 fibre_column.py     (NumPy, SciPy). The column curves of Section 5.5.
# Pinned H-section column, initial bow v0 sin(pi x/L), deflected shape kept sinusoidal: the mid-section
# carries N = P and M = P (v0 + v) with curvature pi^2 v / L^2 (Jezek's approximation). Fibres are
# elastic-perfectly plastic with elastic unloading; compression is positive.
import numpy as np
from scipy.optimize import brentq

E, fy = 210e3, 235.0                        # MPa
h, b, tf, tw = 300.0, 300.0, 19.0, 11.0     # HEB 300 (mm), without the root fillets


def fibres(axis, n=60):
    """Fibre areas, the coordinate y along the bending direction, and the Lehigh residual stress (/fy)."""
    hw = h - 2 * tf
    yf = (np.arange(n) + 0.5) / n * b - b / 2        # across a flange
    yw = (np.arange(n) + 0.5) / n * hw - hw / 2      # along the web
    Af, Aw = b * tf / n, hw * tw / n
    # flanges: compression c at the tips, tension at the centre, linear; web: uniform tension.
    c = 0.3
    t_ = c * b * tf / (b * tf + hw * tw)             # self-equilibrium: 2 b tf (t_ - c)/2 + hw tw t_ = 0
    sf = c - (c + t_) * (1 - 2 * np.abs(yf) / b)     # +c at |y| = b/2, -t_ at y = 0
    sw = -t_ * np.ones(n)
    if axis == "weak":                               # bending in the plane of the flanges
        y = np.concatenate([yf, yf, np.zeros(n)])
    else:                                            # bending in the plane of the web
        y = np.concatenate([np.full(n, (hw + tf) / 2), np.full(n, -(hw + tf) / 2), yw])
    A = np.concatenate([np.full(2 * n, Af), np.full(n, Aw)])
    s0 = fy * np.concatenate([sf, sf, sw])
    return A, y, s0


def max_load(lam_bar, axis, residual=True, bow=1 / 1000, steps=400):
    A, y, s0 = fibres(axis)
    if not residual:
        s0 = 0 * s0
    Atot = A.sum()
    I = (A * y**2).sum()
    lam1 = np.pi * np.sqrt(E / fy)
    L = lam_bar * lam1 * np.sqrt(I / Atot)
    v0 = bow * L
    ep = np.zeros_like(A)                            # plastic strain of each fibre
    sig = lambda e, ep: np.clip(s0 + E * (e - ep), -fy, fy)
    Pmax, vmax = 0.0, 0.6 * L / 100 + 5 * v0
    e0 = 0.0
    for v in np.linspace(0, vmax, steps)[1:]:
        k = np.pi**2 * v / L**2
        def g(e0):
            s = sig(e0 + k * y, ep)
            return (s * A * y).sum() - (s * A).sum() * (v0 + v)
        lo, hi = -0.01, 0.05
        try:
            e0 = brentq(g, lo, hi)
        except ValueError:
            break
        e = e0 + k * y
        st = s0 + E * (e - ep)
        ep = ep + np.where(st > fy, (st - fy) / E, 0) + np.where(st < -fy, (st + fy) / E, 0)
        P = (sig(e, ep) * A).sum()
        if P < 0.5 * Pmax:
            break
        Pmax = max(Pmax, P)
    return Pmax / (Atot * fy)


def ec3(lam_bar, alpha):
    phi = 0.5 * (1 + alpha * (lam_bar - 0.2) + lam_bar**2)
    return np.minimum(1.0, 1 / (phi + np.sqrt(phi**2 - lam_bar**2)))


def crc(lam_bar):
    """CRC parabola sigma/fy = 1 - lam^2/4 up to lam = sqrt 2, Euler beyond (Hibbeler Eq. 13-22, 13-23)."""
    return np.where(lam_bar <= np.sqrt(2), 1 - lam_bar**2 / 4, 1 / np.maximum(lam_bar, 1e-9)**2)


LAMS = np.array([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.5, 2.0])

if __name__ == "__main__":
    print(f"lambda_1 = pi sqrt(E/fy) = {np.pi*np.sqrt(E/fy):.1f}")
    print("European curves at lambda = 1:", {k: round(float(ec3(1.0, a)), 3)
          for k, a in (("a0", .13), ("a", .21), ("b", .34), ("c", .49), ("d", .76))})
    print("lam   strong  weak  weak-no-res | EC3 b   EC3 c   CRC   Euler")
    for lb in LAMS:
        s, w, w0 = max_load(lb, "strong"), max_load(lb, "weak"), max_load(lb, "weak", residual=False)
        print(f"{lb:4.1f}  {s:6.3f} {w:6.3f}  {w0:6.3f}      | {float(ec3(lb,.34)):6.3f} {float(ec3(lb,.49)):6.3f}"
              f" {float(crc(lb)):6.3f} {min(1, 1/lb**2):6.3f}")
    # The stub column: residual stresses lower the load at which the section starts to yield.
    A, y, s0 = fibres("weak")
    print(f"stub column: first yield at P/(A fy) = {1 - s0.max()/fy:.3f}; full yield at 1.000 (elastic core shrinks)")
