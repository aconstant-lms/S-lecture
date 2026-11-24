# ft_section.py -- Chapter 5: thin-walled open sections, their constants and the three buckling loads.
# Run: python3 ft_section.py     (NumPy, SciPy). All numbers of Sections 5.1-5.3 and their exercises.
# A section is a tree of straight walls (mid-line, thickness t). Units: mm, N, MPa.
import numpy as np
from scipy.linalg import eigh

GAUSS = np.polynomial.legendre.leggauss(8)


class Section:
    """Thin-walled open section: nodes (y, z) and walls (i, j, t) forming a tree."""

    def __init__(self, nodes, walls):
        self.X = np.asarray(nodes, float)
        self.walls = walls
        self._centroid_and_inertia()
        self._shear_centre_and_warping()

    def _points(self):
        """Gauss points of every wall: coordinates, weights t ds, and the wall index."""
        s, w = GAUSS
        out = []
        for k, (i, j, t) in enumerate(self.walls):
            a, b = self.X[i], self.X[j]
            L = np.linalg.norm(b - a)
            for sk, wk in zip(s, w):
                out.append((*(a + (sk + 1) / 2 * (b - a)), t * wk * L / 2, k, (sk + 1) / 2))
        return np.array(out)

    def _centroid_and_inertia(self):
        P = self._points()
        self.A = P[:, 2].sum()
        self.c = (P[:, :2] * P[:, 2:3]).sum(0) / self.A
        y, z, dA = P[:, 0] - self.c[0], P[:, 1] - self.c[1], P[:, 2]
        D = np.array([[(y * y * dA).sum(), (y * z * dA).sum()],
                      [(y * z * dA).sum(), (z * z * dA).sum()]])
        # n.D.n = int (n.r)^2 dA: the inertia that resists a lateral displacement along n
        I, V = np.linalg.eigh(D)
        self.Imin, self.Imax, self.R = I[0], I[1], V        # V[:,0]: the direction of easiest bending
        self.J = sum(np.linalg.norm(self.X[j] - self.X[i]) * t**3 / 3 for i, j, t in self.walls)

    def _sectorial(self, pole):
        """Sectorial coordinate omega(s) = int (r x ds) about `pole`, from node 0, at the Gauss points."""
        om = {0: 0.0}
        todo = [0]
        adj = {}
        for k, (i, j, t) in enumerate(self.walls):
            adj.setdefault(i, []).append((j, k)); adj.setdefault(j, []).append((i, k))
        orient = {}
        while todo:
            n = todo.pop()
            for m, k in adj.get(n, []):
                if m in om:
                    continue
                a, b = self.X[n] - pole, self.X[m] - pole
                om[m] = om[n] + (a[0] * b[1] - a[1] * b[0])
                orient[k] = (n, m)
                todo.append(m)
        P = self._points()
        w = np.empty(len(P))
        for q, (_, _, _, k, s) in enumerate(P):
            n, m = orient[int(k)]
            i, j, _ = self.walls[int(k)]
            s = s if (i, j) == (n, m) else 1 - s
            w[q] = (1 - s) * om[n] + s * om[m]
        return P, w

    def _shear_centre_and_warping(self):
        # omega about a pole S is linear in S: find S with int(omega y) = int(omega z) = 0 (centroidal y, z)
        P, w0 = self._sectorial(self.c)
        y, z, dA = P[:, 0] - self.c[0], P[:, 1] - self.c[1], P[:, 2]
        _, wy = self._sectorial(self.c + [1.0, 0.0])
        _, wz = self._sectorial(self.c + [0.0, 1.0])
        gy, gz = wy - w0, wz - w0
        M = np.array([[(gy * y * dA).sum(), (gz * y * dA).sum()],
                      [(gy * z * dA).sum(), (gz * z * dA).sum()]])
        rhs = -np.array([(w0 * y * dA).sum(), (w0 * z * dA).sum()])
        d = np.linalg.solve(M, rhs)
        self.s = self.c + d                                 # shear centre
        wS = w0 + d[0] * gy + d[1] * gz
        wS -= (wS * dA).sum() / self.A                      # normalised sectorial coordinate
        self.Gamma = (wS * wS * dA).sum()                   # warping constant
        # shear centre in principal axes, polar radius of gyration about it
        self.s0 = self.R.T @ d                              # shear-centre offset along V[:,0] and V[:,1]
        self.r0sq = (self.Imin + self.Imax) / self.A + d @ d

    def loads(self, L, E=210e3, G=81e3):
        """Pinned column with fork supports: the three buckling loads, smallest first, and the modes.
        Unknowns (v, w, phi): lateral displacements of the shear centre along V[:,0] (minor-axis
        flexure, inertia Imin) and V[:,1] (major-axis flexure, inertia Imax), and the twist. Eq. (5.9)."""
        Pv = np.pi**2 * E * self.Imin / L**2
        Pw = np.pi**2 * E * self.Imax / L**2
        Pphi = (G * self.J + np.pi**2 * E * self.Gamma / L**2) / self.r0sq
        y0, z0 = self.s0
        K = np.diag([Pv, Pw, self.r0sq * Pphi])
        M = np.array([[1, 0, z0], [0, 1, -y0], [z0, -y0, self.r0sq]])
        P, V = eigh(K, M)
        return P, V, dict(P_minaxis=Pv, P_maxaxis=Pw, P_phi=Pphi)


