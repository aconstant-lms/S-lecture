# ex_truss.py -- Chapter 3: the two-bar truss of Chapter 2 as a finite element model.
# Printed in the book from line 4 on. Run: python3 ex_truss.py  (NumPy, SciPy; uses truss_fe.py)
# Linear buckling, arc-length through both limit points, detection, branch switching, imperfections.
import numpy as np
from truss_fe import von_mises, linear_buckling, follow, locate, switch, newton, negative_pivots

def lba_report(phi):
    m = von_mises(phi)
    eta, Phi = linear_buckling(m)
    s, c = np.sin(np.radians(phi)), np.cos(np.radians(phi))
    # consistent linearisation: K0 + eta dK/deta, with dK/deta along the linear prebuckling path
    u1 = np.linalg.solve(m.K0(), m.p); h = 1e-6
    dK = (m.tangent(h * u1) - m.tangent(-h * u1)) / (2 * h)
    mu = np.linalg.eigvals(np.linalg.solve(m.K0(), -dK)).real
    cons = np.sort(1 / mu[mu > 0])
    print(f"phi = {phi}: linear buckling {eta.round(4)} (modes {np.abs(Phi.T).round(2).tolist()}),"
          f" consistent {cons.round(4)}, exact limit {2 * s**3 / (3 * np.sqrt(3)):.4f}"
          + (f", exact bifurcation {2 * c**2 * np.sqrt(3 * s**2 - 2):.4f}" if s**2 > 2 / 3 else ""))

def run_path(phi, ds, nsteps, method="crisfield", e=0.0):
    m = von_mises(phi, e)
    return m, follow(m, np.zeros(2), 0.0, ds, nsteps, method=method)

if __name__ == "__main__":
    # 1. linear buckling against the exact critical loads
    for phi in (30, 65): lba_report(phi)

    # 2. load control stops at the limit point; arc-length goes through (phi = 30 deg)
    m = von_mises(30); u, ok, eta = np.zeros(2), True, 0.0
    while ok: eta += 0.002; u, ok = newton(m, u, eta)
    print(f"load control: Newton fails first at eta = {eta:.3f} (limit 0.0481)")
    for method in ("crisfield", "riks"):
        m, path = run_path(30, 0.02, 80, method)
        v = np.array([-p[0][1] for p in path]); et = np.array([p[1] for p in path])
        npv = [p[2] for p in path]
        err = np.max(np.abs(et - v * (v - 0.5) * (v - 1.0)))        # exact path, s = 0.5, EA = 1
        changes = [k for k in range(1, len(path)) if npv[k] != npv[k - 1]]
        print(f"{method}: {len(path)} points up to v = {v[-1]:.3f}, max |eta - exact| = {err:.1e},"
              f" negative pivots {npv[0]} -> {max(npv)} -> {npv[-1]}")
        if method == "crisfield":
            for k in changes:
                uc, ec, mode, kind = locate(m, path[k - 1], path[k])
                print(f"   critical point: eta = {ec:.6f}, v = {-uc[1]:.5f}, mode {np.abs(mode).round(3)}, {kind}")

    # 3. phi = 65 deg: detection, classification, branch switching
    m, path = run_path(65, 0.01, 40)
    k = next(k for k in range(1, len(path)) if path[k][2] != path[k - 1][2])
    uc, ec, mode, kind = locate(m, path[k - 1], path[k])
    s, c = np.sin(np.radians(65)), np.cos(np.radians(65)); R = np.sqrt(3 * s**2 - 2)
    print(f"phi = 65: first change of inertia at eta = {ec:.5f} (exact {2 * c**2 * R:.5f}),"
          f" v = {-uc[1]:.5f} (exact {s - R:.5f}), mode {np.abs(mode).round(3)}, {kind}")
    ub, eb = switch(m, uc, ec, mode, 0.05)
    branch = follow(m, ub, eb, 0.02, 30, du0=ub - uc, deta0=eb - ec)
    dev = max(abs(p[0][0]**2 + (-p[0][1] - s)**2 - R**2) + abs(p[1] - 2 * c**2 * (s + p[0][1]))
              for p in branch)
    print(f"   switched branch: {len(branch)} points, max deviation from the exact circle {dev:.1e},"
          f" negative pivots on it {sorted(set(p[2] for p in branch))}")

    # 4. imperfection: a sideways load e*eta (Chapter 2 gives 0.2428, 0.2407, 0.2315)
    for e in (1e-4, 1e-3, 1e-2):
        m, path = run_path(65, 0.005, 120, e=e)
        print(f"   sideways load e = {e:.0e}: maximum load {max(p[1] for p in path):.4f}")
