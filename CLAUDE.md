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

## Balance in Chapters 4-8: 3D link, engineering, physical examples (author, 23 Nov 2026)
Every structural chapter has three layers, in this order and roughly these proportions:
1. **From 3D (about 15 %)**, one short section. The physical assumptions and energy scalings in the spirit of
   Audoly & Pomeau (bending cheap, stretching expensive), then what the mathematics proves, with its precise
   assumptions: asymptotic expansions in the thickness (Ciarlet's school) and Γ-convergence (Friesecke, James,
   Müller; Mora & Müller). State which scaling of loads and displacements gives which model, and when the
   reduced model fails (thick walls, supports, local plasticity). Continuum notation of the author's book.
   Precise statements go in a `gbox`, proofs are cited, not reproduced. Rods: Ch. 4 §`sec:rd-3d` (done);
   plates: Ciarlet (1980) + the author's note CO7 on the von Kármán plate; shells: Ciarlet Vol. III, Ciarlet & Lods.
2. **Engineering core (about two thirds)**: Thompson & Hunt, Koiter, Brush & Almroth for theory and solutions,
   Bushnell and NASA SP-8007 for design and failures. Exercises and projects live here.
3. **Physical examples (about 20 %)**: one or two boxed examples per chapter, kept only if they show a mechanism
   already in the engineering problem (same equations) and carry a scaling law students can check, ideally on a
   table top (Audoly & Pomeau, Reis, Bertoldi, Cerda & Mahadevan, Virot et al.). Otherwise they go to `extra/`.
Chapter 9 closes the loop: Hill's 3D criterion recovers Euler for a slender bar and shows where reduced theories end;
the running cylinder example compares a reduced model with a 3D FEniCS solid.

### Balance check (hub, 23 Nov 2026; source lines of the chapter body, rough). To redo when examples move.
| Ch | From 3D | Engineering core | Physical examples | Remarks |
|---|---|---|---|---|
| 1 | — | galloping, von Mises truss, rigid bar | logistic eq. (fishery in `extra/`) | method chapter, rule not applied |
| 2 | — | ≈100 % (T model, trusses, Augusti, Ziegler) | none | add short pointers to real structures (below) |
| 3 | ≈35 % (weak form, 3D bifurcation) | rubber bearing, truss | none | method chapter, fine |
| 4 | ≈20 % | ≈70 % (Euler, design, rails, foundation) | ≈10 %, scattered | gather the A&P passages into one boxed example |
| 5-9 | planned | planned | planned | Ch. 6 and 8 risk too much physics, Ch. 2, 5, 7 too little |
Candidate moves and additions (decided in the chapter threads, examples may come later):
- Ch. 2: real-structure pointers in one line each — von Mises truss → shallow arches and domes (snap-through);
  Augusti → optimised stiffened panels (Bushnell §7, modal interaction); Ziegler → pipes conveying fluid.
  A physical box (jumping popper, Venus flytrap snap) belongs to Ch. 8, with a forward reference from Ch. 2.
- Ch. 4: "a rod standing up", the pendulum analogy and the localised helix (telephone cord) in one boxed example;
  "a stiff skin on a soft core / thin film" moves to Ch. 6 (wrinkling), only the forward reference stays.
- Ch. 6: engineering core = buckling and effective width of stiffened panels (aircraft skins, box girders);
  wrinkling and d-cones as one or two boxes, not a full section.
- Ch. 7: physical box = poking a soda can (Virot et al.), energy barrier; it ties back to the knockdown factors.
- Ch. 8: engineering first (tanks and Bushnell's gallery, external pressure, nozzle divergent, space deployables:
  tape springs); bistable shells, kirigami and metamaterials as boxes, part of them possibly in Ch. 9.
- Ch. 9: Biot wrinkling and Bloch-wave instabilities of honeycombs (Triantafyllidis L7) carry the engineering
  side; pattern transformation (Mullin et al.) as the box.

