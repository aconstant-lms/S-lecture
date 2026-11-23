# shanley.py -- Chapter 5: Shanley's column, closed form against a step-by-step solution.
# Run: python3 shanley.py     (NumPy, SciPy). All numbers of Section 5.4 and its exercises.
# Model (Hutchinson 1974, Section II.A, with K = 0): a rigid bar of length L on two springs at +-d.
import numpy as np
from scipy.optimize import brentq

E, Et, d, L = 1.0, 1.0 / 3.0, 1.0, 0.8 / 3.0   # spring moduli (force/length), half-spacing, bar length
ey = 1.0                                       # yield contraction of a spring: F_y = E ey = 1
Pt = 2 * Et * d**2 / L                          # tangent-modulus load
Er = 2 * E * Et / (E + Et)                      # reduced modulus of the two-spring cell
Pr = 2 * Er * d**2 / L                          # reduced-modulus load
PE = 2 * E * d**2 / L                           # elastic (Euler) load
c = (E - Et) / (E + Et)


def closed(x, Pb=Pt):
    """Load on the branch that leaves the straight column at Pb, x = L theta / d (spring 2 unloads)."""
    return Pb + (Pr - Pb) * x / (c + x)


def mono(e):
    """Monotonic spring law: elastic, then linear hardening with E_t."""
    return E * e if e <= ey else E * ey + Et * (e - ey)


class Spring:
    def __init__(self, e0=0.0):
        self.emax = e0
    def force(self, e, commit=False):
        if e >= self.emax:
            if commit:
                self.emax = e
            return mono(e)
        return mono(self.emax) - E * (self.emax - e)   # elastic unloading


def path(theta_bar, theta_end, n=4000, P0=None):
    """Follow the column with the rotation theta as the control. P0: start straight at this load."""
    s1, s2 = Spring(), Spring()
    u = 0.0
    if P0 is not None:                                   # perfect column held straight up to P0
        u = brentq(lambda e: 2 * mono(e) - P0, 0.0, 50.0)
        s1.emax = s2.emax = u
    out = []
    for th in np.linspace(0.0, theta_end, n):
        if th == 0.0 and theta_bar == 0.0:              # straight: any u balances the moment; keep P0
            out.append((0.0, 2 * mono(u), mono(u)))
            continue
        g = lambda v: ((s1.force(v + d * th) - s2.force(v - d * th)) * d
                       - (s1.force(v + d * th) + s2.force(v - d * th)) * L * (th + theta_bar))
        u = brentq(g, u - 2.0, u + 20.0)
        F1, F2 = s1.force(u + d * th, True), s2.force(u - d * th, True)
        out.append((th, F1 + F2, F2))
    return np.array(out)


if __name__ == "__main__":
    print(f"P_y = {2*E*ey:.4f}, P_t = {Pt:.4f}, P_r = {Pr:.4f} = {Pr/Pt:.4f} P_t, P_E = {PE:.4f}")
    print(f"P_r/P_t = 2E/(E+E_t) = {2*E/(E+Et):.4f};  c = (E-E_t)/(E+E_t) = {c:.4f}")
    # 1. Perfect column, bifurcation at P_t: closed form against the step-by-step solution.
    res = path(0.0, 0.6, P0=Pt)
    x = L * res[:, 0] / d
    err = np.max(np.abs(res[:, 1] - closed(x)))
    print(f"bifurcation at P_t: max |P_numeric - P_closed| = {err:.2e}")
    for xx in (0.05, 0.2, 0.5, 1.0, 5.0):
        print(f"   x = L theta/d = {xx:4.2f}:  P/P_t = {closed(xx)/Pt:.4f}")
    print(f"   initial slope dP/dx = P_t (spring 2 at neutral loading): {(closed(1e-8)-Pt)/1e-8/Pt:.4f} P_t")
    # 2. Bifurcation above P_t: still possible, under increasing load, up to P_r.
    Pb = 0.5 * (Pt + Pr)
    res = path(0.0, 0.6, P0=Pb)
    print(f"bifurcation at P_b = {Pb/Pt:.3f} P_t: max error {np.max(np.abs(res[:,1]-closed(L*res[:,0]/d, Pb))):.2e}")
    # 3. Imperfect columns: no bifurcation, the path bends near P_t and creeps towards P_r.
    for tb in (1e-3, 1e-2, 5e-2):
        res = path(tb, 0.6)
        x = L * res[:, 0] / d
        i = np.searchsorted(x, 0.05)
        print(f"theta_bar = {tb:6.4f}: P/P_t at x = 0.05: {res[i,1]/Pt:.4f};  at x = 0.16: {res[-1,1]/Pt:.4f}")
    # 4. Hibbeler, Example 13.5 (book p. 690): rod 30 mm, 600 mm, pinned, bilinear sigma-epsilon.
    r, KL = 7.5, 600.0                            # mm
    sE = np.pi**2 * 150e3 / (KL / r)**2           # elastic guess with E = 150 GPa, in MPa
    st = np.pi**2 * 120e3 / (KL / r)**2           # E_t = (270 - 150)/0.001 = 120 GPa
    print(f"Hibbeler 13.5: KL/r = {KL/r:.0f}, Euler {sE:.1f} MPa > 150, tangent {st:.1f} MPa, "
          f"P = {st*np.pi*15**2/1e3:.0f} kN")
    Er_rect = 4 * 150 * 120 / (np.sqrt(150) + np.sqrt(120))**2
    print(f"   reduced modulus (rectangular section) {Er_rect:.1f} GPa -> {np.pi**2*Er_rect*1e3/(KL/r)**2:.0f} MPa")
