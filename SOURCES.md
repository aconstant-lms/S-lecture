# Sources: what to take from each, and where it goes

The files themselves are **not** in this repository (it is public, and most are copyrighted).
The author uploads them again in a chapter thread when they are needed. Page numbers below are
PDF pages of the files the author provided (book page in brackets when different).

Editorial line (author, 21 Nov 2026): **structural engineering first, with some physical examples.**
The spine is Thompson & Hunt, Bažant & Cedolin, Brush & Almroth, Koiter, Guckenheimer & Holmes;
design practice comes from Bushnell and the NASA monographs; Audoly & Pomeau, Reis, Bertoldi, Hutchinson
supply physical examples and illustrations.

## 1. Constantinescu & Korsunsky, *Elasticity with Mathematica* (CUP, 2007), 267 p.
**Role: reference for continuum mechanics and the elasticity notation** (Chapters 3, 6, 9, appendices).
- Contents: Ch. 1 kinematics (deformation gradient F, polar decomposition F = RU = VR, C and B tensors,
  Green–Lagrange strain, small strain, compatibility); Ch. 2 stresses (virtual power, Cauchy stress);
  Ch. 3 linear elasticity (Hooke tensor, Voigt and second-rank notations, symmetries); Ch. 4 general
  principles (displacement and stress formulations, uniqueness, energy potentials, reciprocity, Saint-Venant);
  Ch. 5 Airy functions; Ch. 6 displacement potentials; Ch. 7 energy principles, extremum theorems,
  **Rayleigh–Ritz method (§7.4, p. 209 [197])** and **extremal properties of free vibrations (§7.5, [204])**;
  App. 1 differential operators in curvilinear coordinates; App. 2 the Mathematica package.
- Notation seen in the book: σ = C : ε (§3.1, p. 69 [57]), C the fourth-order Hooke tensor in bold italic
  (**this book writes ℂ, blackboard**),
  S the compliance; data with superscript D: u^D, b^D (body force), t^D (traction) on ∂Ω^u, ∂Ω^t;
  admissible sets 𝒦(u^D, ∂Ω^u), 𝒮(b^D, t^D, ∂Ω^t); potential energy 𝒰_p(u), complementary energy 𝒰*_p(s)
  (§7.1, p. 203 [191]); initial (residual) stress σ_0, temperature change θ, thermal tensor A;
  operators grad, div, curl; λ, μ Lamé coefficients.
- Use: notation of the continuum chapters; Rayleigh–Ritz for plates and shells (Ch. 6–8); its Mathematica
  tools for symbolic exercises (Ch. 2, 4, 6).

## 2. N. Triantafyllidis, *Stability of Solids: from Structures to Materials*, lecture notes MEC563,
École polytechnique, March 2011, 105 p.; slides MEC553 (2018, 9 lectures), 8 homeworks + sample exam.
**Role: inspiration and examples** (the course taught before at the École), mainly Chapters 2, 3, 4, 6, 9.
- Notes: A — stability and bifurcation: definitions, linearisation, Lyapunov's direct method,
  finite-dof examples, energy criterion (pp. 8–21); finite-dof bifurcation models: **perfect and imperfect
  rigid T model (24–31), perfect and imperfect square plate model (32–40), two-bar planar truss (41–45)**;
  **Lyapunov–Schmidt–Koiter (LSK) asymptotics** for elastic continua: functionals and derivatives,
  limit vs bifurcation points, simple mode perfect/imperfect, simultaneous multiple modes (46–82).
  B — applications: **elastica (85–89)**, **rectangular plate (91–103)**. References (104–105).
- Notation of the notes (LSK): energy ℰ(u, λ), λ load parameter (**this book writes η**), principal branch ⁰u(λ), critical point
  (u_c, λ_c), buckling mode ¹u, amplitude ξ, derivatives ℰ,uu (stability operator), ℰ,uuu, ...,
  post-bifurcation coefficients λ₁, λ₂.
- Slides (2018): L1 why stability (failures, applications); L2 bifurcation with finite dof; L3–L4 LSK
  asymptotics (simple mode, imperfections); L5 von Kármán plate, simple and double mode; L6 FEM for stability
  + fiber-reinforced composites (micro/macro instability); L7 cellular solids, Bloch-wave analysis of the
  unit cell; L8 phase transformations in shape memory alloys (lattice instabilities); L9 review.
