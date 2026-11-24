"""Figures of Chapter 5 (thin-walled members and real materials).

Run from this directory:  python3 fig_ch5.py
Writes the PDFs into ../../figures (tw_*.pdf). Same conventions as fig_ch4.py:
stable branches solid blue, unstable or comparison paths gray, critical points orange, green for comparisons.
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "python"))
from shanley import Pt, Pr, L, d, closed, path

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

# Shanley's column: perfect paths (left) and imperfect paths (right) -----------------------
fig, axs = plt.subplots(1, 2, figsize=(6.3, 2.5), sharey=True)
x = np.linspace(0, 1.5, 300)
ax = axs[0]; clean(ax)
ax.plot([0, 0], [0, Pr / Pt], color=CU, lw=1.2)
for Pb in np.linspace(Pt, Pr, 5)[1:-1]:
    ax.plot(x, closed(x, Pb) / Pt, color=GRAY, lw=0.9)
    ax.plot([0], [Pb / Pt], "o", color=GRAY, ms=2.5)
ax.plot(x, closed(x) / Pt, color=CU)
ax.axhline(Pr / Pt, color=GREEN, ls="--", lw=1.0)
ax.plot([0], [1], "o", color=ORANGE, ms=4)
ax.text(1.5, Pr / Pt + 0.03, r"$P_r$ (reduced modulus)", ha="right", va="bottom", fontsize=8, color=GREEN)
ax.text(0.05, 0.96, r"$P_t$", ha="left", va="top", fontsize=8, color=ORANGE)
ax.set_xlim(-0.05, 1.5); ax.set_ylim(0.6, 1.62)
ax.set_xlabel(r"rotation $x = L\theta/d$"); ax.set_ylabel(r"$P/P_t$")
ax.set_title("perfect column", fontsize=8.5)

ax = axs[1]; clean(ax)
ax.plot(x, closed(x) / Pt, color=CU)
ax.plot([0, 0], [0, 1], color=CU, lw=1.2)
for tb, ls in ((1e-3, "-"), (1e-2, "--"), (5e-2, ":")):
    res = path(tb, 1.5 * d / L, n=1500)
    ax.plot(L * res[:, 0] / d, res[:, 1] / Pt, color=GRAY, lw=1.1, ls=ls, label=rf"$\bar\theta = {tb:g}$")
ax.legend(loc="lower right", frameon=False)
ax.axhline(Pr / Pt, color=GREEN, ls="--", lw=1.0)
ax.plot([0], [1], "o", color=ORANGE, ms=4)
ax.set_xlim(-0.05, 1.5)
ax.set_xlabel(r"rotation $x = L\theta/d$")
ax.set_title("imperfect columns", fontsize=8.5)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "tw_shanley.pdf")); plt.close(fig)
print("wrote tw_shanley.pdf")

# Cruciform and angle: buckling stress against length -------------------------------------
from ft_section import cruciform, angle
E, G = 210e3, 81e3
fig, axs = plt.subplots(1, 2, figsize=(6.3, 2.5))
ax = axs[0]; clean(ax)
X = cruciform(120.0, 8.0)
Ls = np.linspace(300, 6000, 300)
st, sf, sm = [], [], []
for L in Ls:
    P, _, d = X.loads(L, E, G)
    st.append(d["P_phi"] / X.A); sf.append(d["P_minaxis"] / X.A); sm.append(P[0] / X.A)
ax.plot(Ls / 1e3, sf, color=GRAY, ls="--", lw=1.0, label="flexure (Euler)")
ax.plot(Ls / 1e3, st, color=GREEN, ls="--", lw=1.0, label=r"torsion, $G(t/b)^2$")
ax.plot(Ls / 1e3, sm, color=CU, label="buckles at")
Lx = np.pi * 120.0**2 / 8.0 * np.sqrt(E / (6 * G))
ax.plot([Lx / 1e3], [G * (8 / 120)**2], "o", color=ORANGE, ms=4)
ax.set_ylim(0, 800); ax.set_xlim(0, 6)
ax.set_xlabel(r"length $L$ (m)"); ax.set_ylabel(r"stress $P/A$ (MPa)")
ax.set_title(r"cruciform, $b = 120$, $t = 8$ mm", fontsize=8.5); ax.legend(frameon=False, loc="upper right")

ax = axs[1]; clean(ax)
An = angle(97.0, 6.0)
Ls = np.linspace(200, 4000, 300)
fl, tw_, ft, lo = [], [], [], []
for L in Ls:
    P, V, d = An.loads(L, E, G)
    fl.append(d["P_minaxis"] / An.A); tw_.append(d["P_phi"] / An.A)
    ftv = P[1] if abs(V[0, 0]) > 0.9 * np.linalg.norm(V[:, 0]) else P[0]
    ft.append(ftv / An.A); lo.append(P[0] / An.A)
ax.plot(Ls / 1e3, fl, color=GRAY, ls="--", lw=1.0, label="minor-axis flexure")
ax.plot(Ls / 1e3, tw_, color=GREEN, ls="--", lw=1.0, label="twist alone")
ax.plot(Ls / 1e3, ft, color=ORANGE, ls=":", lw=1.2, label="flexural-torsional")
ax.plot(Ls / 1e3, lo, color=CU, label="buckles at")
ax.set_ylim(0, 800); ax.set_xlim(0, 4)
ax.set_xlabel(r"length $L$ (m)")
ax.set_title(r"equal angle $100\times100\times6$", fontsize=8.5); ax.legend(frameon=False, loc="upper right")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "tw_sections.pdf")); plt.close(fig)
print("wrote tw_sections.pdf")

# Column curves ---------------------------------------------------------------------------
from fibre_column import max_load, ec3, crc, LAMS
fig, ax = plt.subplots(figsize=(5.0, 3.0)); clean(ax)
lam = np.linspace(0.01, 2.5, 400)
ax.plot(lam, np.minimum(1, 1 / lam**2), color=GRAY, ls="--", lw=1.0, label="Euler and yield")
for a, nm, ls in ((0.21, "a", "-"), (0.34, "b", "--"), (0.49, "c", "-."), (0.76, "d", ":")):
    ax.plot(lam, ec3(lam, a), color=CU, lw=1.0, ls=ls, label=f"European curve {nm}")
ax.plot(lam, crc(lam), color=GREEN, lw=1.0, label="CRC parabola (AISC)")
pts = {k: [max_load(l, *v) for l in LAMS] for k, v in
       (("s", ("strong",)), ("w", ("weak",)), ("w0", ("weak", False)))}
ax.plot(LAMS, pts["s"], "o", color=ORANGE, ms=3.5, label="fibre column, strong axis")
ax.plot(LAMS, pts["w"], "s", color=ORANGE, ms=3.5, mfc="none", label="fibre column, weak axis")
ax.plot(LAMS, pts["w0"], "x", color=GRAY, ms=4, label="weak axis, no residual stress")
ax.set_xlim(0, 2.5); ax.set_ylim(0, 1.1)
ax.set_xlabel(r"slenderness $\bar\lambda = \sqrt{A f_y/P_c}$"); ax.set_ylabel(r"$\chi = P_{\max}/(A f_y)$")
ax.legend(frameon=False, fontsize=6.5, loc="lower left")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "tw_curves.pdf")); plt.close(fig)
print("wrote tw_curves.pdf")
