"""Figures of Chapter 2 (discrete systems, Koiter, snap-through, interaction, flutter).

Run from this directory:  python3 fig_ch2.py
Writes the PDFs into ../../figures (ld_*.pdf). Same conventions as fig_ch1.py:
stable branches solid blue, unstable dashed gray, critical points orange.
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "python"))
from ex_imperfection import p_lateral, p_inclined, p_augusti, max_load, law_half, law_23

OUT = os.path.join(HERE, "..", "..", "figures")
os.makedirs(OUT, exist_ok=True)
CU = (31 / 255, 90 / 255, 200 / 255)
GRAY = (0.55, 0.55, 0.55)
ORANGE = (0.80, 0.40, 0.10)
GREEN = (20 / 255, 150 / 255, 60 / 255)
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["cmr10", "DejaVu Serif"],
    "mathtext.fontset": "cm", "axes.formatter.use_mathtext": True,
    "font.size": 9, "axes.labelsize": 9, "legend.fontsize": 8,
    "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.unicode_minus": False, "lines.linewidth": 1.6,
})


def stable(ax, x, y, **kw):
    ax.plot(x, y, color=kw.pop("color", CU), lw=1.8, solid_capstyle="round", zorder=3, **kw)


def unstable(ax, x, y, **kw):
    ax.plot(x, y, color=kw.pop("color", GRAY), lw=1.5, ls=(0, (4, 3)), zorder=3, **kw)


def split_plot(ax, x, y, is_stable, **kw):
    idx = np.flatnonzero(np.diff(is_stable.astype(int))) + 1
    for seg in np.split(np.arange(len(x)), idx):
        if len(seg) < 2:
            continue
        seg = np.append(seg, min(seg[-1] + 1, len(x) - 1))
        (stable if is_stable[seg[0]] else unstable)(ax, x[seg], y[seg], **kw)


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("wrote", name)


# ------------------------------------------------ 1. rigid T model, three cases
# eta_c = L = 1; path eta = (theta + m theta^2 + n theta^3) / (theta + delta)
# stability: E_thth / L = (1 - eta) + 2 m theta + 3 n theta^2 > 0
fig, axs = plt.subplots(1, 3, figsize=(6.3, 2.2), sharey=True)
cases = [(0.6, 0.0, "asymmetric ($m>0$, $n=0$)"),
         (0.0, 1.0, "stable symmetric ($n>0$)"),
         (0.0, -1.0, "unstable symmetric ($n<0$)")]
th = np.linspace(-0.62, 0.62, 2001)
for ax, (m, n, title) in zip(axs, cases):
    ax.axhline(1, color=(0.8, 0.8, 0.8), lw=0.6)
    stable(ax, [0, 0], [0, 1]); unstable(ax, [0, 0], [1, 1.5])
    eta = 1 + m * th + n * th**2
    split_plot(ax, th, eta, (1 - eta) + 2 * m * th + 3 * n * th**2 > 0)
    for d in (0.02, -0.02):
        for side in (th[th * d > 0], th[th * d < 0]):
            side = side[np.abs(side + d) > 1e-3]
            e = (side + m * side**2 + n * side**3) / (side + d)
            st = (1 - e) + 2 * m * side + 3 * n * side**2 > 0
            ok = (e > 0) & (e < 1.5)
            split_plot(ax, side[ok], e[ok], st[ok], color=GREEN if d > 0 else ORANGE)
    ax.plot(0, 1, "o", color="k", ms=3, zorder=5)
    ax.set_title(title, fontsize=8)
    ax.set_xlabel(r"$\theta$"); ax.set_xlim(-0.62, 0.62); ax.set_ylim(0, 1.5)
    ax.set_xticks([0]); clean(ax)
axs[0].set_ylabel(r"$\eta/\eta_c$"); axs[0].set_yticks([0, 1])
fig.subplots_adjust(wspace=0.12)
save(fig, "ld_tmodel.pdf")

# ------------------------------------------------ 2. imperfection-sensitivity curves
fig, ax = plt.subplots(figsize=(4.6, 2.6))
xb = np.logspace(-5, np.log10(0.05), 40)
rows = [(p_inclined, lambda x: law_half(x, -0.75), "asymmetric, $\\eta_1=-\\frac{3}{4}\\eta_c$", CU),
        (p_lateral, lambda x: law_23(x, -1.0), "unstable symmetric, $\\eta_2=-\\eta_c$", ORANGE),
        (p_augusti, lambda x: law_23(x, -2 / 3), "Augusti, coincident modes", GREEN)]
for p, law, lab, col in rows:
    ax.plot(xb, [max_load(p, x) for x in xb], color=col, lw=1.8, label=lab)
    ax.plot(xb, law(xb), color=col, lw=1.0, ls=(0, (2, 2)))
ax.set_xlabel(r"imperfection $\bar\xi$"); ax.set_ylabel(r"$\eta_m/\eta_c$")
ax.set_xlim(0, 0.05); ax.set_ylim(0.5, 1.0); clean(ax)
ax.legend(frameon=False, loc="lower left")
save(fig, "ld_imperfection.pdf")

# ------------------------------------------------ 3. two-bar (von Mises) truss
fig, axs = plt.subplots(1, 2, figsize=(6.3, 2.4))
for ax, deg in zip(axs, (30, 65)):
    phi = np.radians(deg); s, c = np.sin(phi), np.cos(phi)
    v = np.linspace(-0.15 * s, 2.15 * s, 1500)
    lam = v * (v - 2 * s) * (v - s)
    Kuu = v**2 - 2 * v * s + 2 * c**2
    Kvv = 3 * (v**2 - 2 * v * s + 2 * s**2 / 3)
    split_plot(ax, v, lam, (Kuu > 0) & (Kvv > 0))
    if 3 * s**2 > 2:
        R = np.sqrt(3 * s**2 - 2)
        vb = np.linspace(s - R, s + R, 50)
        unstable(ax, vb, 2 * c**2 * (s - vb), color=ORANGE)
        ax.plot([s - R, s + R], [2 * c**2 * R, -2 * c**2 * R], "o", color=ORANGE, ms=3.5, zorder=5)
    lm = 2 / (3 * np.sqrt(3)) * s**3
    ax.plot([s * (1 - 1 / np.sqrt(3))], [lm], "o", color="k", ms=3, zorder=5)
    ax.axhline(0, color="k", lw=0.5)
    ax.set_title(rf"$\varphi = {deg}^\circ$", fontsize=8)
    ax.set_xlabel(r"$v/L$"); clean(ax)
axs[0].set_ylabel(r"$\eta/EA$")
fig.subplots_adjust(wspace=0.28)
save(fig, "ld_truss.pdf")

# ------------------------------------------------ 4. Augusti column
fig, axs = plt.subplots(1, 2, figsize=(6.3, 2.4), sharey=True)
u = np.linspace(0, 1.2, 400)
# (a) c2 = 1.2 c1: primary paths and the falling coupled path from C
c1, c2 = 1.0, 1.2
ax = axs[0]
stable(ax, [0, 0], [0, c1]); unstable(ax, [0, 0], [c1, 1.35])
PC = (3 * c1 + c2) / 4
pb = c1 / (1 - u**2 / 6)                       # path (b): u1 = u, u2 = 0
split_plot(ax, u, pb, pb < PC)
pc = c2 / (1 - u**2 / 6)
unstable(ax, u[pc < 1.35], pc[pc < 1.35])
# coupled path (d): solve the two equations for (u1, u2, P) by sampling u2
u2 = np.linspace(0, 0.9, 200)
sol = []
for b in u2:
    # c1 = P(1 - u1^2/6 + b^2/2), c2 = P(1 - b^2/6 + u1^2/2)  ->  eliminate P
    # c1 (1 - b^2/6 + a/2) = c2 (1 - a/6 + b^2/2), a = u1^2
    a = (c2 * (1 + b**2 / 2) - c1 * (1 - b**2 / 6)) / (c1 / 2 + c2 / 6)
    if a >= 0:
        sol.append((np.sqrt(a), c1 / (1 - a / 6 + b**2 / 2)))
sol = np.array(sol)
unstable(ax, sol[:, 0], sol[:, 1], color=ORANGE)
ax.plot(np.sqrt(6 * (1 - c1 / PC)), PC, "o", color=ORANGE, ms=3.5, zorder=5)
ax.text(np.sqrt(6 * (1 - c1 / PC)) + 0.04, PC + 0.03, "$C$", fontsize=8)
ax.set_title(r"$c_2 = 1.2\,c_1$", fontsize=8)
ax.set_xlabel(r"$u_1$"); ax.set_ylabel(r"$PL/c_1$"); ax.set_ylim(0, 1.35); clean(ax)
# (b) coincident springs: uncoupled stable paths, coupled falling path, imperfect
ax = axs[1]
stable(ax, [0, 0], [0, 1]); unstable(ax, [0, 0], [1, 1.35])
stable(ax, u, 1 / (1 - u**2 / 6))
unstable(ax, u, 1 / (1 + u**2 / 3), color=ORANGE)
for eps in (0.01, 0.03):
    ue = np.linspace(eps * 1.001, 1.2, 600)
    pe = p_augusti(ue, eps)
    imax = np.argmax(pe)
    stable(ax, ue[:imax + 1], pe[:imax + 1], color=GREEN)
    unstable(ax, ue[imax:], pe[imax:], color=GREEN)
ax.set_title(r"$c_1 = c_2$: single plane (blue), $45^\circ$ plane (orange)", fontsize=8)
ax.set_xlabel(r"$u$"); clean(ax)
fig.subplots_adjust(wspace=0.12)
save(fig, "ld_augusti.pdf")

# ------------------------------------------------ 5. Ziegler's column
fig, axs = plt.subplots(1, 2, figsize=(6.3, 2.3))
p = np.linspace(0, 3, 600)
disc = (2 * p - 7)**2 - 8
pf = 3.5 - np.sqrt(2)
ax = axs[0]
for sg in (1, -1):
    sq = np.where(disc >= 0, np.sqrt(np.abs(disc)), np.nan)
    stable(ax, p, (7 - 2 * p + sg * sq) / 4)
re = np.where(disc < 0, (7 - 2 * p) / 4, np.nan)
unstable(ax, p, re, color=ORANGE)
ax.axvline(pf, color=ORANGE, lw=0.7, ls=":")
ax.text(pf + 0.05, 2.6, r"$p_f = \frac{7}{2}-\sqrt{2}$", fontsize=8, color=ORANGE)
ax.set_xlabel(r"$p = Pl/k$"); ax.set_ylabel(r"$\omega^2 m l^2/k$"); clean(ax)
ax = axs[1]
sys.path.insert(0, os.path.join(HERE, "..", "python"))
from ex_ziegler import growth_rates, critical
cs = np.logspace(-3, -0.3, 25)
ax.semilogx(cs, [critical(c) for c in cs], color=CU)
ax.axhline(pf, color=ORANGE, lw=0.8, ls=":")
ax.axhline(41 / 28, color=GRAY, lw=0.8, ls=":")
ax.text(1.2e-3, pf + 0.04, "undamped", fontsize=8, color=ORANGE)
ax.text(1.2e-3, 41 / 28 - 0.12, r"limit $c\to 0$", fontsize=8, color=GRAY)
ax.set_xlabel(r"damping $c$"); ax.set_ylabel(r"flutter load $p_f$"); ax.set_ylim(1.2, 2.3); clean(ax)
fig.subplots_adjust(wspace=0.35)
save(fig, "ld_ziegler.pdf")
