# Chapter 1: Differential equations and bifurcation

Label prefix `st` (historical; `sec:st-*`, `eq:st-*`, `fig:st-*`, `exo:st-*`, bibitem keys `st-*`).
Status: complete draft (21 Nov 2026): lecture text, exercises with solutions, 2 h session with
answers and instructor notes. Slides: still the skeleton deck. Template chapter of the book.

## Content
1. Growth and decay, ẏ = ay.
2. Steady states and the slope test.
3. Lyapunov stability: definitions, direct method (Lyapunov function), damped oscillator and energy,
   Lagrange–Dirichlet, Jacobian eigenvalues (first method), trace–determinant plane: divergence vs flutter.
4. The pitchfork: symmetry breaking, critical slowing down.
5. Why bifurcations happen: implicit function theorem (one variable, then the precise statement for
   n unknowns with box/graph, contraction argument, Rudin Thm 9.28, Krantz & Parks; inverse function
   theorem as its twin; the circle: fold = wrong choice of variable, branch point = no variable works,
   Figure `st_ift`); zero eigenvalue **Jv = 0**,
   left eigenvector **w**, fold (wᵀf_r ≠ 0) vs branch point (wᵀf_r = 0).
6. Fold, transcritical, pitchfork: normal forms, reduction from Taylor coefficients (table), von Mises truss
   (snap-through at a fold; replaces the fishery, 21 Nov 2026).
7. Hopf bifurcation: complex normal form, first Lyapunov coefficient ℓ₁ (Guckenheimer–Holmes 3.4.11),
   galloping of a square prism (Den Hartog, Parkinson–Smith).
8. Potential energy, buckling and imperfections: rigid bar, cusp, hysteresis.
9. Continuation: natural parameter (fails at folds), pseudo-arclength (Keller), augmented Jacobian
   invertible at folds and singular at branch points; each step is the implicit function theorem
   with the arclength as parameter; Box 1.2, detection and branch switching.

Exercises: 9 short questions, 9 problems, 4 computer exercises (pitchfork, hysteresis,
pseudo-arclength from scratch, normal forms in Mathematica).

## Files
- `notes/ch01_bifurcation.tex` chapter; `figures/st_*.pdf` made by `code/figures/fig_ch1.py`
  (new: `st_lyapunov`, `st_tracedet`, `st_hopf`, `st_continuation`, `st_ift`; the last one imports `code/python/arclength.py`)
- `code/python/`: `ex_pitchfork.py`, `ex_hysteresis.py`, `ex_galloping.py`, `arclength.py`
  (pseudo-arclength from scratch, Box 1.2), `normal_forms_sympy.py` (classification, cusp, ℓ₁)
- `code/mathematica/`: `normal_forms.wl`, `arclength.wl` (same steps as the Python/SymPy versions)
- `exercises/ch01_session.tex` 2 h session: (a) stability by hand, (b) pseudo-arclength from scratch,
  (c) normal forms in Mathematica; `slides/c01_bifurcation.tex` deck (skeleton)

## Decisions and open questions
- Table-top (24 Nov 2026): plastic ruler pushed on a kitchen scale, then pre-bent (pitchfork vs imperfection).
- Energy, buckling and imperfections of one-degree-of-freedom systems are covered here;
  Chapter 2 starts from several degrees of freedom and Koiter's analysis.
- (21 Nov 2026) Hopf bifurcation, Lyapunov's two methods and the Jacobian are introduced here
  (ODE level, galloping example); Chapter 2 reuses them for Ziegler's column (flutter).
- (21 Nov 2026) Continuation is introduced here for one equation and small n (ideas, Box 1.2,
  augmented Jacobian, branch switching at a pitchfork); Chapter 3 keeps n-dof/FE continuation,
  Riks/Crisfield, step control, and the linear buckling eigenproblem. `arclength.py` is written for
  n unknowns and can be reused there.
- Notation: state column `\mat{y}`, Jacobian `\mat{J}`, null vectors `\mat{v}`, `\mat{w}`,
  continuation unknowns `\mat{u} = (\mat{y}, r)`, tangent `\mat{t}`, augmented Jacobian
  `\widehat{\mat{J}}`, Lyapunov function W, Hopf amplitude ρ and coefficient ℓ₁ (notation list updated).
- Open: the Mathematica files have not been run in Mathematica yet (no Mathematica in the build
  environment); the SymPy/Python versions were run and give the numbers in the text. Marked with
  `\untested` in the instructor manual.
- (author, 21 Nov 2026, Ch. 2 thread) The fishery is replaced by the von Mises truss (Example `ex:st-vonmises`,
  Figure `fig:st-vonmises` made by block 5 of `fig_ch1.py`, Problem `exo:st-vonmises`). The fishery text, its
  exercise, its figure and the old figure code are kept in `extra/fishery.tex` and `extra/st_fishery.pdf`.
- Open: the deck `slides/c01_bifurcation.tex` still has to be written from the notes.

## Sources
Strang, Strogatz, Guckenheimer & Holmes, Kuznetsov, Seydel, Thompson & Hunt; Lyapunov (1892/1992),
Hopf (1942), Keller (1977), Allgower & Georg (2003), Den Hartog (1932), Parkinson & Smith (1964).
Details and page numbers: `SOURCES.md`. Ask the author to upload a file when it is needed.

## Papers needed
(ask the author to upload them; tick when received)
