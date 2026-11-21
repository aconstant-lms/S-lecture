# Working on the lecture notes "Stability in Mechanics" (working title)

Author: Andrei Constantinescu (LMS, CNRS & Ecole Polytechnique). LaTeX book, see README.md for the layout.
Same model as the NPM notes (https://github.com/aconstant-lms/npm-lecture): style, notation and chapter
frame are shared. When a convention changes in one book, check whether it should change in the other.

## Conventions (apply to every edit)
- Notation lives in `preamble/notation.tex`; use its macros, never ad-hoc bold:
  vectors and 2nd-order tensors bold italic (`\vu`, `\vn`, `\sig`, `\eps`, `\vect{}`, `\tens{}`),
  4th-order tensors blackboard bold (`\bbC`, `\bbS`, `\bbI`, `\tensf{}`), matrices bold upright (`\mat{K}`).
  The 2nd-order tensor of diffusion coefficients is `\bbK` (blackboard bold), as in the NPM notes.
- Style is the RG style of the NPM notes (`preamble/style.tex`): short declarative sentences, sans-serif headings,
  key statements in `gbox`, exercises with `\exercise{Title}\label{exo:...}` + `solution` environment.
- Every chapter (and appendix) follows the frame: `\framepart{Outline}` (objectives + plan), numbered
  sections, `\framepart{Summary}` (a `gbox*` of bold-led items), `\framepart{Exercises}` (sub-parts with
  `\framesub{...}`), and the `chapterbib` which prints the `References` frame part. Frame parts are
  unnumbered, in small caps: refer to them with `\pageref`/`\nameref`, never `\ref`.
  `ch01_bifurcation/notes/ch01_bifurcation.tex` is the template.
- Index concepts with `\index{concept}` or `\index{concept!subconcept}` on the line after a section label,
  `\paragraph`, `gbox` title or exercise label (never inside captions or math). Reuse existing top-level
  entries instead of creating near-duplicates; use `sortkey@Display` for accents/math.
- In running text, inline integrals and fractions are written with `\displaystyle`; `\tfrac` stays small.
  Not in tables, captions or headings.
- Key statements (Strang style): no Theorem/Proposition/Lemma/Corollary/Definition environments by default.
  A key result is a `gbox` whose title states the claim in words, with its `\label` right after
  `\begin{gbox}{...}`; the argument follows as `\paragraph{Why it works.}`, starting from the picture,
  then the short chain of formulas. Cite it as "Section~\ref{...}" or with `\nameref`, never "Theorem~\ref".
  Numbered `example` environments are kept. Before a general statement, prefer a small worked example
  with numbers or matrices.
- Algorithms: in the chapter text, Simo & Hughes "Box" style (a `gbox` titled `Box <ch>.<n>  <title>`,
  numbered steps); in exercise parts, CMAME-style pseudocode (`algorithm` + `algpseudocode`).
- Exercises start with `\framesub{Short questions}` (exam-style, short solutions), then `\framesub{Problems}`
  or thematic sub-parts.
- Constraints are added to Lagrangians with the sign `-\lambda\,(\mat{P}\vu-\vuD)`, so that the multiplier is
  the reaction (positive).
- New symbols go into the notation list `ch00_intro/notes/notation_list.tex` as well as `preamble/notation.tex`.
- Each chapter ends with its own `chapterbib`; bibitem keys must be unique across the whole book.
- Labels are prefixed per chapter (table in "Course plan" below): `ch:<p>`, `sec:<p>-*`, `eq:<p>-*`,
  `fig:<p>-*`, `exo:<p>-*`, bibitem keys `<p>-*`. Appendices `app:*`.
- Author comments in the sources look like `%% AC: ...`; process them when asked, then delete them.
- Red `\draftnote{...}` marks open questions for the author; leave them unless resolved.

## Style models
- Gilbert Strang (*Introduction to Applied Mathematics*, *Computational Science and Engineering*,
  *Differential Equations and Linear Algebra*): mathematically precise, but not overburdened. Short sentences,
  one idea each; the picture and a small example before the general statement; few symbols, each one used.
  Displayed formulas are not crowded: no long chains of `\quad`/`\qquad` or hand-made spacing (`\,`, `\!`,
  `\hspace`) beyond what the notation needs; split a long display into short steps instead.
- Editorial line (author, Nov 2026): **structural engineering first, with some physical examples.** The spine is
  Thompson & Hunt, Bažant & Cedolin, Brush & Almroth, Koiter, Guckenheimer & Holmes; design practice comes from
  Bushnell (1981) and NASA SP-8007; Audoly & Pomeau, Reis, Bertoldi, Hutchinson give physical examples and pictures.

## Notation sources (see SOURCES.md for details)
- Continuum mechanics and elasticity: the author's book, Constantinescu & Korsunsky, *Elasticity with Mathematica*
  (CUP 2007): σ = C : ε, data with superscript D (u^D, b^D, t^D on ∂Ω^u, ∂Ω^t), admissible sets 𝒦, 𝒮
  (`\Kad`, `\Sad`), potential energy 𝒰_p(u), residual stress σ_0, temperature θ, operators grad, div, curl.
- Stability and Koiter/LSK asymptotics: Triantafyllidis's MEC563 notes, with **η** in place of his λ:
  energy ℰ(u, η) with load parameter η, principal branch ⁰u(η), critical point (u_c, η_c), mode ¹u,
  amplitude ξ, derivatives ℰ,uu, ℰ,uuu.
- Decided (author, 21 Nov 2026): the Hooke tensor is blackboard ℂ (`\bbC`), as in the NPM notes, not the bold
  C of the book; the load parameter is **η** (`\eta`) from Chapter 2 on. λ stays for growth rates (Chapter 1),
  Lagrange multipliers and the Lamé constant. Chapter 1 keeps its control parameter r and load P.

## Repository structure
`SOURCES.md` (sources and what to take from each) sits next to this file. One folder per chapter, the same sub-folders everywhere:

    main.tex                     the book (lecture notes); \include{<chNN>/notes/<chNN>}
    exercise_sheets.tex          exercise sessions, questions only (students)
    instructor_manual.tex        same sessions with answers and instructor notes
    preamble/                    style.tex, notation.tex (book), manual.tex + manual_chapters.tex
                                 (sessions), slides.tex (Beamer decks), index.ist
    ch00_intro/                  front matter: titlepage, overview (roadmap), notation_list
    chNN_<name>/                 one chapter (NN = 01..09), with
      README.md                  planned content, status, decisions of the chapter thread
      notes/chNN_<name>.tex      the chapter of the book
      exercises/chNN_session.tex the 2 h exercise session (sheet + answers + instructor notes)
      slides/cNN_<name>.tex      Beamer deck, compiled from its own folder; FIG/ for slide-only pictures
      figures/                   PDF figures of the notes (also used by the slides)
      code/python|mathematica|fenics|cast3m/   computer codes of the chapter
      code/figures/              scripts that produce figures/
      extra/                     material kept for later revisions (not compiled)
    appendices/appX_<name>/      appendices, same sub-folders

Sessions: `\sessiontitle`, parts `\spart`, questions `\q` (or `\qc` for code questions), `answer` and
`instructor` environments (printed only in the instructor manual). Cite the book as `\ref{B-sec:...}`.
A new session is listed in `preamble/manual_chapters.tex`.

## Course plan (9 lectures of 2 h + 9 exercise sessions of 2 h)
Progression in dimension: discrete, 1D, 2D, 3D. Each chapter follows the same path: closed form on the
simplest model, Mathematica for asymptotics, Python for continuation, FEniCS and Cast3M for the full problem,
checked against the closed form. A running example: the cylinder (1 dof model, ring, shell, 3D solid).

| Ch | Folder | Prefix | Title | Content |
|---|---|---|---|---|
| 0 | `ch00_intro` | `in` | Introduction | front matter, course overview |
| 1 | `ch01_bifurcation` | `st` | Differential equations and bifurcation | slope test, normal forms, imperfections, rigid bar (drafted) |
| 2 | `ch02_discrete` | `ld` | Discrete systems: energy and Lagrangian mechanics | Hessian, Koiter with 1-2 dof, von Mises truss, Augusti, Ziegler (flutter) |
| 3 | `ch03_continuation` | `nc` | Continuation and finite elements | pseudo-arclength, Riks/Crisfield, branch switching, linear buckling, ANM, FEniCS/Cast3M |
| 4 | `ch04_rods` | `rd` | Rods: the elastica and beyond | Kirchhoff rods, elastica, elastic foundation, twist and natural curvature |
| 5 | `ch05_thinwalled` | `tw` | Thin-walled members and real materials | torsional buckling, cruciform column, Shanley, residual stresses, column curves |
| 6 | `ch06_plates` | `pl` | Plates | Föppl-von Kármán, plate buckling, effective width, wrinkling, d-cones |
| 7 | `ch07_cylinders` | `cy` | Cylindrical shells and imperfection sensitivity | classical load, Koiter, knockdown factors, rocket fuselage |
| 8 | `ch08_shells` | `sh` | Shells in service: nozzles, prestress and deployable structures | external pressure, nozzle divergent, bistable shells, tape springs, kirigami |
| 9 | `ch09_solids` | `so` | Three-dimensional bodies | Hill, loss of ellipticity, Biot wrinkling, pattern transformation; projects |

Assessment (proposal, to be confirmed): exam + project in pairs from session 5 on, one real structure.
Status of each chapter: its `README.md`. Skeleton chapters carry the planned content as `\draftnote`s.

## Reference list (to grow; each chapter copies what it cites into its own chapterbib)
- Textbooks: Thompson & Hunt, *A General Theory of Elastic Stability* (1973); Bažant & Cedolin, *Stability of
  Structures* (1991); Brush & Almroth, *Buckling of Bars, Plates, and Shells* (1975); Timoshenko & Gere,
  *Theory of Elastic Stability* (1961); Audoly & Pomeau, *Elasticity and Geometry* (2010); Nguyen Q. S.,
  *Stability and Nonlinear Solid Mechanics* (2000); Koiter (1945, NASA TT F-10833, 1967).
- Dynamical systems: Strang, *Differential Equations and Linear Algebra* (2014); Strogatz (2015);
  Guckenheimer & Holmes (1983); Seydel (2010); Bergé, Pomeau & Vidal, *L'ordre dans le chaos* (1984).
- Numerics: Keller (1977); Riks (1979); Crisfield (1981); Allgower & Georg (2003); Cochelin, Damil &
  Potier-Ferry, *Méthode asymptotique numérique* (2007); Logg, Mardal & Wells (FEniCS book, 2012).
- Shells and design: von Kármán & Tsien (1941); NASA SP-8007; Calladine (1983); Singer, Arbocz & Weller,
  *Buckling Experiments*; Elishakoff (2014); Hutchinson & Koiter (1970); Hutchinson (1967, 1974).
- Recent papers for examples and illustrations: Reis (2015, buckliphobia to buckliphilia); Lee, López Jiménez,
  Marthelot, Hutchinson & Reis (2016); Virot, Kreilos, Schneider & Rubinstein (2017); Bertoldi, Vitelli,
  Christensen & van Hecke (2017); Mullin, Deschanel, Bertoldi & Boyce (2007); Rafsanjani & Bertoldi (2017);
  Gomez, Moulton & Vella (2017); Cerda & Mahadevan (2003); Bergou et al., discrete elastic rods (2008);
  Kebadze, Guest & Pellegrino (2004); Seffen & Pellegrino (1999); Östlund & Muhammad-Klingmann (2005).
- Design and course material: Bushnell, Buckling of shells — pitfall for designers, *AIAA J.* 19 (1981) 1183–1226
  (paper + slides); NASA SP-8007 (Weingarten, Seide & Peterson, rev. 1968) and NASA/SP-8007-2020/REV 2
  (Hilburger, 2020); Triantafyllidis, *Stability of Solids: from Structures to Materials*, MEC563 notes (École
  polytechnique, 2011) and MEC553 slides and homeworks (2018); Constantinescu & Korsunsky (2007).
- What to take from each source, with page numbers and a chapter map: `SOURCES.md`. The files are not in the
  repository (public, copyrighted); ask the author to upload them in the thread that needs them.
- Before a reference enters a chapterbib, check its details (authors, journal, volume, pages) against the source.

## Threads: one hub, one thread per chapter
- The hub thread (course plan, structure, cross-chapter decisions) owns this file, `README.md`,
  `ch00_intro/` and `preamble/`.
- Each chapter thread works in its own folder `chNN_<name>/`, and touches other files only for
  cross-references, notation (`preamble/notation.tex` + `ch00_intro/notes/notation_list.tex`),
  `main.tex` and `preamble/manual_chapters.tex`.
- At the start of a chapter thread: read this file, `SOURCES.md`, `chNN_<name>/README.md`, and the chapters before it.
- At the end of each round: update `chNN_<name>/README.md` (status, decisions, open questions). A decision
  that affects other chapters (notation, plan, a result used later) is also written under
  "Cross-chapter decisions" below, in one dated line, so the hub and the other threads see it.
- Pull before working (`git pull --rebase`); two threads may push on the same day.

## Cross-chapter decisions
- 2026-11-21: one folder per chapter; 9-chapter plan above; Chapter 1 keeps the prefix `st`.
- 2026-11-21: editorial line structural engineering + physical examples; sources recorded in `SOURCES.md`;
  elasticity notation from Constantinescu & Korsunsky, LSK notation from Triantafyllidis.
- 2026-11-21: Hooke tensor ℂ (blackboard, `\bbC`); load parameter η from Chapter 2 on (notation list updated).
- 2026-11-21 (Ch. 1 thread): Lyapunov stability, Jacobian eigenvalues and the Hopf bifurcation (galloping example)
  are introduced in Chapter 1; Chapter 2 reuses them (Ziegler, flutter) instead of introducing Hopf.
- 2026-11-21 (Ch. 1 thread): Chapter 1 gives the ideas of continuation on one equation (natural parameter vs
  pseudo-arclength, augmented Jacobian, zero eigenvalue Jv = 0 with fold test wᵀf_r ≠ 0, Box 1.2) and a Python
  code `ch01_bifurcation/code/python/arclength.py` for n unknowns; Chapter 3 builds on it (FE, Riks/Crisfield).
  Matrix notation for ODE systems: `\mat{y}`, `\mat{J}`, `\mat{v}`, `\mat{w}`, `\mat{u}=(\mat{y},r)`, `\widehat{\mat{J}}`.
- 2026-11-21 (Ch. 2 thread): Chapter 2 notation accepted: generalised coordinates `\mat{u}`, stiffness
  `\mat{K} = ℰ,uu`, mass `\mat{M}`, ⁰u(η), ¹u, ξ, ²u; η = η_c + η₁ξ + ½η₂ξ² (Taylor convention of Triantafyllidis);
  κ', ℰ₃, ℰ₄; imperfection amplitude ξ̄; maximum load η_m; flutter load P_f. Box 2.2 (Koiter's coefficients) and
  `ch02_discrete/code/python/koiter_sympy.py` (n dof) are reused for the elastica, plates and shells.