def I_section(h, b, tf, tw):
    return Section([(0, 0), (-b / 2, 0), (b / 2, 0), (0, h), (-b / 2, h), (b / 2, h)],
                   [(0, 1, tf), (0, 2, tf), (0, 3, tw), (3, 4, tf), (3, 5, tf)])


def channel(h, b, t):
    return Section([(0, 0), (b, 0), (0, h), (b, h)], [(0, 1, t), (0, 2, t), (2, 3, t)])


def angle(b, t):
    return Section([(0, 0), (b, 0), (0, b)], [(0, 1, t), (0, 2, t)])


def cruciform(b, t):
    return Section([(0, 0), (b, 0), (-b, 0), (0, b), (0, -b)],
                   [(0, 1, t), (0, 2, t), (0, 3, t), (0, 4, t)])


if __name__ == "__main__":
    E, G, nu = 210e3, 81e3, 0.3
    # 1. Checks against closed forms --------------------------------------------------------
    h, b, tf, tw = 300.0, 300.0, 19.0, 11.0          # HEB 300 by its mid-lines (thin-line model)
    I = I_section(h - tf, b, tf, tw)
    print(f"I-section: Gamma = {I.Gamma:.4e}, closed form t_f b^3 h^2/24 = {tf*b**3*(h-tf)**2/24:.4e} mm^6")
    C = channel(200.0, 75.0, 8.0)
    e = 3 * 75.0**2 / (200.0 + 6 * 75.0)
    print(f"channel: shear centre {-C.s[0]:.3f} mm behind the web, closed form 3b^2/(h+6b) = {e:.3f}")
    GamC = 8.0 * 75.0**3 * 200.0**2 / 12 * (3 * 75.0 + 2 * 200.0) / (6 * 75.0 + 200.0)
    print(f"         Gamma = {C.Gamma:.4e}, closed form = {GamC:.4e}")
    A_ = angle(95.0, 10.0)
    print(f"angle: shear centre at ({A_.s[0]:.2e}, {A_.s[1]:.2e}) = the corner, Gamma = {A_.Gamma:.1e}")
    X = cruciform(95.0, 10.0)
    print(f"cruciform: Gamma = {X.Gamma:.1e}, J = {X.J:.4e} = 4bt^3/3, r0^2 = {X.r0sq:.2f} = b^2/3 = {95**2/3:.2f}")

    # 2. The cruciform: torsional load independent of the length ------------------------------
    b, t = 95.0, 10.0
    print(f"\ncruciform b = {b}, t = {t}: G(t/b)^2 = {G*(t/b)**2:.1f} MPa")
    for L in (500.0, 1000.0, 2000.0, 4000.0):
        P, _, d = X.loads(L, E, G)
        print(f"   L = {L:5.0f} mm: torsional {d['P_phi']/X.A:6.1f} MPa, flexural {d['P_minaxis']/X.A:7.1f} MPa"
              f" -> buckles at {P[0]/X.A:6.1f} MPa")
    Lx = np.pi * b**2 / t * np.sqrt(E / (6 * G))
    print(f"   crossover length pi (b^2/t) sqrt(E/6G) = {Lx:.0f} mm = {Lx/(b**2/t):.3f} b^2/t")
    k = 6 * (1 - nu) / np.pi**2
    print(f"   plate with one free edge: k = 6(1 - nu)/pi^2 = {k:.4f}")
    bX, tX = 120.0, 8.0
    print(f"   cruciform b = {bX:.0f}, t = {tX:.0f}: G(t/b)^2 = {G*(tX/bX)**2:.0f} MPa, at the yield stress of S355")

    # 3. Equal-angle struts: flexural-torsional buckling governs short, thin angles ------------
    for (bb, tt) in ((100.0, 10.0), (100.0, 6.0)):
        An = angle(bb - tt / 2, tt)
        print(f"\nangle {bb:.0f} x {bb:.0f} x {tt:.0f} (mid-line legs {bb-tt/2:.0f} mm), pinned, fork supports:")
        for L in (500.0, 1000.0, 2000.0, 3000.0):
            P, V, d = An.loads(L, E, G)
            ft = P[1] if abs(V[0, 0]) > 0.9 * np.linalg.norm(V[:, 0]) else P[0]
            print(f"   L = {L:4.0f}: minor-axis flexure {d['P_minaxis']/1e3:7.1f} kN, twist alone {d['P_phi']/1e3:6.1f},"
                  f" flexural-torsional {ft/1e3:6.1f}  -> {P[0]/1e3:6.1f} kN, {P[0]/An.A:5.0f} MPa")

    # 4. A channel strut: the coupled load is below all three --------------------------------
    print("\nchannel 200 x 75 x 8 (mid-lines), pinned, fork supports:")
    for L in (1000.0, 2000.0, 4000.0):
        P, V, d = C.loads(L, E, G)
        print(f"   L = {L:4.0f}: P_minaxis {d['P_minaxis']/1e3:7.1f}, P_maxaxis {d['P_maxaxis']/1e3:7.1f},"
              f" P_phi {d['P_phi']/1e3:7.1f};  modes {P[0]/1e3:7.1f}, {P[1]/1e3:7.1f}, {P[2]/1e3:7.1f} kN")
    print(f"   shear-centre offset {np.linalg.norm(C.s - C.c):.1f} mm, r0^2 = {C.r0sq:.0f} mm^2,"
          f" H = {1 - np.sum((C.s - C.c)**2)/C.r0sq:.3f}")

    # 5. Lateral-torsional buckling ----------------------------------------------------------
    # simply supported I-beam under uniform moment: M_cr = (pi/L) sqrt(EI_z GJ) sqrt(1 + pi^2 E Gamma/(G J L^2))
    for L in (4000.0, 8000.0):
        M = np.pi / L * np.sqrt(E * I.Imin * G * I.J) * np.sqrt(1 + np.pi**2 * E * I.Gamma / (G * I.J * L**2))
        print(f"HEB 300 beam, L = {L/1e3:.0f} m, uniform moment: M_cr = {M/1e6:.0f} kN m")
    # a steel ruler held on edge as a cantilever, tip load at the centroid: P_cr = 4.013 sqrt(EI_z GJ)/L^2
    d_, t_, L_ = 30.0, 1.0, 300.0
    for (nm, EE, GG) in (("steel", E, G), ("acrylic", 3.2e3, 1.2e3)):
        EIz, GJ = EE * d_ * t_**3 / 12, GG * d_ * t_**3 / 3
        print(f"{nm} ruler {d_:.0f} x {t_:.0f} mm, {L_:.0f} mm: P_cr = {4.013*np.sqrt(EIz*GJ)/L_**2:.2f} N;"
              f" halve L: x {4:.0f}")

    # 6. Eurocode 3 (EN 1993-1-1, 6.3.2.2, general case): lateral-torsional buckling resistance -------
    #    lambda_LT = sqrt(W_pl f_y / M_cr), chi_LT from the column formula with alpha_LT;
    #    rolled I-sections with h/b <= 2: curve a (alpha_LT = 0.21). HEB 300: W_pl,y = 1869 cm^3 (tables).
    from fibre_column import ec3
    Wpl, fy = 1869e3, 235.0
    for L in (4000.0, 8000.0):
        M = np.pi / L * np.sqrt(E * I.Imin * G * I.J) * np.sqrt(1 + np.pi**2 * E * I.Gamma / (G * I.J * L**2))
        lt = np.sqrt(Wpl * fy / M)
        chi = float(ec3(lt, 0.21))
        print(f"EC3 LTB, HEB 300 S235, L = {L/1e3:.0f} m: M_pl = {Wpl*fy/1e6:.0f} kN m, lambda_LT = {lt:.3f},"
              f" chi_LT = {chi:.3f}, M_b = {chi*Wpl*fy/1e6:.0f} kN m")
