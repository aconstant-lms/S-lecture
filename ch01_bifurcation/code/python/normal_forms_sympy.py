# Chapter 1 -- reduction to normal forms with SymPy (same steps as normal_forms.wl).
# Printed in the book from line 4 on (\lstinputlisting[firstline=4]).
# Run: python3 normal_forms_sympy.py
import sympy as sp

y, r, h, x, v, mu = sp.symbols("y r h x v mu", real=True)

def classify(f, y0, r0):
    """Type of the bifurcation of y' = f(y, r) at (y0, r0), from its Taylor coefficients."""
    d = lambda *s: sp.simplify((sp.diff(f, *s) if s else f).subs({y: y0, r: r0}))
    f0, fy, fr, fyy, fyr, fyyy = d(), d(y), d(r), d(y, y), d(y, r), d(y, y, y)
    assert f0 == 0 and fy == 0, "not a bifurcation point"
    if fr != 0 and fyy != 0:
        return f"fold: Y' = R + Y^2 with R = {sp.simplify(fr*fyy/2)}*(r - r0), Y = {sp.simplify(fyy/2)}*(y - y0)"
    if fr == 0 and fyy != 0 and fyr != 0:
        return f"transcritical: Y' = R Y - Y^2 with R = {fyr}*(r - r0), Y = {sp.simplify(-fyy/2)}*(y - y0)"
    if fr == 0 and fyy == 0 and fyr != 0 and fyyy != 0:
        kind = "supercritical" if fyyy < 0 else "subcritical"
        return f"{kind} pitchfork: R = {fyr}*(r - r0), f_yyy = {fyyy}"
    return "degenerate: look at higher derivatives"

print(classify(r - y - sp.exp(-y), 0, 1))                   # the saddle-node in disguise
print(classify(y * (1 - y) - r * y, 0, 1))                   # logistic with a proportional catch
k, L, c, P = sp.symbols("k L c P", positive=True)
bar = (-k * y + r * L * sp.sin(y)) / c                       # rigid bar, r = P
print(classify(bar, 0, k / L))

# The cusp: eliminate y between f = 0 and f_y = 0.
f = h + r * y - y**3
print("cusp:", sp.factor(sp.resultant(f, sp.diff(f, y), y)), "= 0")

def lyapunov1(fx, gy, w):
    """First Lyapunov coefficient (Guckenheimer & Holmes 3.4.11) of
    x' = -w y + f(x, y), y' = w x + g(x, y) at the Hopf point."""
    X, Y = sp.symbols("X Y")
    F, G = fx(X, Y), gy(X, Y)
    D = lambda e, *s: sp.diff(e, *s).subs({X: 0, Y: 0})
    a = (D(F, X, X, X) + D(F, X, Y, Y) + D(G, X, X, Y) + D(G, Y, Y, Y)) / 16 \
        + (D(F, X, Y) * (D(F, X, X) + D(F, Y, Y)) - D(G, X, Y) * (D(G, X, X) + D(G, Y, Y))
           - D(F, X, X) * D(G, X, X) + D(F, Y, Y) * D(G, Y, Y)) / (16 * w)
    return sp.simplify(a)

# Van der Pol x'' - (mu - x^2) x' + x = 0 at mu = 0, with y = -x': x' = -y, y' = x - x^2 y.
print("van der Pol: l1 =", lyapunov1(lambda X, Y: 0, lambda X, Y: -X**2 * Y, 1))
# Galloping x'' + w^2 x = gamma x' - beta x'^3 at gamma = 0, with y = -x'/w.
w, beta = sp.symbols("omega beta", positive=True)
print("galloping:  l1 =", lyapunov1(lambda X, Y: 0, lambda X, Y: -beta * w**2 * Y**3, w))
