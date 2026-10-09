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

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "figures", "ch1")
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

# ----------------------------------------------- 5. fishery N' = N(1-N) - h
fig, ax = plt.subplots(figsize=(W, 2.5))
N = np.linspace(0, 1.05, 200)
for h, col, ls, lab in [(0.0, (0.7, 0.7, 0.7), "-", r"$h=0$"),
                        (0.15, CU, "-", r"$h=0.15$"),
                        (0.25, ORANGE, "-", r"$h=\frac{1}{4}$ (critical)"),
                        (0.32, (0.35, 0.35, 0.35), (0, (4, 3)), r"$h=0.32$")]:
    ax.plot(N, N * (1 - N) - h, color=col, ls=ls, lw=1.5, label=lab)
middle_axes(ax)
Np, Nm = (1 + np.sqrt(0.4)) / 2, (1 - np.sqrt(0.4)) / 2
ax.plot(Np, 0, "o", color=CU, ms=5, zorder=5)
ax.plot(Nm, 0, "o", mfc="white", mec=CU, mew=1.4, ms=5, zorder=5)
ax.plot(0.5, 0, "o", color=ORANGE, ms=4.5, zorder=5)
ax.text(Np, 0.025, r"$N_+$", color=CU, ha="center")
ax.text(Nm, 0.025, r"$N_-$", color=CU, ha="center")
ax.set_xticks([1]); ax.set_yticks([])
ax.set_xlim(-0.02, 1.12); ax.set_ylim(-0.42, 0.32)
ax.text(1.12, 0.015, r"$N$", ha="right"); ax.text(0.02, 0.30, r"$\dot N$")
ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False)
save(fig, "st_fishery.pdf")

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
