# Chapter 3: From continuum to discrete: numerical methods

Label prefix `nc` (`sec:nc-*`, `eq:nc-*`, `fig:nc-*`, `exo:nc-*`, bibitem keys `nc-*`).
Folder name `ch03_continuation` kept (21 Nov 2026).
Status: complete draft (21 Nov 2026). Lecture text, exercises with solutions, and the 2 h session with answers and
instructor notes. Three open questions are marked in red: ANM, the bearing example, and the untested FEniCSx/Cast3M
inputs. Slides: not started.

## Content
1. `sec:nc-weak` From the energy to the weak form. The column first: weak form, natural boundary condition,
   P_c = π²EI/L². Then the elastic body in the notation of the author's MEC563 L03 slides: Saint Venant–Kirchhoff,
   e(u) = ε(u) + ½q(u,u), q(v,w) = sym(gradᵀv grad w), and the first and second variations. A gbox: the weak form
   is the gradient, the stability operator the Hessian. The column's load work is the initial-stress term.
2. `sec:nc-fe` From fields to matrices. Residual r = f_int − ηp, tangent K. Bar element with Green strain:
   k = (EA/L³)xxᵀ + (N/L)I. Example: the truss from two elements gives Ch. 2's Hessian. Box 3.1.
3. `sec:nc-lba` Linear buckling (K₀ + ηK_σ)¹u = 0 (Triantafyllidis L6, slide 9). Box 3.2. Table on the truss:
   30°: 0.250 against 0.0481 (×5.2), consistent 0.0833; 65°: 0.324 against 0.2434 (+33 %). Gbox: reliable only
   if the prebuckling state is nearly linear (Bushnell). Figure `nc_truss`.
4. `sec:nc-rayleigh` The eigenproblem as a minimisation. Column with x(L − x): 12 (+21.6 %); x²(L − x) changes
   nothing (symmetry); x³(L − x): +0.056 %. Rayleigh quotient gbox, with the weak form of the eigenproblem
   (C&K §7.5, eq. 7.59). Ritz/FE upper bounds and the min–max principle; Hermite elements converge from above
   at rate h⁴ (figure `nc_ritz`). The sign of b: negative eigenvalues are buckling under the reversed load.
   **Example: a rubber bearing buckles in tension.** Haringx vs Engesser, Kelly 2003, Kelly & Takhirov 2007,
   Bažant 2003 (figure `nc_bearing`). Marked in red as a proposal for the author.
5. `sec:nc-riks` Arc-length. Load control fails at η = 0.050; displacement control and snap-back; bordering;
   Riks (plane) and Crisfield (sphere, root choice). Box 3.3. The truss at 30°: 81 points, agrees with the exact
   path to 10⁻¹¹.
6. `sec:nc-detect` Detection by negative pivots of LDLᵀ (Sylvester; L6 slides 3 and 6), with a gbox. Bisection,
   the extended system (Wriggers & Simo 1990), classification by ¹uᵀp. Numbers for both angles.
7. `sec:nc-switch` Branch switching along the mode (the circle of Ch. 2 reproduced to 10⁻¹³, unstable) and
   through an imperfection (maximum loads 0.2428, 0.2407, 0.2315, the two-thirds law). Gbox.
8. `sec:nc-tools` FEniCS (UFL, derivative, SLEPc shift-invert) and Cast3M (sigm 'LINE', ksigma 'FLAM',
   flambage, pasapas). Gbox: trust a code after it has reproduced a closed form. The linear buckling load
   (0.250 against 0.333) reveals which geometric matrix a code uses.

Exercises: 8 short questions; 4 problems (Ritz and FE column, truss as bar elements, the extended system,
Engesser and Haringx); 4 computer exercises (arc-length from scratch, the bearing, FEniCS, Cast3M).

## Files
- `notes/ch03_continuation.tex`: the chapter. `figures/nc_truss.pdf`, `nc_ritz.pdf` and `nc_bearing.pdf` are made by
  `code/figures/fig_ch3.py`.
- `code/python/truss_fe.py`: bar elements with Green strain, K₀, K_σ, linear buckling, Riks/Crisfield by
  bordering, negative pivots (scipy `ldl`), bisection, branch switching. It is a general bar code, reusable later.
- `code/python/ex_truss.py`: all truss numbers of the chapter. `ex_ritz_column.py`: Ritz and Hermite FE for the column.
  `ex_bearing.py`: Timoshenko column, Engesser vs Haringx, tension root.
