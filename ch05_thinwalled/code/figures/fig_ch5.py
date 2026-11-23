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
