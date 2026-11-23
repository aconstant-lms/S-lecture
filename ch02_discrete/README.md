# Chapter 2: Discrete systems: energy and Lagrangian mechanics

Label prefix `ld` (`sec:ld-*`, `eq:ld-*`, `fig:ld-*`, `exo:ld-*`, bibitem keys `ld-*`).
Status: complete draft (21 Nov 2026): lecture text, exercises with solutions, 2 h session with
answers and instructor notes. Two open questions in red (von Mises truss with 2 dof, Augusti).
Slides: not started.

## Content
1. `sec:ld-lagrange` Energy and Lagrange's equations: column of two bars (Ziegler's geometry) under a dead
   load, 𝒲, K, M, Q; linearised motion; frequencies go to zero at P_c = (3 − √5)/2 · k/l.
2. `sec:ld-hessian` Energy criterion (gbox), critical point and mode, limit vs bifurcation test
   ¹uᵀ𝒲,uη (Chapter 1's wᵀf_r with w = v); Box 2.1.
3. `sec:ld-koiter` Koiter: rigid T model (Triantafyllidis AB-1); general LSK expansion; κ', 𝒲₃, 𝒲₄;
   η₁ = −𝒲₃/(2κ'), η₂ = −(𝒲₄ + 3𝒲,ijk ²uᵢ¹uⱼ¹uₖ)/(3κ'); Box 2.2; the three link models of Thompson & Hunt
   §1.2 (η₂ = η_c/3, −η_c; η₁ = −¾η_c); gbox: passive coordinates can only lower η₂.
4. `sec:ld-imperfect` Imperfections: imperfect T model; reduced equations; 1/2 and 2/3 laws (gbox);
   Figure: exact vs asymptotic curves.
5. `sec:ld-snap` Two-bar (von Mises) truss with 2 dof (Triantafyllidis AB-5, Green strains): limit point;
   sideways bifurcation only for φ > 54.7°, before the limit point for φ > 60°; η₂ = −2c²/R, and
   +0.838 instead of −0.524 at 65° without the passive coordinate. Red note: asymmetry.
6. `sec:ld-interaction` Augusti column (Thompson & Hunt §10.4): secondary bifurcation P^C = (3c₁ + c₂)/(4L),
   coincident case PL = c/(1 + u²/3), P_m L/c ≈ 1 − (3ε/2)^{2/3}; optimum design (gbox). Red note: asymmetry.
7. `sec:ld-flutter` Ziegler's column: follower load, det K = k², kinetic criterion,
   P_f = (7/2 − √2) k/l; destabilisation paradox, 1.4643 k/l (= 41/28 to five digits) as c → 0.

Exercises: 8 short questions, 5 problems (column of two bars, lateral and inclined bars, steep truss,
rotating mechanism after the MEC553 sample exam), 3 computer exercises (Koiter coefficients,
imperfection curves + truss by continuation, Ziegler).

## Files
- `notes/ch02_discrete.tex` chapter; `figures/ld_*.pdf` made by `code/figures/fig_ch2.py`
  (`ld_tmodel`, `ld_imperfection`, `ld_truss`, `ld_augusti`, `ld_ziegler`); two TikZ sketches inline.
- `code/python/`: `koiter_sympy.py` (Box 2.2 for n dof, all models), `ex_imperfection.py`
  (exact vs asymptotic maximum loads; steep truss with a sideways load, using
  `ch01_bifurcation/code/python/arclength.py`), `ex_ziegler.py` (growth rates, flutter, damping).
- `code/mathematica/koiter.wl` (same steps as `koiter_sympy.py`).
- `exercises/ch02_session.tex` 2 h session: (a) T model by hand, (b) Koiter by computer algebra on the
  steep truss, (c) imperfection curves and Ziegler in Python. Listed in `preamble/manual_chapters.tex`.

## Decisions and open questions
- Notation (author, 21 Nov 2026, accepted): `\mat{u}`, `\mat{K}`, `\mat{M}`, T, `\mat{Q}`, ⁰u(η), ¹u, ξ, ²u,
  η = η_c + η₁ξ + ½η₂ξ² (Triantafyllidis's Taylor convention), κ', 𝒲₃, 𝒲₄, imperfection ξ̄, maximum
  load η_m, flutter load P_f. In `preamble/notation.tex` and the notation list.
- (author, 21 Nov 2026) The von Mises truss replaces the fishery as the fold example of Chapter 1
  (Example `ex:st-vonmises`, Figure `fig:st-vonmises`, Exercise `exo:st-vonmises`); the fishery is in
  `ch01_bifurcation/extra/fishery.tex`.
- Open (author: keep in red): the symmetric two-bar truss bifurcates only for φ > 54.7°; a realistic
  2-dof example of limit point vs bifurcation probably needs an asymmetry (unequal bars, off-apex load).
- Open (author: keep in red): Augusti shows symmetric interaction (quartic coupling); add an asymmetric
  interaction (one-half law), as in stiffened panels?
- The Augusti kinematics is settled: springs act on the angles whose sines are the tip displacements
  (Thompson & Hunt §10.4). With projected angles or successive rotations the coupling is stabilising:
  that is a different model.
- The Mathematica file has not been run (no Mathematica here); the SymPy twin gives all numbers in the
  text. Marked `\untested` in the instructor manual.
- Bažant & Cedolin is not available (author): cited only for Beck's column and physical examples.
- Triantafyllidis homeworks H1, H2 were not uploaded; the problems use the notes, Thompson & Hunt and
  the sample exam instead.

## Sources
- Triantafyllidis, MEC563 notes: energy criterion pp. 20–21; rigid T model pp. 24–31; two-bar truss
  pp. 41–45; LSK simple mode pp. 57–64 (η₁, η₂: AC-3.13, AC-3.14); imperfections pp. 65–71 (AC-4.14, AC-4.31).
- Thompson & Hunt (1973): link models §1.2, book pp. 3–21 (PDF 19–39); Augusti model and erosion of an
  optimum design §10.4, book pp. 243–249 (PDF 260–266).
- MEC553 sample exam (2018), Problem 1: rotating mechanism (Exercise `exo:ld-rotating`).
- Ziegler (1968) for the column and the paradox; Koiter (1945); Hutchinson & Koiter (1970).
