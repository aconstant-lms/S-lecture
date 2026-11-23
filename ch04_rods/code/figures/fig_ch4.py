"""Figures of Chapter 4 (rods: three models, the elastica, the foundation, the imperfect column).

Run from this directory:  python3 fig_ch4.py
Writes the PDFs into ../../figures (rd_*.pdf). Same conventions as fig_ch2.py:
stable branches solid blue, unstable dashed gray, critical points orange, green for comparisons.
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "python"))
from elastica import exact, shape
from ex_stability import branch, spectrum

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

def clean(ax):
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

th = np.radians(np.linspace(0.2, 172, 400))
P, W, D = np.array([exact(t) for t in th]).T

# 1. Three rods, three diagrams (the author's slide 11) ------------------------------
fig, axs = plt.subplots(1, 3, figsize=(6.3, 2.2), sharey=True)
titles = ["no rotation (bar)", "small rotations", "large rotations (elastica)"]
for ax, ti in zip(axs, titles):
    clean(ax); ax.set_title(ti, fontsize=8.5); ax.set_xlim(-0.45, 0.45); ax.set_ylim(0, 4.6)
    ax.set_xlabel(r"$w(L/2)/L$")
axs[0].set_ylabel(r"$P/P_c$")
axs[0].plot([0, 0], [0, 4.6], color=CU)
for ax in axs[1:]:
    ax.plot([0, 0], [0, 1], color=CU); ax.plot([0, 0], [1, 4.6], color=GRAY, ls="--")
    ax.plot([0], [1], "o", color=ORANGE, ms=4); ax.plot([0], [4], "o", color=ORANGE, ms=4)
axs[1].plot([-0.45, 0.45], [1, 1], color=CU); axs[1].plot([-0.45, 0.45], [4, 4], color=GRAY, ls="--")
TOUCH = np.radians(130.709)                       # the first branch loses stability where the ends touch
for n, col, ls in ((1, CU, "-"), (2, GRAY, "--")):
    for sg in (1, -1):
        m = (P * n**2 <= 4.6) & ((th <= TOUCH) | (n > 1))
        axs[2].plot(sg * W[m] / n, n**2 * P[m], color=col, ls=ls)
        if n == 1:
            m2 = (P <= 4.6) & (th >= TOUCH)
            axs[2].plot(sg * W[m2], P[m2], color=GRAY, ls="--")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "rd_models.pdf")); plt.close(fig)

# 2. The elastica: load against end rotation, and shapes ------------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.3, 2.5), gridspec_kw={"width_ratios": [1, 1.25]})
clean(a1)
st = th <= np.radians(130.709)
a1.plot(np.degrees(th[st]), P[st], color=CU, label="exact (elliptic)")
a1.plot(np.degrees(th[~st]), P[~st], color=GRAY, ls="--")
a1.plot([130.71], [2.1834], "o", color=ORANGE, ms=4)
a1.plot(np.degrees(th), 1 + th**2 / 8, color=GREEN, ls="-.", label=r"Koiter $1 + \theta_0^2/8$")
ts = np.radians([20, 40, 60, 90, 120, 150])
a1.plot(np.degrees(ts), [exact(t)[0] for t in ts], "o", ms=3.5, mfc="white", color=ORANGE,
        label="shooting")
a1.set_xlabel(r"end rotation $\theta_0$ (deg)"); a1.set_ylabel(r"$P/P_c$")
a1.set_xlim(0, 175); a1.set_ylim(0.9, 4.0); a1.legend(frameon=False, loc="upper left")
clean(a2); a2.set_aspect("equal")
for deg in (20, 60, 90, 130.71, 160):
    x, w = shape(np.radians(deg))
    col, ls = (ORANGE, "-") if abs(deg - 130.71) < 1 else ((GRAY, "--") if deg > 131 else (CU, "-"))
    a2.plot(x, w, color=col, ls=ls, lw=1.3)
    i = np.argmax(w); a2.text(x[i], w[i] + 0.02, f"{deg:.0f}$^\\circ$", ha="center", fontsize=7)
a2.plot([0, 1], [0, 0], color=GRAY, lw=0.8)
a2.set_xlabel(r"$x/L$"); a2.set_ylabel(r"$w/L$"); a2.set_ylim(-0.05, 0.52)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "rd_elastica.pdf")); plt.close(fig)

# 3. The foundation: P(q) and the festoon of a finite beam ----------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.3, 2.4))
clean(a1)
q = np.linspace(0.3, 3, 300)
a1.plot(q, 0.5 * (q**2 + 1 / q**2), color=CU, label=r"$P/P_c$")
a1.plot(q, 0.5 * q**2, color=GRAY, ls=":", lw=1.1); a1.plot(q, 0.5 / q**2, color=GRAY, ls=":", lw=1.1)
a1.text(2.45, 2.5, "bending", fontsize=7.5, color=GRAY); a1.text(0.33, 3.3, "foundation", fontsize=7.5, color=GRAY)
a1.plot([1], [1], "o", color=ORANGE, ms=4)
a1.set_xlabel(r"wavenumber $q/q_c$"); a1.set_ylabel(r"$P/P_c$"); a1.set_ylim(0, 4); a1.set_xlim(0, 3)
clean(a2)
L = np.linspace(0.5, 5.2, 600) * np.pi
env = np.full_like(L, np.inf)
for n in range(1, 7):
    Pn = 0.5 * ((n * np.pi / L) ** 2 + (L / (n * np.pi)) ** 2)
    a2.plot(L / np.pi, Pn, color=GRAY, lw=0.9, ls="--"); env = np.minimum(env, Pn)
a2.plot(L / np.pi, env, color=CU)
for n in range(1, 5):                             # mode jumps, L q_c/pi = sqrt(n(n+1))
    a2.plot([np.sqrt(n * (n + 1))], [0.5 * (n / (n + 1) + (n + 1) / n)], "o", color=ORANGE, ms=3.5)
a2.set_ylim(0.9, 2.2); a2.set_xlim(0.5, 5.2)
a2.set_xlabel(r"length $L\,q_c/\pi$"); a2.set_ylabel(r"$P/P_c$")
for n, x in ((1, 0.85), (2, 1.95), (3, 2.95), (4, 3.95), (5, 4.9)):
    a2.text(x, 1.02, f"$n={n}$", fontsize=7, ha="center")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "rd_foundation.pdf")); plt.close(fig)

# 4. The imperfect column and the Southwell plot --------------------------------------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.3, 2.4))
clean(a1)
w = np.linspace(0, 0.12, 400)
for a, col in ((0.002, CU), (0.01, GREEN), (0.03, ORANGE)):
    p = w / (w + a)
    a1.plot(w, p, color=col, label=rf"$\bar a = {a}\,L$")
a1.plot([0, 0], [0, 1], color=GRAY, ls="--"); a1.plot([0, 0.12], [1, 1], color=GRAY, ls="--")
a1.set_xlabel(r"added deflection $w(L/2)/L$"); a1.set_ylabel(r"$P/P_c$")
a1.set_ylim(0, 1.1); a1.legend(frameon=False, loc="lower right")
clean(a2)
a = 0.002; p = np.array([0.4, 0.55, 0.7, 0.8, 0.88])
d = a * p / (1 - p)
a2.plot(d * 1e3, d / p * 1e3, "o", color=ORANGE, ms=4)
dd = np.linspace(0, d.max() * 1.1, 10); a2.plot(dd * 1e3, (dd + a) * 1e3, color=CU)
a2.set_xlabel(r"$w(L/2)/L\ \ (\times 10^{-3})$"); a2.set_ylabel(r"$(w/L)/(P/P_c)\ \ (\times 10^{-3})$")
a2.text(4, 3.0, r"slope $=1/P_c$" "\n" r"intercept $=\bar a$", fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "rd_imperfect.pdf")); plt.close(fig)
# 5. Stability of the elastica branches: the lowest eigenvalues of the second variation ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.3, 2.4))
degs = np.linspace(3, 172, 70)
for n, col in ((1, CU), (2, GREEN), (3, ORANGE)):
    lam = np.array([spectrum(*branch(n, np.radians(d)), ne=300, nev=4) for d in degs])
    a1.plot(degs, lam[:, n - 1] / np.pi**2, color=col, label=f"mode {n}")
    a2.step(degs, (lam < -1e-6).sum(axis=1), where="mid", color=col, label=f"mode {n}")
for a in (a1, a2):
    clean(a); a.axvline(130.71, color=GRAY, lw=0.8, ls=":"); a.set_xlabel(r"end rotation $\theta_0$ (deg)")
a1.axhline(0, color=GRAY, lw=0.8)
a1.set_ylabel(r"$n$-th eigenvalue $/\pi^2$"); a1.set_ylim(-1, 3.2); a1.legend(frameon=False, loc="upper right")
a2.set_ylabel("unstable directions"); a2.set_yticks([0, 1, 2, 3]); a2.set_ylim(-0.2, 3.4)
a2.text(135, 0.3, "ends touch", fontsize=7.5, color=GRAY)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "rd_stability.pdf")); plt.close(fig)
print("written:", sorted(f for f in os.listdir(OUT) if f.startswith("rd_")))