- Homeworks (2018), candidate exercises: H1 finite-dof mechanisms (Ch. 2); H2 two nonlinear springs in
  series (Ch. 1–2); H3 simply supported beam, axial load (Ch. 4); H4 same with a wavy imperfection (Ch. 4);
  H5 clamped circular von Kármán plate under radial compression (Ch. 6); H6 layered composite, long
  wavelength bifurcation (Ch. 9); H7 thin ring on an elastic foundation with thermal load (Ch. 7);
  H8 atomic chain, discrete vs continuum (Ch. 9, optional); sample exam: four masses linked by rods and
  springs (Ch. 2).

## 2b. J. M. T. Thompson & G. W. Hunt, *A General Theory of Elastic Stability* (Wiley, 1973), 322 p. (PDF 344 p.)
**Role: spine of Chapter 2** (book page = PDF page − 18 in Ch. 1, − 17 in Ch. 10).
- §1.2 simple link models, book pp. 3–21: simple arch (snap-through), hinged cantilever (stable symmetric),
  propped cantilever (unstable symmetric), asymmetric model (spring at 45°), two-hinged strut.
- §2.5 initial imperfections (book p. 65): limit point, asymmetric, stable- and unstable-symmetric points.
- §10.4 erosion of an optimum design, book pp. 243–249 (PDF 260–266): the **Augusti model** (energy, paths,
  secondary bifurcation P^C = (3c₁ + c₂)/4L, coincident case, imperfection sensitivity).

## 3. D. Bushnell, Buckling of shells — pitfall for designers, *AIAA Journal* 19 (1981) 1183–1226,
and the slide version (88 slides, "6-1" to "6-88").
**Role: design principles and the "rogue's gallery" of failures** (Chapters 0, 5, 7, 8).
- Paper sections (PDF page = journal page − 1182): 1 introduction and catastrophic failures (p. 1);
  2 buckling basics (p. 5); 3 classical buckling of cylinders and spheres, imperfection sensitivity (p. 7; qualitative guidelines p. 14); 4 nonlinear collapse
  and when linear bifurcation is appropriate (p. 15); 5 bifurcation from a nonlinear prebuckling state (p. 19);
  6 boundary conditions, transverse shear, stable post-buckling (p. 24); 7 optimum design and modal interaction
  (p. 29); 8 effect of imperfections on stiffened shells and a design method (p. 34); 9 examples needing sophisticated analysis (p. 37); 10 summary (p. 40).
- Slides: collapsed tanks (Belgian conical water tank, wine tanks after earthquakes, San Fernando 1971, LNG tank),
  then the same roadmap; closing "main points": imperfections and boundary conditions often have a huge
  influence; when a linear bifurcation model is (not) enough.
- Use: motivation in the course overview and Ch. 7–8; the design checklist of Ch. 7; local vs general
  instability and modal interaction in Ch. 5 and 8.

## 4. NASA SP-8007, *Buckling of Thin-Walled Circular Cylinders* (public documents)
- **1968 revision** (Weingarten, Seide, Peterson; Sept. 1965, revised Aug. 1968), 56 p., scanned: the classical
  empirical knockdown factors for isotropic and orthotropic cylinders under axial compression, bending, external
  pressure, torsion and combined loads (contents on p. 3).
- **2020 revision**, NASA/SP-8007-2020/REV 2 (M. W. Hilburger, NASA Langley, Dec. 2020), 109 p.: history and
  state of the art (imperfections, prebuckling, boundary conditions, composites, cutouts, joints), and three
  design approaches — empirical (the 1968 knockdown factor γ, formula on p. 41 and 54), semi-empirical,
  analysis-based (Shell Buckling Knockdown Factor assessment, SBKF).
- Use: Ch. 7 (knockdown factors, from the lower bound of tests to analysis-based design), Ch. 8 (pressure),
  exercises comparing a Cast3M/FEniCS computation with the knockdown curves. Public: they may be cited with
  their NTRS numbers; the PDFs are still kept out of the repository (size).

## 4b. A. Constantinescu, *Large strains and stability analysis*, MEC563 lecture slides (L03), 43 p.
**Role: the author's own notation for large strains in the stability chapters** (Chapters 3 and 9).
- Kinematics (F, polar decomposition, C, B); Green–Lagrange strain e(u) = ε(u) + ½q(u,u), q and r the symmetric and
  antisymmetric parts of ∇ᵀv·∇w; St Venant–Kirchhoff energy; weak problem and Newton–Raphson; geometric stiffness
  {v}ᵀ[K_G]{w} = ∫q(v,w):σ⁰; critical points (limit vs bifurcation from W,uλ); 3D linear buckling
  ∫ε(v):C:ε(w) + λ∫q(v,w):σ⁰ = 0; inverted pendulum, rails, Venus flytrap, Love–Kirchhoff rods.
- Use: Ch. 3 §3.1 (weak form, second variation); Ch. 9 (large strains, 3D bodies).

