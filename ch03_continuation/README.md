# Chapter 3: From continuum to discrete: numerical methods

Label prefix `nc` (`sec:nc-*`, `eq:nc-*`, `fig:nc-*`, `exo:nc-*`, bibitem keys `nc-*`).
Folder name `ch03_continuation` kept (21 Nov 2026).
Status: outline (21 Nov 2026). The Outline frame part is written: objectives and plan. The sections carry their
planned content as `\draftnote`s. Nothing else is drafted yet.

## Planned content (author's list, 21 Nov 2026)
Weak forms; linear buckling as an eigenproblem; the eigenproblem as a weak (variational) optimisation
problem; Riks arc-length; branch switching; detecting bifurcations. Exercises: first steps in FEniCS (with
SLEPc for eigenproblems) and Cast3M, both on the two-bar truss of the Chapter 2 session, so that students
check against known answers.

1. `sec:nc-weak` From the energy to the weak form: the column first (weak form, P_c = π²EI/L²), then the elastic
   body (Green–Lagrange strain, ℂ, 𝒦). First variation = virtual work; second variation = material + initial-stress
   term (Trefftz).
2. `sec:nc-fe` From fields to matrices: interpolation; residual r = f_int(u) − η p; tangent K = material + geometric
   K_σ. The truss as two bar elements gives exactly Ch. 2's (eq:ld-truss-K). Box 3.1.
3. `sec:nc-lba` Linear buckling: (K₀ + η K_σ) ¹u = 0, Box 3.2. When it fails: the truss (below).
4. `sec:nc-rayleigh` The eigenproblem as a minimisation: Rayleigh quotient, Courant–Fischer min–max, Rayleigh–Ritz
   upper bounds (column with w = x(L − x): 12 EI/L², +21.6 %), FE converges from above; link with vibrations
   (Constantinescu & Korsunsky §7.5).
5. `sec:nc-riks` Arc-length: load/displacement control fail; Riks (normal plane) and Crisfield (sphere, root choice);
   bordering (two solves with K, no augmented matrix); scaling and step control. Box 3.3. Builds on Box 1.2.
6. `sec:nc-detect` Detection: det K, smallest eigenvalues (SLEPc), inertia by negative pivots of LDLᵀ (Sylvester);
   bisection or extended system; limit vs bifurcation by ¹uᵀp (Ch. 2 test).
7. `sec:nc-switch` Branch switching: bifurcation equation / Koiter coefficients; perturbation along the mode;
   imperfection in the shape of the mode (also gives the imperfection sensitivity).
8. `sec:nc-tools` Two FE codes, a short map: FEniCS (UFL, `derivative`, SNES, SLEPc) and Cast3M (KSIG, VIBR, PASAPAS).

## Known answers for the exercises (two-bar truss, EA = L = 1, Green–Lagrange strain)
Checked with SymPy in this thread. Classical linear buckling = K₀ + η K_σ about the undeformed state.
| φ | exact critical point | linear buckling (K_σ only) | K₀ + η dK/dη |
|---|---|---|---|
| 30° | limit point η_max = 2s³/(3√3) = 0.0481 | 0.250 (vertical), 0.750 (sideways) | 0.0833 |
| 65° | sideways bifurcation 0.2434 (η₂ = −0.524), limit 0.2865 | 0.324 (sideways), 1.49 (vertical) | 0.324 / 0.496 |

Lessons: at 30° linear buckling is 5.2 times too high (snap-through, nonlinear prebuckling); at 65° it is 33 % too
high. The linear buckling load depends on the strain measure in K_σ. With Green strain, K_σ = (N/L) I per bar.
With the small-rotation geometric matrix (N/L)(I − eeᵀ) the 30° value becomes 2s³/c² = 0.333. State the
convention used by FEniCS and by Cast3M's KSIG, and check it in the code.

## Exercise session (2 h): plan
(a) By hand, 30 min: the truss as two bar elements; K₀, K_σ, linear buckling at 30° and 65°, compared with the exact
values of Chapter 2. (b) FEniCS, 45 min: two interval elements in the plane, energy in UFL, Newton, linear
buckling with SLEPc, then arc-length through the limit point at 30°. (c) Cast3M, 45 min: the same truss,
KSIG + VIBR, PASAPAS with arc-length; at 65° switch branches with a sideways load 10⁻³ η (Ch. 2: η_m = 0.2407).
Computer exercises in the notes: the same three, plus Riks–Crisfield from scratch in Python (reusing
`ch01_bifurcation/code/python/arclength.py`).

## Decisions and open questions
- (author, 21 Nov 2026) Title "From continuum to discrete: numerical methods" replaces "Continuation and finite
  elements"; folder and prefix unchanged. The hub should update the plan table in `CLAUDE.md`, `README.md` and the
  roadmap in `ch00_intro/notes/overview.tex`.
- The two-bar truss of Chapter 2 is the test case of the whole chapter. The Euler column is used only in its
  linearised form, for the weak form and Rayleigh–Ritz. The elastica stays in Chapter 4.
- Mode symbol in linear buckling: ¹u, as in Chapter 2 (not φ, which is the truss angle).
- Open: ANM (Cochelin, Damil, Potier-Ferry) was in the old plan but is not in the author's list. Proposal: one
  paragraph in `sec:nc-riks`, or drop it.
- Open: FEniCS version. Proposal: FEniCSx (dolfinx ≥ 0.9, petsc4py/slepc4py), not legacy FEniCS. Arc-length has to be
  written by hand on top of the Newton solver.
- Open: Cast3M version and keywords (KSIG, VIBR, PASAPAS arc-length option). Check them against the author's Cast3M
  version. The author's repository `Castem_Introduction` may have reusable inputs.
- New notation to propose when drafting: residual `\mat{r}`, reference load vector `\mat{p}`, `\mat{K}_0`, `\mat{K}_\sigma`,
  Green–Lagrange strain `\tens{E}` and 2nd Piola–Kirchhoff stress `\tens{S}`, bilinear forms a, b, and a `\grad`
  operator (no macro yet in `preamble/notation.tex`).
- Bibliography to add, after checking against the sources: Bushnell (1981), §4 on when linear bifurcation is enough;
  Crisfield, *Non-linear Finite Element Analysis of Solids and Structures* (Wiley, 1991/1997); Wriggers & Simo
  (1990) or Wriggers, Wagner & Miehe (1988) for the extended system; the SLEPc paper (Hernandez, Roman & Vidal, 2005).

## Sources
Triantafyllidis L6 (FEM for stability), Riks, Crisfield, Keller; Constantinescu & Korsunsky Ch. 7 (Rayleigh–Ritz
§7.4, free vibrations §7.5); Bushnell (1981) §4. Details and page numbers: `SOURCES.md`. Please upload
Triantafyllidis's L6 slides and Constantinescu & Korsunsky Ch. 7 for the drafting round.
