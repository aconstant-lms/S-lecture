"""Figures of Chapter 1 (ODEs and bifurcation).

Run from this directory:  python3 fig_ch1.py
Writes the PDFs into figures/ch1/ (st_*.pdf). Stable branches are drawn
solid in the blue of the book (colour cu), unstable branches dashed gray,
bifurcation points and jumps in orange.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "figures")
os.makedirs(OUT, exist_ok=True)

CU = (31 / 255, 90 / 255, 200 / 255)      # \definecolor{cu} in preamble/style.tex
GRAY = (0.55, 0.55, 0.55)
ORANGE = (0.80, 0.40, 0.10)
W = 4.6                                    # figure width in inches (text width is 6.4 in)

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"],
    "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True,
    "font.size": 9, "axes.labelsize": 9, "legend.fontsize": 8,
    "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.unicode_minus": False, "lines.linewidth": 1.6,
})


def stable(ax, x, y, **kw):
    ax.plot(x, y, color=CU, lw=1.8, solid_capstyle="round", zorder=3, **kw)


def unstable(ax, x, y, **kw):
    ax.plot(x, y, color=GRAY, lw=1.5, ls=(0, (4, 3)), zorder=3, **kw)


def split_plot(ax, x, y, is_stable):
    """Plot a branch, solid where is_stable is True and dashed elsewhere."""
    idx = np.flatnonzero(np.diff(is_stable.astype(int))) + 1
    for seg in np.split(np.arange(len(x)), idx):
        if len(seg) < 2:
            continue
        seg = np.append(seg, min(seg[-1] + 1, len(x) - 1))   # close the gap
        (stable if is_stable[seg[0]] else unstable)(ax, x[seg], y[seg])


def middle_axes(ax):
    """Axes through the origin, arrows at the ends, no frame."""
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_position("zero")
        ax.spines[s].set_linewidth(0.7)
    ax.plot(1, 0, ">k", ms=3.5, transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", ms=3.5, transform=ax.get_xaxis_transform(), clip_on=False)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------- 1. y' = ay
fig, ax = plt.subplots(figsize=(W, 2.2))
t = np.linspace(0, 3, 200)
ax.plot(t, np.exp(-t), color=CU)
ax.plot(t, np.ones_like(t), color="k", lw=1.0)
ax.plot(t, np.exp(0.5 * t), color=ORANGE)
ax.text(2.25, 0.25, r"$a=-1$: decay", color=CU)
ax.text(2.25, 1.12, r"$a=0$")
ax.text(1.55, 2.55, r"$a=\frac{1}{2}$: growth", color=ORANGE)
ax.set_xlim(0, 3.2); ax.set_ylim(0, 4.8)
ax.set_xticks([0, 1, 2, 3]); ax.set_yticks([0, 1, 2, 3, 4])
ax.set_xlabel(r"$t$"); ax.set_ylabel(r"$y(t)$")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
save(fig, "st_exponentials.pdf")

# ------------------------------------------------- 2. phase line y' = y(1-y)
fig, ax = plt.subplots(figsize=(W, 2.1))
y = np.linspace(-0.4, 1.4, 200)
ax.plot(y, y * (1 - y), color="k", lw=1.2)
middle_axes(ax)
arrow = dict(arrowstyle="-|>", color=CU, lw=1.8, mutation_scale=11)
ax.annotate("", xy=(0.80, 0), xytext=(0.15, 0), arrowprops=arrow)
ax.annotate("", xy=(1.13, 0), xytext=(1.42, 0), arrowprops=arrow)
ax.annotate("", xy=(-0.38, 0), xytext=(-0.08, 0), arrowprops=arrow)
ax.plot(1, 0, "o", color=CU, ms=6, zorder=5)
ax.plot(0, 0, "o", mfc="white", mec=GRAY, mew=1.5, ms=6, zorder=5)
ax.text(1.02, 0.04, r"stable, $y^*=1$")
ax.text(-0.02, 0.04, r"unstable, $y^*=0$", ha="right")
ax.text(0.5, 0.29, r"$f>0$: $y$ increases", ha="center")
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(-0.45, 1.5); ax.set_ylim(-0.75, 0.38)
ax.text(1.52, -0.06, r"$y$")
ax.text(0.03, 0.36, r"$f(y)$")
save(fig, "st_phaseline.pdf")

# --------------------------------------------- 3. pitchfork y' = ry - y^3
fig, ax = plt.subplots(figsize=(W, 2.7))
s = np.linspace(-1, 1, 401)
stable(ax, [-1, 0], [0, 0])
unstable(ax, [0, 1], [0, 0])
stable(ax, s**2, s)
middle_axes(ax)
ax.plot(0, 0, "o", color=ORANGE, ms=5, zorder=5)
ax.text(-0.55, 0.06, "stable, unique", ha="center")
ax.text(0.62, 0.06, "unstable", ha="center", color=GRAY)
ax.text(1.03, 0.98, r"$+\sqrt{r}$"); ax.text(1.03, -1.02, r"$-\sqrt{r}$")
ax.annotate("bifurcation point", xy=(-0.01, -0.02), xytext=(-0.85, -0.55),
            color=ORANGE, arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7))
ax.set_xlim(-1.1, 1.2); ax.set_ylim(-1.2, 1.2)
ax.set_xticks([-1, -0.5, 0.5, 1]); ax.set_xticklabels([r"$-1$", r"$-0.5$", r"$0.5$", r"$1$"])
ax.set_yticks([-1, 1]); ax.set_yticklabels([r"$-1$", r"$1$"])
ax.text(1.18, 0.06, r"$r$", ha="right"); ax.text(0.04, 1.12, r"$y^*$")
save(fig, "st_pitchfork.pdf")

# ------------------------------ 4. saddle-node and transcritical normal forms
fig, axs = plt.subplots(1, 2, figsize=(1.25 * W, 2.3))
ax = axs[0]
s = np.linspace(0, 1, 200)
stable(ax, -s**2, -s); unstable(ax, -s**2, s)
middle_axes(ax)
ax.plot(0, 0, "o", color=ORANGE, ms=4.5, zorder=5)
ax.text(0.12, 0.45, "no steady state", fontsize=8)
ax.set_title(r"saddle-node: $\dot y=r+y^2$", fontsize=9, pad=10)
ax = axs[1]
stable(ax, [-1, 0], [0, 0]); unstable(ax, [0, 1], [0, 0])
unstable(ax, [-1, 0], [-1, 0]); stable(ax, [0, 1], [0, 1])
middle_axes(ax)
ax.plot(0, 0, "o", color=ORANGE, ms=4.5, zorder=5)
ax.set_title(r"transcritical: $\dot y=ry-y^2$", fontsize=9, pad=10)
for ax in axs:
    ax.set_xlim(-1.1, 1.15); ax.set_ylim(-1.1, 1.1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.text(1.15, -0.15, r"$r$", ha="right"); ax.text(0.05, 1.0, r"$y^*$")
fig.subplots_adjust(wspace=0.25)
save(fig, "st_normalforms.pdf")

# ------------------------------- 5. von Mises truss P/(EA sin^3 phi) = w(w-1)(w-2)
fig, ax = plt.subplots(figsize=(3.4, 2.5))
w = np.linspace(-0.25, 2.35, 600)
g = w * (w - 1) * (w - 2)
gp = 3 * w**2 - 6 * w + 2
split_plot(ax, w, g, gp > 0)
w1, w2 = 1 - 1 / np.sqrt(3), 1 + 2 / np.sqrt(3)
pm = 2 / (3 * np.sqrt(3))
ax.plot(w1, pm, "o", color=ORANGE, ms=4.5, zorder=5)
ax.annotate("", xy=(w2, pm), xytext=(w1 + 0.04, pm),
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2))
ax.text((w1 + w2) / 2, pm + 0.04, "snap-through", color=ORANGE, ha="center", fontsize=8)
ax.axhline(0, color="k", lw=0.6)
ax.set_xlabel(r"$w = v/(L\sin\varphi)$")
ax.set_ylabel(r"$P/(EA\sin^3\varphi)$")
ax.set_xticks([0, w1, 1, 2]); ax.set_xticklabels(["0", r"$1-\frac{1}{\sqrt{3}}$", "1", "2"])
ax.set_yticks([-pm, 0, pm]); ax.set_yticklabels([r"$-\frac{2}{3\sqrt{3}}$", "0", r"$\frac{2}{3\sqrt{3}}$"])
for sp_ in ("top", "right"):
    ax.spines[sp_].set_visible(False)
ax.set_ylim(-0.55, 0.62)
save(fig, "st_vonmises.pdf")

# ------------------------------------------- 6. potential V = -r y^2/2 + y^4/4
fig, axs = plt.subplots(1, 3, figsize=(1.3 * W, 1.75))
for ax, r in zip(axs, (-1.0, 0.0, 1.0)):
    yy = np.linspace(-1.75, 1.75, 300)
    V = -0.5 * r * yy**2 + 0.25 * yy**4
    m = V < 1.15
    ax.plot(yy[m], V[m], color="k", lw=1.2)
    middle_axes(ax)
    if r <= 0:
        ax.plot(0, 0.07, "o", color=CU, ms=5.5, zorder=5)
    else:
        ax.plot(0, 0.07, "o", mfc="white", mec=GRAY, mew=1.4, ms=5.5, zorder=5)
        ax.plot([-1, 1], [-0.18, -0.18], "o", color=CU, ms=5.5, zorder=5)
    ax.set_xlim(-1.8, 1.8); ax.set_ylim(-0.4, 1.2)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(rf"$r={r:g}$", fontsize=9, pad=8)
    ax.text(1.75, -0.17, r"$y$", ha="right"); ax.text(0.14, 1.05, r"$V$")
fig.subplots_adjust(wspace=0.2)
save(fig, "st_potential.pdf")

# ------------------------- 7. rigid bar: equilibrium paths, perfect and imperfect
fig, ax = plt.subplots(figsize=(W, 2.8))
PMAX, TMAX = 1.62, 1.6
th = np.linspace(-TMAX, TMAX, 3201)
th = th[np.abs(th) > 1e-4]
p_perfect = th / np.sin(th)                       # buckled branch: P/Pc = theta/sin(theta)
for side in (th > 0, th < 0):
    m = side & (p_perfect < PMAX)
    stable(ax, th[m], p_perfect[m])
stable(ax, [0, 0], [0, 1]); unstable(ax, [0, 0], [1, PMAX])
labels = []
for th0 in (0.1, 0.3):
    for branch in (th[th > th0], th[th < 0]):
        p = (branch - th0) / np.sin(branch)       # imperfect: P/Pc = (theta - theta0)/sin(theta)
        keep = (p >= 0) & (p < PMAX)
        split_plot(ax, branch[keep], p[keep], p[keep] * np.cos(branch[keep]) < 1.0)
    labels.append((th0, (TMAX - th0) / np.sin(TMAX)))
middle_axes(ax)
ax.text(TMAX + 0.04, TMAX / np.sin(TMAX), r"$\theta_0=0$", va="center", fontsize=8)
for th0, pe in labels:
    ax.text(TMAX + 0.04, pe, rf"$\theta_0={th0:g}$", va="center", fontsize=8)
ax.plot(0, 1, "o", color=ORANGE, ms=5, zorder=5)
ax.annotate(r"$P=P_c$", xy=(0.0, 1.0), xytext=(-0.85, 0.55), color=ORANGE,
            arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.7))
ax.set_xlim(-TMAX, 2.15); ax.set_ylim(0, 1.75)
ax.set_xticks([-1, 1]); ax.set_xticklabels([r"$-1$", r"$1$"]); ax.set_yticks([])
ax.text(2.15, 0.06, r"$\theta$", ha="right")
ax.text(0.05, 1.68, r"$P/P_c$")
save(fig, "st_bar_paths.pdf")

# --------------------------------------------- 8. hysteresis, y' = h + y - y^3
fig, ax = plt.subplots(figsize=(W, 2.7))
yy = np.linspace(-1.33, 1.33, 400)
hh = yy**3 - yy
a = 1 / np.sqrt(3)
split_plot(ax, hh, yy, np.abs(yy) >= a)
middle_axes(ax)
hc = 2 / (3 * np.sqrt(3))
jump = dict(arrowstyle="-|>", color=ORANGE, lw=1.5, mutation_scale=11)
ax.annotate("", xy=(hc, 2 * a - 0.03), xytext=(hc, -a), arrowprops=jump)
ax.annotate("", xy=(-hc, -2 * a + 0.03), xytext=(-hc, a), arrowprops=jump)
ax.text(hc + 0.04, 0.5, "jump up", color=ORANGE)
ax.text(-hc - 0.04, -0.55, "jump down", color=ORANGE, ha="right")
ax.text(hc + 0.06, -0.78, r"$h=h_c$")
ax.text(-hc - 0.06, 0.72, r"$h=-h_c$", ha="right")
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.45, 1.45)
ax.text(1.17, 0.07, r"$h$", ha="right"); ax.text(0.05, 1.35, r"$y^*$")
save(fig, "st_hysteresis.pdf")

# ------------------- 9. Lyapunov: damped oscillator crosses the energy levels inward
from scipy.integrate import solve_ivp
fig, ax = plt.subplots(figsize=(0.62 * W, 2.5))
xx, vv = np.meshgrid(np.linspace(-1.6, 1.6, 300), np.linspace(-1.6, 1.6, 300))
ax.contour(xx, vv, 0.5 * vv**2 + 0.5 * xx**2, levels=[0.08, 0.3, 0.6, 1.0],
           colors=[GRAY], linewidths=0.8)
sol = solve_ivp(lambda t, z: [z[1], -z[0] - 0.3 * z[1]], [0, 30], [1.4, 0.0],
                max_step=0.02)
ax.plot(sol.y[0], sol.y[1], color=CU, lw=1.5)
ax.annotate("", xy=(sol.y[0, 60], sol.y[1, 60]), xytext=(sol.y[0, 55], sol.y[1, 55]),
            arrowprops=dict(arrowstyle="-|>", color=CU, lw=1.5, mutation_scale=11))
ax.plot(0, 0, "o", color=CU, ms=5, zorder=5)
middle_axes(ax)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.6, 1.6); ax.set_aspect("equal")
ax.text(1.68, 0.08, r"$x$", ha="right"); ax.text(0.08, 1.48, r"$\dot x$")
ax.text(0.75, 1.2, r"$E=$ const", color=GRAY, fontsize=8)
save(fig, "st_lyapunov.pdf")

# ------------------------------------------ 10. trace-determinant plane of a 2x2 J
fig, ax = plt.subplots(figsize=(W, 2.6))
T = np.linspace(-2.2, 2.2, 200)
ax.fill_between([-2.2, 0], 0, 1.6, color=CU, alpha=0.10, lw=0)
ax.plot(T, T**2 / 4, color="k", lw=0.8, ls=(0, (2, 2)))
ax.plot([-2.2, 2.2], [0, 0], color=ORANGE, lw=2.0)
ax.plot([0, 0], [0, 1.6], color=ORANGE, lw=2.0)
middle_axes(ax)
arr = dict(arrowstyle="-|>", color="k", lw=1.2, mutation_scale=10)
ax.annotate("", xy=(-1.5, -0.25), xytext=(-1.5, 0.45), arrowprops=arr)
ax.annotate("", xy=(0.35, 0.9), xytext=(-0.55, 0.9), arrowprops=arr)
ax.text(-1.42, 0.12, "buckling\n(divergence)", fontsize=8)
ax.text(0.42, 0.98, "galloping, flutter\n(Hopf)", fontsize=8)
ax.text(-2.1, 1.4, "stable", color=CU)
ax.text(-0.75, 0.55, "spirals", fontsize=7.5, color=GRAY)
ax.text(-2.15, 0.62, "nodes", fontsize=7.5, color=GRAY)
ax.text(1.0, 0.14, r"$\det\mathbf{J}=0$: real $\lambda$ through $0$", color=ORANGE, fontsize=8)
ax.text(0.06, 1.48, r"$\mathrm{tr}\,\mathbf{J}=0$: $\lambda=\pm i\omega$", color=ORANGE, fontsize=8)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(-2.2, 2.3); ax.set_ylim(-0.45, 1.65)
ax.text(2.3, -0.13, r"$\mathrm{tr}\,\mathbf{J}$", ha="right")
ax.text(-0.08, 1.55, r"$\det\mathbf{J}$", ha="right")
save(fig, "st_tracedet.pdf")

# --------------------------- 11. Hopf: z' = (r + i) z - |z|^2 z, phase planes and diagram
fig, axs = plt.subplots(1, 3, figsize=(1.35 * W, 1.9),
                        gridspec_kw=dict(width_ratios=[1, 1, 1.35]))
def hopf(t, z, r):
    x, y = z; q = x * x + y * y
    return [r * x - y - q * x, x + r * y - q * y]
for ax, r in zip(axs[:2], (-0.15, 0.25)):
    s = solve_ivp(hopf, [0, 60], [0.9, 0.0], args=(r,), max_step=0.02)
    ax.plot(s.y[0], s.y[1], color=CU, lw=1.0)
    if r > 0:
        s2 = solve_ivp(hopf, [0, 60], [0.05, 0.0], args=(r,), max_step=0.02)
        ax.plot(s2.y[0], s2.y[1], color=CU, lw=1.0, alpha=0.55)
        c = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.sqrt(r) * np.cos(c), np.sqrt(r) * np.sin(c), color=ORANGE, lw=1.8)
        ax.plot(0, 0, "o", mfc="white", mec=GRAY, mew=1.3, ms=4.5, zorder=5)
    else:
        ax.plot(0, 0, "o", color=CU, ms=4.5, zorder=5)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp_ in ax.spines.values():
        sp_.set_linewidth(0.5); sp_.set_color(GRAY)
    ax.set_title(rf"$r={r:g}$", fontsize=9, pad=4)
ax = axs[2]
stable(ax, [-1, 0], [0, 0]); unstable(ax, [0, 1], [0, 0])
rr = np.linspace(0, 1, 100)
ax.plot(rr, np.sqrt(rr), color=ORANGE, lw=1.8)
middle_axes(ax)
ax.plot(0, 0, "o", color=ORANGE, ms=4.5, zorder=5)
ax.text(0.55, 0.88, r"cycle $\rho=\sqrt{r}$", color=ORANGE, fontsize=8, ha="center")
ax.set_xlim(-1.05, 1.15); ax.set_ylim(-0.15, 1.15)
ax.set_xticks([]); ax.set_yticks([])
ax.text(1.15, 0.05, r"$r$", ha="right"); ax.text(0.05, 1.05, r"$\rho$")
fig.subplots_adjust(wspace=0.25)
save(fig, "st_hopf.pdf")

# -------- 12. continuation of the S-curve: natural parameter vs pseudo-arclength
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "python"))
from arclength import continuation
F = lambda x: np.array([x[1] + x[0] - x[0]**3])
X, Tg, M = continuation(F, [-1.3, -1.3**3 + 1.3], [0, 1], 0.12, 34)
nat, bad, y = [], [], -1.3
for h in np.arange(-0.9, 0.9, 0.08):           # natural parameter: march in h
    for _ in range(30):
        y -= (h + y - y**3) / (1 - 3 * y**2)     # Newton on f(y; h) = 0
    (nat if abs(h + y - y**3) < 1e-8 else bad).append((h, y))
nat, bad = np.array(nat), np.array(bad)
fig, axs = plt.subplots(1, 2, figsize=(1.35 * W, 2.4))
ax = axs[0]
yy = np.linspace(-1.33, 1.33, 400)
ax.plot(yy**3 - yy, yy, color=(0.8, 0.8, 0.8), lw=1.0, zorder=1)
ax.plot(X[:, 1], X[:, 0], "o", color=CU, ms=3.2, zorder=3, label="pseudo-arclength")
ax.plot(nat[:, 0], nat[:, 1], "x", color=ORANGE, ms=4.5, mew=1.2, zorder=4, label=r"natural, steps in $h$")
ax.plot(bad[:, 0], bad[:, 1], "s", mfc="white", mec=ORANGE, ms=4, mew=1.1, zorder=4,
        label="Newton fails")
middle_axes(ax)
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(-1.0, 1.0); ax.set_ylim(-1.45, 1.45)
ax.text(1.0, 0.07, r"$h$", ha="right"); ax.text(0.05, 1.33, r"$y$")
ax.legend(loc="upper left", frameon=False, fontsize=7, handletextpad=0.2,
          bbox_to_anchor=(-0.03, 1.02))
ax = axs[1]
s = np.arange(len(X)) * 0.12
ax.plot(s, M[:, 0], color=ORANGE, lw=1.4, label=r"$\det\mathbf{J}=f_y$")
ax.plot(s, M[:, 1], color=CU, lw=1.6, label=r"$\det\widehat{\mathbf{J}}$")
ax.axhline(0, color="k", lw=0.6)
for y0, h0 in [(-1 / np.sqrt(3), 0), (1 / np.sqrt(3), 0)]:
    k = np.argmin(np.abs(X[:, 0] - y0)); ax.axvline(s[k], color=GRAY, lw=0.6, ls=":")
ax.set_xlabel(r"arclength $s$")
for sp_ in ("top", "right"):
    ax.spines[sp_].set_visible(False)
ax.legend(loc="lower right", frameon=False, fontsize=7.5)
ax.text(s[np.argmin(np.abs(X[:, 0] + 0.577))], 0.6, " fold", fontsize=7.5, color=GRAY, ha="right")
ax.text(s[np.argmin(np.abs(X[:, 0] - 0.577))], 0.6, " fold", fontsize=7.5, color=GRAY)
fig.subplots_adjust(wspace=0.3)
save(fig, "st_continuation.pdf")

# ------- 13. implicit function theorem: regular point, fold, branch point (boxes)
from matplotlib.patches import Rectangle
fig, axs = plt.subplots(1, 3, figsize=(1.38 * W, 2.25))
c = np.linspace(0, 2 * np.pi, 400)

def frame(ax, xl, yl):
    middle_axes(ax)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("equal")
    ax.text(xl[1], 0.07, r"$r$", ha="right"); ax.text(0.06, yl[1] - 0.12, r"$y$")

def box(ax, x0, y0, hw, hh):
    ax.add_patch(Rectangle((x0 - hw, y0 - hh), 2 * hw, 2 * hh, fill=True,
                           fc=(*CU, 0.08), ec=CU, lw=0.9, ls=(0, (3, 2)), zorder=1))

# (a) regular point of the circle: y is a function of r inside the box
ax = axs[0]
ax.plot(np.cos(c), np.sin(c), color=(0.75, 0.75, 0.75), lw=1.0)
r0, y0 = 0.6, 0.8
box(ax, r0, y0, 0.28, 0.2)
rr = np.linspace(r0 - 0.28, r0 + 0.28, 50)
ax.plot(rr, np.sqrt(1 - rr**2), color=CU, lw=2.0, zorder=3)
for rv in (0.42, 0.75):
    ax.plot([rv, rv], [y0 - 0.2, y0 + 0.2], color=GRAY, lw=0.7, ls=":")
ax.plot(r0, y0, "o", color=CU, ms=4.5, zorder=4)
ax.text(0.0, -1.52, r"$f_y\neq0$:" "\n" r"$y=y^*(r)$", ha="center", fontsize=8, color=CU,
        bbox=dict(fc="white", ec="none", pad=1))
ax.set_title("regular point", fontsize=9, pad=4)
frame(ax, (-1.2, 1.5), (-1.85, 1.25))

# (b) fold of the circle: no graph over r, but r is a function of y
ax = axs[1]
ax.plot(np.cos(c), np.sin(c), color=(0.75, 0.75, 0.75), lw=1.0)
box(ax, 1.0, 0.0, 0.2, 0.32)
yy = np.linspace(-0.32, 0.32, 50)
ax.plot(np.sqrt(1 - yy**2), yy, color=ORANGE, lw=2.0, zorder=3)
ax.plot([0.9, 0.9], [-0.32, 0.32], color=GRAY, lw=0.7, ls=":")
ax.plot([0.8, 1.2], [0.18, 0.18], color=GRAY, lw=0.7, ls=":")
ax.annotate("", xy=(1.0, 0.55), xytext=(1.0, 0.0),
            arrowprops=dict(arrowstyle="-|>", color="k", lw=1.0, mutation_scale=9))
ax.text(1.04, 0.5, r"$\mathbf{t}$", fontsize=8)
ax.plot(1.0, 0.0, "o", color=ORANGE, ms=4.5, zorder=4)
ax.text(0.0, -1.52, r"$f_y=0,\ f_r\neq0$:" "\n" r"$r=r^*(y)$", ha="center", fontsize=8,
        color=ORANGE, bbox=dict(fc="white", ec="none", pad=1))
ax.set_title("fold", fontsize=9, pad=4)
frame(ax, (-1.2, 1.5), (-1.85, 1.25))

# (c) branch point of the pitchfork r y - y^3 = 0: no graph in any direction
ax = axs[2]
s_ = np.linspace(-1.05, 1.05, 200)
ax.plot([-1.2, 1.2], [0, 0], color=(0.75, 0.75, 0.75), lw=1.0)
ax.plot(s_**2, s_, color=(0.75, 0.75, 0.75), lw=1.0)
box(ax, 0.0, 0.0, 0.3, 0.3)
ax.plot([-0.3, 0.3], [0, 0], color=GRAY, lw=2.0, zorder=3)
s2 = np.linspace(-0.3, 0.3, 60)
ax.plot(s2**2, s2, color=GRAY, lw=2.0, zorder=3)
ax.plot(0, 0, "o", color="k", ms=4.5, zorder=4)
ax.text(0.0, -1.52, r"$f_y=f_r=0$:" "\n" "no graph", ha="center", fontsize=8,
        bbox=dict(fc="white", ec="none", pad=1))
ax.set_title("branch point", fontsize=9, pad=4)
frame(ax, (-1.2, 1.5), (-1.85, 1.25))
fig.subplots_adjust(wspace=0.12)
save(fig, "st_ift.pdf")