- `code/fenics/truss_fenicsx.py`: dolfinx 0.9. The energy is written in UFL, the derivatives come from `derivative`,
  linear buckling uses SLEPc (GNHEP, shift-invert at 0), and the path reuses the Python driver. **Not run.**
- `code/cast3m/truss.dgibi`: `flambage` (after the author's Cast3M guide, ch_eigen) and `pasapas` with
  `'GRANDS_DEPLACEMENTS'` and imposed apex deflection. **Not run.**
- `exercises/ch03_session.tex`: the 2 h session. (a) Truss matrices and linear buckling by hand; (b) FEniCS,
  with Algorithm 3.1 (arc-length by bordering, CMAME style); (c) Cast3M. Listed in `preamble/manual_chapters.tex`.

## Decisions and open questions
- (author, 21 Nov 2026) The title is "From continuum to discrete: numerical methods". Folder and prefix are unchanged.
  The hub should update the plan table in `CLAUDE.md`, `README.md` and the roadmap in `ch00_intro/notes/overview.tex`.
- The Chapter 2 two-bar truss is the test case of the whole chapter. The Euler column is used only in its
  linearised form, for the weak form and Rayleigh–Ritz. The elastica stays in Chapter 4.
- Large strains: §3.1 uses the author's MEC563 L03 slides (St Venant–Kirchhoff, e = ε + ½q, K + λK_G with
  K_G ↔ ∫q(v,w):σ⁰). Polar decomposition, constitutive choices and loss of ellipticity stay for Chapter 9.
- Geometric stiffness convention: Green strain, K_σ ↔ ∫σ̂:q(v,w), as in L6 slide 9. For a bar this is (N/L)I.
  The small-rotation matrix (N/L)(I − eeᵀ) gives 0.333 instead of 0.250 at 30°. The chapter uses this difference
  as a check on codes.
- Symbols: the arc-length weight is ψ (Crisfield); the plate rotation of the bearing is θ. The mode is ¹u, as in Ch. 2.
- Open (red): the ANM paragraph, or drop it.
- Open (red, proposal): the bearing that buckles in tension is the "surprising example" asked for by the author
  (21 Nov 2026). Keep it here, move it to Ch. 9 with a FEniCS plane-strain bearing, or drop it?
  A second candidate is tensile buckling with a slider (Zaccaria, Bigoni, Noselli & Misseroni 2011).
- Open (red): the FEniCSx and Cast3M inputs have not been run. FEniCSx could not be installed in the build
  environment: pip has no wheel and the conda download was refused. Cast3M is not available. Run both once,
  and check which geometric matrix `ksigma` uses for `barr` and which strain measure `pasapas` uses for bars.
  Arc-length in `pasapas` was not found in the author's guide; the truss does not need it.
- FEniCSx version: dolfinx 0.9 API (`fem.functionspace`, `create_mesh` with a `ufl.Mesh`,
  `assemble_matrix(..., diagonal=0.0)`).

## Sources
- Triantafyllidis, MEC553 Lecture 6 (2018), slides 3–9: incremental Newton–Raphson, LDLᵀ stability check and
  bisection, the geometric stiffness method and its caution. Slides 10–24 (fibre composites) are for Ch. 9.
- Constantinescu & Korsunsky (2007), Ch. 7: §7.2 extremum theorems (book p. 192, PDF p. 204); §7.4 Rayleigh–Ritz
  (book pp. 197–199, PDF pp. 209–211); §7.5 free vibrations, Rayleigh quotient, orthogonality, approximate spectra
  (book pp. 204–209, PDF pp. 216–221).
- Author, MEC563 "Large strains and stability analysis" (L03 slides, 43 p.): e = ε + ½q, energy, Newton–Raphson,
  K_G, critical points (limit vs bifurcation), 3D buckling eigenproblem.
- Audoly & Pomeau (2010) §2.5 (book pp. 47–48): small strain and finite rotations, second Piola–Kirchhoff
  stress, and the ambiguity of the stress under finite rotations (cited in §3.1 and in the bearing example).
- The author's Cast3M guide (repository `Castem_Introduction`, ch_eigen and ch_largestrain): ksigma 'FLAM',
  flambage, pasapas entries.
- Checked references: Kelly (2003), Kelly & Takhirov (2007), Bažant (2003), Wriggers & Simo (1990).
  Riks (1979), Crisfield (1981), Hernandez, Roman & Vidal (2005) are as in the hub list or standard.