### Who owns what (overlap check, hub, 23 Nov 2026)
A topic is developed once, in its owner chapter; the others recall it in one sentence and cite it.
| Topic | Owner | Others (refer, do not redo) |
|---|---|---|
| Stability of ODEs, Lyapunov, Jacobian, Hopf, normal forms | Ch. 1 | Ch. 2 (flutter uses Hopf) |
| Pseudo-arclength on ODEs (Box 1.2, `arclength.py`) | Ch. 1 | Ch. 3 extends to FE (Box 3.3 bordering, `truss_fe.py`) |
| von Mises truss: 1 dof fold | Ch. 1 | Ch. 2 adds the sideways dof, Ch. 3 is its FE test case |
| Energy criterion, Hessian, Koiter's coefficients (Box 2.2), imperfection power laws | Ch. 2 | Ch. 3 (variations), Ch. 4-8 use them |
| Vibration and buckling (ω² → 0, Southwell by vibration) | Ch. 2 (Ch. 1 one exercise) | Ch. 7 vibration correlation technique on shells |
| Weak form, variations, Green–Lagrange `e = ε + ½q(u,u)`, 3D bifurcation, Koiter for a body | Ch. 3 | Ch. 4, 6, 7 use them; Ch. 9 starts from `sec:nc-bif` (Hill adds uniqueness, ellipticity) |
| Linear buckling, Rayleigh quotient, Ritz, arc-length, pivots, branch switching, the codes | Ch. 3 | all later chapters |
| Shear-soft columns, Engesser–Haringx, rubber bearing | Ch. 3 | Ch. 4-5 refer |
| Euler loads, effective length, elastica (exact), Southwell plot, secant formula, foundation | Ch. 4 | Koiter coefficients of the elastica stay in Ch. 3 (eq. `nc-elastica-koiter`) |
| From 3D to the rod (fibre strain, three energies) | Ch. 4 | Ch. 6 follows the same pattern for the plate, Ch. 7 for the shell |
| Wrinkling, thin film on soft substrate | Ch. 6 | Ch. 4 one sentence, Ch. 9 surface instability of the half-space |
| Twist, natural curvature, tape springs | Ch. 8 | Ch. 4 remark only |
| Inelastic buckling, tangent modulus, column curves | Ch. 5 | Ch. 4 design only through the secant formula |
Points to watch: (1) the vibration–buckling link appears in Ch. 1 (exercise) and Ch. 2 (example + exercise):
keep, they build, but Ch. 7 must only cite them; (2) two "from scratch" continuation exercises (Ch. 1 ODE, Ch. 3 FE):
the Ch. 3 one should start from the Ch. 1 code; (3) Ch. 6, built on the author's note CO7, must reuse Ch. 3's
Green–Lagrange notation and variations and mirror Ch. 4's "From 3D" section, not restate them
(CO7's ê, κ̂, hats → Ch. 3 notation; W → 𝒲; λ → η).

## Figures and sketches
- Figures should be **nice, structured and inspirational**: a reader should grasp the mechanism from the picture
  before reading the formulas (Strang: the picture first). Every section with a new structure, load case or idea
  gets a sketch.
- **Sketches in TikZ**: structures, supports, springs, loads, buckling modes, imperfections, geometry of rods,
  plates and shells, energy landscapes, flow charts of the method. One file per sketch in
  `<chNN>/figures/tikz/<p>_<name>.tex` (a bare `tikzpicture`), `\input` in the notes and reused in the slides.
- **Plots** (bifurcation diagrams, equilibrium paths, knockdown curves, computed fields) from the chapter scripts
  in `<chNN>/code/figures/` (matplotlib or pgfplots), never screenshots.
- One visual language across the book: the shared styles and colours of `preamble/style.tex` (`cu` blue for the
  kinematic side and stable branches, `cphi` green for the static side, gray dashed for unstable branches,
  orange for critical points and jumps; `spring`, `arr`, ...). Same line widths, sans-serif labels at
  `\small`, symbols as in the text. A style needed in several chapters is added to `preamble/style.tex`
  (and noted under "Cross-chapter decisions"), not redefined locally.
- Sketches stay clean: few labels, generous white space, no decoration that carries no meaning. Check every
  figure in the compiled PDF (render the page and look at it) before committing.

## Notation sources (see SOURCES.md for details)
- Continuum mechanics and elasticity: the author's book, Constantinescu & Korsunsky, *Elasticity with Mathematica*
  (CUP 2007): σ = C : ε, data with superscript D (u^D, b^D, t^D on ∂Ω^u, ∂Ω^t), admissible sets 𝒦, 𝒮
  (`\Kad`, `\Sad`), potential energy 𝒰_p(u), residual stress σ_0, temperature θ, operators grad, div, curl.
- Stability and Koiter/LSK asymptotics: Triantafyllidis's MEC563 notes, with **η** in place of his λ:
  energy 𝒲(u, η) with load parameter η, principal branch ⁰u(η), critical point (u_c, η_c), mode ¹u,
  amplitude ξ, derivatives 𝒲,uu, 𝒲,uuu.
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
      figures/                   PDF figures of the notes (also used by the slides);
                                 figures/tikz/ the TikZ sketches (one .tex per sketch)
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
| 3 | `ch03_continuation` | `nc` | From continuum to discrete: numerical methods | weak forms, bifurcation of a 3D elastic body, linear buckling (eigenproblem, Rayleigh quotient), Riks arc-length, detection, branch switching, FEniCS/Cast3M |
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
- Rigorous derivation of reduced models (checked 23 Nov 2026): plates — Ciarlet, A justification of the von Kármán
  equations, *ARMA* 73 (1980) 349–389; Friesecke, James & Müller, A hierarchy of plate models derived from nonlinear
  elasticity by Γ-convergence, *ARMA* 180 (2006) 183–236 (von Kármán: energy per unit volume ∼ h⁴, forces ∼ h³);
  rods — Bermúdez & Viaño (1984), Trabucho & Viaño (Handbook of Numerical Analysis IV, 1996), Cimetière et al. (1988),
  Mora & Müller (2003, 2004), all in Ch. 4; shells — Ciarlet, *Mathematical Elasticity III: Theory of Shells*
  (North-Holland, 2000); Ciarlet & Lods, Asymptotic analysis of linearly elastic shells III: justification of Koiter's
  shell equations, *ARMA* 136 (1996) 191–200.
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
- 2026-11-23 (hub, author): balance rule for Ch. 4-8 (3D link with physical assumptions and rigorous derivations,
  engineering core, boxed physical examples); Ch. 3 retitle propagated to the plan table, README and overview.
- 2026-11-23: figures: TikZ sketches in `<chNN>/figures/tikz/`, plots from scripts, one visual language
  (section "Figures and sketches").
- 2026-11-21 (Ch. 1 thread): Lyapunov stability, Jacobian eigenvalues and the Hopf bifurcation (galloping example)
  are introduced in Chapter 1; Chapter 2 reuses them (Ziegler, flutter) instead of introducing Hopf.
- 2026-11-21 (Ch. 1 thread): Chapter 1 gives the ideas of continuation on one equation (natural parameter vs
  pseudo-arclength, augmented Jacobian, zero eigenvalue Jv = 0 with fold test wᵀf_r ≠ 0, Box 1.2) and a Python
  code `ch01_bifurcation/code/python/arclength.py` for n unknowns; Chapter 3 builds on it (FE, Riks/Crisfield).
  Matrix notation for ODE systems: `\mat{y}`, `\mat{J}`, `\mat{v}`, `\mat{w}`, `\mat{u}=(\mat{y},r)`, `\widehat{\mat{J}}`.
- 2026-11-21 (Ch. 2 thread): Chapter 2 notation accepted: generalised coordinates `\mat{u}`, stiffness
  `\mat{K} = 𝒲,uu`, mass `\mat{M}`, ⁰u(η), ¹u, ξ, ²u; η = η_c + η₁ξ + ½η₂ξ² (Taylor convention of Triantafyllidis);
  κ', 𝒲₃, 𝒲₄; imperfection amplitude ξ̄; maximum load η_m; flutter load P_f. Box 2.2 (Koiter's coefficients) and
  `ch02_discrete/code/python/koiter_sympy.py` (n dof) are reused for the elastica, plates and shells.
