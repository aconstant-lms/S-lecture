# koiter_sympy.py -- Chapter 2: Koiter (LSK) coefficients of a simple critical point, n dof.
# Run: python3 koiter_sympy.py     (SymPy). Same steps as ../mathematica/koiter.wl.
# Convention: eta = eta_c + eta1*xi + eta2*xi^2/2 + ...  (Triantafyllidis, AC-3.13/14).
import sympy as sp


def lsk(E, u, eta, uc, du0, etac, u1):
    """Koiter coefficients of E(u, eta) at the critical point (uc, etac).

    u    : list of symbols (the dof), eta : load symbol
    uc   : critical state on the principal path, du0 : d(u0)/d(eta) there
    u1   : buckling mode (any length; it is normalised here)
    Returns (eta1, eta2); eta2 is None when eta1 != 0.
    """
    n = len(u)
    sub = {**dict(zip(u, uc)), eta: etac}
    u1 = sp.Matrix(u1) / sp.sqrt(sum(c**2 for c in u1))
    d = lambda *ix: sp.diff(E, *[u[i] for i in ix])          # partial derivatives
    K = sp.Matrix(n, n, lambda i, j: d(i, j).subs(sub))
    assert sp.simplify((K * u1).norm()) == 0, "u1 is not a null vector of K_c"
    # rate of loss of stiffness along the principal path: (dK/deta) [u1, u1]
    Kp = sum((sum(d(i, j, k) * du0[k] for k in range(n)) + sp.diff(d(i, j), eta)).subs(sub)
             * u1[i] * u1[j] for i in range(n) for j in range(n))
    E3 = lambda a, b, c: sum(d(i, j, k).subs(sub) * a[i] * b[j] * c[k]
                             for i in range(n) for j in range(n) for k in range(n))
    e3 = sp.simplify(E3(u1, u1, u1))
    if e3 != 0:
        return sp.simplify(-e3 / (2 * Kp)), None
    # second-order field v (v orthogonal to u1):  K_c v = -E_uuu[u1, u1]
    rhs = sp.Matrix([-sum(d(i, j, k).subs(sub) * u1[j] * u1[k]
                          for j in range(n) for k in range(n)) for i in range(n)])
    lam = sp.Symbol('mu')
    vs = sp.Matrix(sp.symbols('v0:%d' % n))
    sol = sp.solve(list(K * vs - rhs - lam * u1) + [(u1.T * vs)[0]], list(vs) + [lam], dict=True)[0]
    v = vs.subs(sol)
    e4 = sum(sp.diff(E, u[i], u[j], u[k], u[l]).subs(sub) * u1[i] * u1[j] * u1[k] * u1[l]
             for i in range(n) for j in range(n) for k in range(n) for l in range(n))
    eta2 = -sp.Rational(1, 3) * (e4 + 3 * E3(v, u1, u1)) / Kp
    return sp.Integer(0), sp.simplify(eta2)


if __name__ == "__main__":
    k, L, Ek, l, m, n, c, c1, c2 = sp.symbols('k L E l m n c c_1 c_2', positive=True)
    eta, th, v, x, y = sp.symbols('eta theta v x y')

    # 1. Rigid T model (Triantafyllidis AB-1): dof (v, theta)
    E = Ek * (v**2 + (l * th)**2) + k / 2 * (L * th)**2 + m / 3 * (L * th)**3 \
        + n / 4 * (L * th)**4 - eta * (v + L * th**2 / 2)
    etac = (2 * Ek * l**2 + k * L**2) / L
    print('T model, m != 0  :', lsk(E, [v, th], eta, [etac / (2 * Ek), 0], [1 / (2 * Ek), 0], etac, [0, 1]))
    print('T model, m = 0   :', lsk(E.subs(m, 0), [v, th], eta, [etac / (2 * Ek), 0], [1 / (2 * Ek), 0], etac, [0, 1]))

    # 2. Rigid bar on a torsional spring (Chapter 1), dead load eta = P
    E = k * th**2 / 2 - eta * L * (1 - sp.cos(th))
    print('bar, torsional   :', lsk(E, [th], eta, [0], [0], k / L, [1]))
    # 3. Bar with a horizontal spring that stays horizontal: P = kL cos(theta)
    E = k * (L * sp.sin(th))**2 / 2 - eta * L * (1 - sp.cos(th))
    print('bar, lateral     :', lsk(E, [th], eta, [0], [0], k * L, [1]))
    # 4. Bar with a spring inclined at 45 degrees, anchored at (-L, 0)
    ln = sp.sqrt((L * sp.sin(th) + L)**2 + (L * sp.cos(th))**2)
    E = k * (ln - sp.sqrt(2) * L)**2 / 2 - eta * L * (1 - sp.cos(th))
    print('bar, inclined    :', lsk(E, [th], eta, [0], [0], k * L / 2, [1]))

    # 5. Two-bar truss (Triantafyllidis AB-5), EA = L = 1, Green strains, steep bars
    phi = sp.Symbol('phi')
    s, co = sp.sin(phi), sp.cos(phi)
    eps = lambda l2: (l2 - 1) / 2
    E = (eps((co + x)**2 + (s - y)**2)**2 + eps((co - x)**2 + (s - y)**2)**2) / 2 - eta * y
    R = sp.sqrt(3 * s**2 - 2)
    yb = s - R                                       # first bifurcation on the principal path
    etab = 2 * co**2 * R
    dlam = sp.diff(y * (y - 2 * s) * (y - s), y).subs(y, yb)
    e1, e2 = lsk(E, [x, y], eta, [0, yb], [0, 1 / dlam], etab, [1, 0])
    print('truss, phi = 65  :', sp.N(e2.subs(phi, 65 * sp.pi / 180), 6),
          ' exact -2cos^2/R =', sp.N((-2 * co**2 / R).subs(phi, 65 * sp.pi / 180), 6))
    E4only = -sp.Rational(1, 3) * 6 / ((sp.diff(x**2 + y**2 - 2*y*s + 2*co**2, y) / dlam).subs(y, yb))
    print('   without the passive coordinate v:', sp.N(E4only.subs(phi, 65 * sp.pi / 180), 6))

    # 6. Augusti column (Thompson & Hunt 1973, Sec. 10.4), truncated energy, eta = P
    E = c1 * x**2 / 2 + c2 * y**2 / 2 + eta * L * (-x**2 / 2 - y**2 / 2 + x**4 / 24 + y**4 / 24
                                                    - x**2 * y**2 / 4)
    print('Augusti, mode 1  :', lsk(E, [x, y], eta, [0, 0], [0, 0], c1 / L, [1, 0]))
    Ed = sp.expand(E.subs({c1: c, c2: c, x: y}))      # 45-degree plane, coincident springs
    print('Augusti, diagonal (amplitude u = u1 = u2):', lsk(Ed, [y], eta, [0], [0], c / L, [1]))
