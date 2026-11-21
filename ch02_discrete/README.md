# Chapter 2: Discrete systems: energy and Lagrangian mechanics

Label prefix `ld` (`sec:ld-*`, `eq:ld-*`, `fig:ld-*`, `exo:ld-*`, bibitem keys `ld-*`).
Status: outline drafted (21 Nov 2026). The Outline frame part is written; the seven sections, the
summary and the exercises are planned as `\draftnote`s in `notes/ch02_discrete.tex`.

## Outline (2 h lecture; minutes are a target)
1. `sec:ld-lagrange` Energy and Lagrange's equations (15'): 2-dof chain of rigid bars first; T, M, ℰ, Q;
   equilibrium; linearised motion M v̈ + K v = 0; a frequency goes to zero at the critical load.
2. `sec:ld-hessian` Energy criterion and Hessian (15'): K = ℰ,uu positive definite; det K = 0, mode ¹u;
   limit vs bifurcation point (¹uᵀℰ,uη, the fold test of Ch. 1 with w = v); Box 2.1.
3. `sec:ld-koiter` Koiter, simple critical point (25'): η = η_c + η₁ξ + η₂ξ²; stable symmetric
   (Ch. 1 bar), unstable symmetric (lateral spring, P = kL cos θ), asymmetric (45° spring,
   P/P_c = 1 − ¾θ, P_c = kL/2); 2 dof with ²u, the passive coordinate lowers η₂.
4. `sec:ld-imperfect` Imperfection sensitivity (15'): one-half and two-thirds power laws, stable case
   ξ̄^{1/3}; exact vs asymptotic curves; link to the cusp of Ch. 1; preview of Ch. 7.
5. `sec:ld-snap` Snap-through, von Mises truss (15'): limit point, jump, hysteresis; limit points are
   not imperfection-sensitive; 2-dof asymmetric bifurcation (open, see below).
6. `sec:ld-interaction` Mode interaction, Augusti column (10'): two modes, quartic energy, coupled paths;
   naive optimisation (Thompson, Bushnell §7).
7. `sec:ld-flutter` Ziegler's column (15'): follower load, no potential, static method fails; kinetic method;
   flutter at P_f = (7/2 − √2) k/l ≈ 2.086 k/l; destabilisation paradox, ≈ 1.464 k/l with small equal damping.

Exercises: short questions (8–10), problems (H1, H2, sample exam, imperfect spring bars, shallow truss,
Beck's column with 2 dof), computer: (a) `code/mathematica/koiter.wl` + `code/python/koiter_sympy.py`
(symbolic η_c, ¹u, ²u, η₁, η₂), (b) `code/python/ex_imperfection.py` (exact η_m by continuation with
`ch01_bifurcation/code/python/arclength.py` vs power laws), (c) `code/python/ex_ziegler.py` (eigenvalue loci).
Session `exercises/ch02_session.tex`: (a) Hessian and Koiter by hand on the inclined-spring bar,
(b) Mathematica, (c) Python.

## Notation (proposal, to be confirmed by the author)
Column of generalised coordinates `\mat{u}` (as in `preamble/notation.tex`), mass matrix `\mat{M}`,
kinetic energy T, generalised non-conservative forces `\mat{Q}`, stiffness (Hessian) `\mat{K} = ℰ,uu`,
principal branch ⁰u(η), mode ¹u, amplitude ξ, second-order field ²u, post-buckling coefficients η₁, η₂
(Triantafyllidis's λ₁, λ₂), imperfection amplitude ξ̄ (Hutchinson & Koiter), maximum load η_m, flutter load P_f.
These go into the notation list when the sections are written.

## Checks already made (SymPy/NumPy, scratch scripts, not in the repo)
- 45° spring bar: P/(kL) = 1/2 − 3θ/8 + θ²/16 + …, so P/P_c = 1 − ¾θ.
- Ziegler (2m, m): undamped 2.08579 k/l = 7/2 − √2; equal dampers c → 0: 1.4643 k/l.
- Von Mises, elastic bars only: limit point, no asymmetric bifurcation (h/a = 0.2, 0.5; apex spring 0–1).
- Augusti, two kinematics with rotational springs: diagonal coupled path stiffer than the single-plane path.

## Decisions and open questions
- Notation (hub, 21 Nov 2026): load parameter η, energy ℰ(u, η), critical load η_c; λ is not used for the load.
- Ch. 1 covers the 1-dof bar, its imperfection and the cusp; Ch. 2 recalls the bar only as the stable-symmetric case.
- Ch. 1 covers Hopf and the trace–determinant plane; Ch. 2 uses them for Ziegler without new theory.
- Continuation stays light here (reuse of `arclength.py`); FE and Riks/Crisfield are Ch. 3, which checks its
  codes on these models.
- Open: 2-dof von Mises model with an asymmetric bifurcation: which extra ingredient (Triantafyllidis
  two-bar truss pp. 41–45, or Pecknold, Ghaboussi & Healey 1985)?
- Open: the spring kinematics of the Augusti model (Thompson & Hunt 1973; Bažant & Cedolin 1991).
- Open: the 2-dof example where ²u changes the sign of η₂ (Triantafyllidis T model, or a chain with a
  nonlinear spring).
- Open: does the von Mises truss replace the fishery of Ch. 1 as the fold example? (draftnote in Ch. 1, §6)
- Sources needed in this thread: Triantafyllidis notes A (pp. 8–45), H1, H2, sample exam; the relevant
  chapters of Thompson & Hunt (1973) and Bažant & Cedolin (1991).

## Sources
Thompson & Hunt, Koiter, Bažant & Cedolin, Triantafyllidis notes A (T model, square plate, two-bar truss, LSK), H1, H2, sample exam.
Details and page numbers: `SOURCES.md`. Ask the author to upload a file when it is needed.
