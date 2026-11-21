"""Figures of Chapter 3 (from continuum to discrete: numerical methods).

Run from this directory:  python3 fig_ch3.py
Writes the PDFs into ../../figures (nc_*.pdf). Same conventions as fig_ch2.py:
stable branches solid blue, unstable dashed gray, critical points black, linear buckling orange.
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "python"))
from truss_fe import von_mises, linear_buckling, follow, locate, switch
from ex_bearing import critical_loads
from ex_ritz_column import hermite_fe

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


# ------------------------------------------------ 1. truss: arc-length path against linear buckling
fig, axs = plt.subplots(1, 2, figsize=(6.3, 2.5))
for ax, phi, ds in zip(axs, (30, 65), (0.01, 0.01)):
    m = von_mises(phi)
    path = follow(m, np.zeros(2), 0.0, ds, 400 if phi == 30 else 260)
    v = np.array([-p[0][1] for p in path]); eta = np.array([p[1] for p in path])
    npv = np.array([p[2] for p in path])
    ok = v <= 2 * np.sin(np.radians(phi)) + 0.05
    split_plot(ax, v[ok], eta[ok], npv[ok] == 0)
    lba = linear_buckling(m)[0][0]
    ax.axhline(lba, color=ORANGE, lw=1.0, ls=(0, (2, 2)))
    ax.text(0.02, lba - 0.01, "linear buckling", color=ORANGE, va="top", fontsize=7.5)
    ax.axhline(0, color=(0.8, 0.8, 0.8), lw=0.6, zorder=0)
    k = [i for i in range(1, len(path)) if npv[i] != npv[i - 1]]
    uc, ec, mode, kind = locate(m, path[k[0] - 1], path[k[0]])
    ax.plot(-uc[1], ec, "o", color="k", ms=4, zorder=6)
    if phi == 65:
        ub, eb = switch(m, uc, ec, mode, 0.02)
        br = follow(m, ub, eb, 0.01, 400, du0=ub - uc, deta0=eb - ec)
        bv = np.array([-p[0][1] for p in br]); be = np.array([p[1] for p in br])
        sel = np.arange(len(br)) <= np.argmax(bv)          # half circle in (u, v): v from s - R to s + R
        unstable(ax, np.append(-uc[1], bv[sel]), np.append(ec, be[sel]), color=ORANGE)
        ax.plot(bv[sel][-1], be[sel][-1], "o", color="k", ms=4, zorder=6)
        ax.set_ylim(-0.32, 0.38)
    else:
        ax.set_ylim(-0.07, 0.3)
    ax.set_xlabel(r"apex deflection $v/L$"); clean(ax)
    ax.set_title(rf"$\varphi = {phi}^\circ$", fontsize=9)
axs[0].set_ylabel(r"load $\eta/EA$")
save(fig, "nc_truss.pdf")

# ------------------------------------------------ 2. bearing: buckling in compression and in tension
fig, ax = plt.subplots(figsize=(4.6, 2.7))
g = np.logspace(-2, 2, 200)                       # GA / P_E
r = np.sqrt(1 + 4 / g)
ax.plot(g, g / 2 * (r - 1), color=CU, label="Haringx, compression")
ax.plot(g, -g / 2 * (r + 1), color=ORANGE, label="Haringx, tension")
ax.plot(g, 1 / (1 + 1 / g), color=GRAY, ls=(0, (4, 3)), label="Engesser (no tension root)")
for gg in (0.03, 0.1, 0.3, 1, 3, 10):
    c, t = critical_loads(200, 1.0, 1.0, gg * np.pi**2, "haringx")
    ax.plot(gg, c / np.pi**2, "o", color=CU, ms=3, zorder=5)
    ax.plot(gg, t / np.pi**2, "o", color=ORANGE, ms=3, zorder=5)
ax.axhline(0, color=(0.8, 0.8, 0.8), lw=0.6, zorder=0)
ax.set_xscale("log"); ax.set_ylim(-4, 1.6)
ax.set_xlabel(r"shear stiffness $GA_s/P_E$"); ax.set_ylabel(r"critical load $P/P_E$")
ax.legend(frameon=False, loc="center right"); clean(ax)
save(fig, "nc_bearing.pdf")

# ------------------------------------------------ 3. column: finite elements converge from above
fig, ax = plt.subplots(figsize=(3.2, 2.4))
ns = np.array([1, 2, 4, 8, 16, 32])
err = np.array([hermite_fe(n)[0] / np.pi**2 - 1 for n in ns])
ax.loglog(ns, err, "o-", color=CU, ms=3.5)
ax.loglog(ns[2:], err[2] * (ns[2:] / ns[2])**-4.0, color=GRAY, lw=0.9, ls=(0, (3, 2)))
ax.text(9, 2e-4, "slope $-4$", color=GRAY, fontsize=7.5)
ax.set_xlabel("number of elements"); ax.set_ylabel(r"$P_h/P_c - 1$"); clean(ax)
save(fig, "nc_ritz.pdf")