## 4c. B. Audoly & Y. Pomeau, *Elasticity and Geometry: From Hair Curls to the Non-linear Response of Shells*
(Oxford University Press, 2010), 597 p. **Role: physical examples and pictures** (PDF page = book page + 11).
- Ch. 2 3D elasticity; §2.5 stress and strain for finite displacements, second Piola–Kirchhoff stress (book p. 47).
- Ch. 3 Kirchhoff rods (Darboux vector, twist, Kirchhoff equations, spinning-top analogy, localized helix, p. 59);
  Ch. 4 mechanics of the human hair (p. 105); Ch. 5 rippled leaves, uncoiled springs (p. 132). → Ch. 4.
- Ch. 6 plates, Theorema egregium, developable surfaces, Föppl–von Kármán (p. 157); Ch. 7 end effects in plate
  buckling (p. 214); Ch. 8 finite-amplitude buckling of a strip, Euler column, secondary buckling, delamination
  (p. 251); Ch. 9 crumpled paper, d-cones and ridges (p. 325); Ch. 10 fractal buckling near edges (p. 369). → Ch. 6.
- Ch. 11 geometric rigidity of surfaces (p. 403); Ch. 12 shells of revolution (p. 435); Ch. 13 the elastic torus
  (p. 454); Ch. 14 spherical shell pushed by a wall (p. 490). → Ch. 7, 8.
- Used in Ch. 3: §2.5 (finite rotations, choice of stress measure).

## 4d. H. Kielhöfer, *Bifurcation Theory: An Introduction with Applications to PDEs* (Springer, Applied
Mathematical Sciences 156, 2004), 355 p. **Role: precise statements behind the "Why it works" paragraphs**
(author: very nice but too mathematical, few illustrations; cite, do not follow). PDF page = book page + 9.
- Ch. I local theory: implicit function theorem (I.1), Lyapunov–Schmidt (I.2), for potential operators (I.3),
  turning points (I.4), bifurcation from a simple eigenvalue, Crandall–Rabinowitz (I.5, Theorem I.5.1, p. 15),
  bifurcation formulas λ̇(0), λ̈(0) = Koiter's η₁, η₂ (I.6, p. 18), exchange of stability (I.7, p. 20),
  Hopf (I.8–I.9, p. 30), degenerate bifurcation and Newton polygon (I.15–I.16), high-dimensional kernels,
  variational methods (I.19–I.21).
- Ch. II global theory: degree, odd crossing numbers (II.4, p. 186), Rabinowitz global bifurcation (II.5),
  change of Morse index for potential operators (II.7, Theorem II.7.3, p. 214).
- Ch. III elliptic PDEs, free nonlinear vibrations, global branches.
- Use: Ch. 1 (IFT, Hopf, exchange of stability), Ch. 2 (Lyapunov–Schmidt for potentials, bifurcation formulas),
  Ch. 3 (Crandall–Rabinowitz for branch switching, Morse index for the pivot count), Ch. 4 and 6 (Euler column,
  plates as elliptic problems).

## 5. Map: sources by chapter
| Ch | Main sources |
|---|---|
| 0 | Bushnell (failures), Triantafyllidis L1 (why stability) |
| 1 | Strang, Strogatz, Guckenheimer & Holmes, Thompson & Hunt |
| 2 | Thompson & Hunt (§1.2, §10.4), Koiter, Triantafyllidis notes A (T model pp. 24–31, two-bar truss pp. 41–45, LSK pp. 57–71), sample exam Problem 1; Ziegler (1968) |
| 3 | Triantafyllidis L6 (FEM, slides 3–9), Riks, Crisfield, Keller; Constantinescu & Korsunsky Ch. 7 (§7.2, §7.4, §7.5); author's L03 slides; Bushnell §4; Kelly (2003), Bažant (2003) |
| 4 | Triantafyllidis BA-1 (elastica), H3, H4; Timoshenko & Gere; Audoly & Pomeau Ch. 3–5 (rods, hair, ribbons) |
| 5 | Bažant & Cedolin, Trahair, Shanley, Hutchinson (plastic buckling), Bushnell §7 |
| 6 | Triantafyllidis BB-1 and L5 (von Kármán plate, double mode), H5; Brush & Almroth; Constantinescu & Korsunsky Ch. 7 |
| 7 | Brush & Almroth, Koiter, NASA SP-8007 (1968, 2020), Bushnell §3–8, H7 |
| 8 | Bushnell (pressure, tanks), NASA SP-8007 2020, Hutchinson (spheres), Reis, Bertoldi |
| 9 | Constantinescu & Korsunsky Ch. 1–4, Triantafyllidis L6–L7 (composites, Bloch waves), H6, H8 |