- 2026-11-21 (Ch. 2 thread, author): the von Mises truss replaces the fishery in Chapter 1 (fold example);
  the fishery moves to `ch01_bifurcation/extra/`.
- 2026-11-21 (Ch. 3 thread, author): Chapter 3 is retitled "From continuum to discrete: numerical methods" (folder
  `ch03_continuation` and prefix `nc` unchanged): weak forms, linear buckling as an eigenproblem and as a Rayleigh-quotient
  minimisation, Riks arc-length, detection, branch switching; the Chapter 2 two-bar truss is its FEniCS/Cast3M test case.
  Hub: update the plan table, `README.md` and `ch00_intro/notes/overview.tex`.
- 2026-11-21 (Ch. 3 thread): continuum notation of Ch. 3 (from the author's MEC563 L03 slides): Green–Lagrange
  `\tens{e}(\vu) = \eps + ½\tens{q}(\vu,\vu)`, `\tens{q}(\vv,\vw)` = sym(gradᵀv grad w), variations D_u 𝒲[v], D_uu 𝒲[v,w];
  FE: residual `\mat{r} = \mat{f}_int − η\mat{p}`, `\mat{K}_0`, `\mat{K}_\sigma` (Green-strain geometric stiffness, ∫σ̂:q),
  forms a, b, Rayleigh quotient R; arc-length weight ψ. Box 3.2 (linear buckling), Box 3.3 (arc-length by bordering)
  and `ch03_continuation/code/python/truss_fe.py` (bar elements, Riks/Crisfield, negative pivots, branch switching)
  can be reused by later chapters. Large-strain theory beyond St Venant–Kirchhoff stays for Ch. 9.
- 2026-11-23 (Ch. 4 thread, author): the energy is written 𝒲 (`\mathcal{W}`) in the whole book, as in the author's
  slides. Done on 23 Nov in Ch. 2, Ch. 3 (notes and sessions), `preamble/notation.tex`, the notation list and the
  READMEs (Ch. 1 keeps plain W for the Lyapunov function).
- 2026-11-23 (Ch. 4 thread, author): a short section on the bifurcation of a 3D elastic body (principal branch,
  critical point, limit vs bifurcation, 3D linear buckling, Koiter's η₁, η₂ by variations) goes in Ch. 3; if too
  long, a chapter of its own between Ch. 3 and Ch. 4. Sources: author's C04 slides, Triantafyllidis notes AC.
- 2026-11-23 (Ch. 4 thread, author): twist and natural curvature are a remark in Ch. 4 and treated in Ch. 8.
- 2026-11-23 (Ch. 4 thread): Chapter 4 drafted. Notation: rod displacements u, w, EA, EI, r, N, M, end load P, P_c,
  effective-length factor K, wavenumber q, elastica angle θ(s), end rotation θ₀, elliptic K(k), E(k), foundation k
  (notation list updated). Reusable: `ch04_rods/code/python/elastica.py` (exact elastica, shooting, continuation with
  Ch. 1 `arclength.py`) for the plates and shells threads as a code check; TikZ sketches in `ch04_rods/figures/tikz/`.
- 2026-11-23 (Ch. 4 thread, author): Timoshenko & Gere is not available. Alfutov, *Stability of Elastic Structures*
  (Springer, 2000) and Brush & Almroth (1975) were uploaded and used; hub: add Alfutov to `SOURCES.md` (B&A §4.6 ring on a
  foundation for Ch. 7, §2.5–2.6 beam columns and failure of bars for Ch. 5).
- 2026-11-24 (Ch. 5 thread): Chapter 5 drafted. Notation (notation list updated): v, w, φ for the shear-centre
  displacements and twist, J, Γ, ω, y₀, z₀, r₀, P_v, P_w, P_φ, M_cr; inelastic E_t, E_s, E_r, P_t, P_r, Ḡ; Shanley's
  k, k_t, d, c; design λ̄, χ, α and **ζ for the Ayrton–Perry imperfection (η stays the load parameter)**, σ₀, f_y.
  SOURCES.md: Hutchinson (1974) and new §4g (Chajes & Winter, AISC 360-22, Hutchinson 2016 on spheres → Ch. 7–8).
  Reusable: `ch05_thinwalled/code/python/ft_section.py` (thin-walled section constants, shear centre, Γ, the 3×3
  buckling eigenproblem), `shanley.py`, `fibre_column.py` (column curves). Ch. 6 may cite the cruciform as its first
  plate example (k = 0.425 + (b/a)², `sec:tw-cruciform`).

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