- 2026-11-21 (Ch. 2 thread, author): the von Mises truss replaces the fishery in Chapter 1 (fold example);
  the fishery moves to `ch01_bifurcation/extra/`.
- 2026-11-21 (Ch. 3 thread, author): Chapter 3 is retitled "From continuum to discrete: numerical methods" (folder
  `ch03_continuation` and prefix `nc` unchanged): weak forms, linear buckling as an eigenproblem and as a Rayleigh-quotient
  minimisation, Riks arc-length, detection, branch switching; the Chapter 2 two-bar truss is its FEniCS/Cast3M test case.
  Hub: update the plan table, `README.md` and `ch00_intro/notes/overview.tex`.

## Workflow
- One conversation per chapter; touch other files only when needed (cross-references, notation).
- Build: `pdflatex -interaction=nonstopmode main.tex` three times (all paths are relative to the repository root). Before committing, the log must have
  no undefined references, no multiply-defined labels and no overfull boxes.
- Code lives in the chapter folder: `<chNN>/code/{python,mathematica,fenics,cast3m}/`, figure scripts in
  `<chNN>/code/figures/` (run from their own directory, outputs into `<chNN>/figures/`). Code is printed in
  exercise solutions with `\lstinputlisting[firstline=4]{<chNN>/code/python/...}` after the results stated in
  words. Never paste code inline in the .tex. The book itself does not mention the repository.
- Commit with a clear message per round of corrections and push to `main`. The commit message becomes
  the release note, so make it readable for the author.
- Every push to `main` triggers `.github/workflows/build-pdf.yml`, which compiles the book and publishes
  `S_lecture_notes.pdf` on the release "latest": https://github.com/aconstant-lms/s-lecture/releases/latest
  After pushing, check the run succeeded and give the author that link.
- `.github/workflows/build-extras.yml` builds the exercise sheets, the instructor manual and every deck
  `ch*/slides/c*.tex` when their sources change, and uploads `S_exercise_sheets.pdf`, `S_instructor_manual.pdf`,
  `S_slides_cNN_*.pdf` to the same release. Slide and manual PDFs are not versioned.
