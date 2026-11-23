# Chapter 4: Rods: the elastica and beyond

Label prefix `rd` (`sec:rd-*`, `eq:rd-*`, `fig:rd-*`, `exo:rd-*`, bibitem keys `rd-*`).
Status: **outline agreed (23 Nov 2026)**, decisions below. No text yet. Next: the 3D bifurcation section (Ch. 3),
then §4.1–4.2.

## Spine of the chapter (from the author's slides C05 "Poutres", slide 11)
One column, three energies, three bifurcation diagrams. The rotations, not the strains, decide the post-buckling:

| rotations | energy per unit length | diagram |
|---|---|---|
| none (bar) | ½ EA u'² | one straight branch, no bifurcation |
| small (von Kármán rod) | ½ EA (u' + ½w'²)² + ½ EI w''² | Euler loads, flat secondary branches (amplitude undetermined) |
| large (elastica) | ½ EI θ'² (inextensible) | rising branches, stable post-buckling |

The chapter derives the three energies from the 3D energy of Chapter 3 (Ciarlet's asymptotic justification),
then treats each one: Euler loads and design (small rotations), the elastica in closed form (large rotations),
and the foundation, which picks a wavelength and turns the post-buckling unstable.

Notation (author, 23 Nov 2026): the energy is written **𝒲** (`\mathcal{W}`), as in the author's slides, not ℰ.
Load parameter η (book convention), the 2D fibre displacements u, w, the rotation θ (= −β of the slides).

## Prerequisite: bifurcation of a 3D elastic body (before this chapter)
The author asks for a short 3D derivation of bifurcation theory *before* Chapter 4 (slides C04, pp. 9 and 21–28;
Triantafyllidis notes A, LSK pp. 46–82, and MEC553 L3–L4). Chapter 3 §3.1 already has e = ε + ½q, D_u𝒲, D_uu𝒲 and
the stability gbox, and §3.3 has (K₀ + ηK_σ)¹u = 0. What is still missing is short:
1. principal branch ⁰u(η) from D_u𝒲 = 0, its tangent d⁰u/dη = −[𝒲,uu]⁻¹𝒲,uη (C04 eq. 25);
2. critical point: D_uu𝒲[¹u, v] = 0 for all v; limit point if 𝒲,uη[¹u] ≠ 0, bifurcation point otherwise (C04 eq. 26);
3. 3D linear buckling ∫ε(v):ℂ:ε(w) + η∫q(v,w):σ₀ = 0 (C04 eq. 28) and its FE form (eq. 29);
4. Koiter's η₁, η₂ written with variations (Box 2.2 with sums replaced by D³𝒲, D⁴𝒲), so Chapter 4 can apply them
   to the column and the elastica.
Proposal: a new section in Chapter 3 between `sec:nc-weak` and `sec:nc-fe`, ~2 pages. Owned by the Ch. 3 thread / hub
(see open question 1). Chapter 4 then starts from it.

## Outline
**Outline frame.** Objectives: derive a rod energy from 3D and say when it is right; compute Euler loads for the four
classical supports and use effective lengths; solve the elastica with elliptic integrals and check Koiter's η₂;
explain wavelength selection on a foundation; validate a Python shooting code and an FE code against the closed form.

**4.1 From the three-dimensional body to the rod** (`sec:rd-3d`)
- The fibre (slide 8): ds² = 1 + 2u' + u'² + w'², e = u' + ½(u'² + w'²); rotation β "small but not negligible" → e = u' + ½w'².
- Love–Kirchhoff / Euler–Bernoulli kinematics (slide 9): ū = u + zβ, β = −w', e = u' + ½w'² − zw''.
- Energy (slide 16): 𝒲(u, w; η) = ½∫EA(u' + ½w'²)² + ½∫EI w''² − η ℓ. Equilibrium N' = 0, M'' − Nw'' = 0 (slide 12).
- gbox "The energy scale chooses the rod model". Why it works: Ciarlet's method. Scale the cross-section by h,
  expand in h: linear rods (Bermúdez & Viaño 1984; Trabucho & Viaño 1996, Handbook of Numerical Analysis IV);
  nonlinear rods (Cimetière, Geymonat, Le Dret, Raoult & Tutek 1988); Γ-convergence: energy ~h⁴ gives the
  inextensible bending–torsion rod, the elastica (Mora & Müller 2003); lower energy gives the von Kármán-like rod
  (Mora & Müller 2004). Ciarlet, *Mathematical Elasticity* I (1988) for the method (plates: Ciarlet & Destuynder 1979).
  Stated, cited, not proved (Kielhöfer style: cite, don't follow).

**4.2 Small rotations: Euler loads and design** (`sec:rd-euler`)
- Second variation (slide 16) on the principal branch ⁰u = −(P/EA)x, ⁰w = 0: EI w'''' + P w'' = 0 (slide 17,
  adjacent equilibrium), q² = P/EI, w = C₁ sin qx + C₂ cos qx + C₃x + C₄.
- Four supports (slide 19): pinned–pinned π²EI/L², pinned–clamped 2.046π²EI/L², clamped–clamped 4π²EI/L²,
  clamped–free π²EI/4L². Effective length K L and the Euler hyperbola σ_c = π²E/(KL/r)² (Hibbeler §13.2–13.3).
- Why the branches are flat (slide 11, middle): under a dead load N = −P along the branch, 𝒲 is quadratic in w.
- The imperfect column (slides 20–21): w = w̄/(P_c/P − 1); the secant formula as its design form (Hibbeler §13.4);
  Southwell plot (links to the Ch. 2 power laws: here no maximum load, a stable-symmetric point).
- Design box: slenderness, (KL/r)_c, where Euler stops and Chapter 5 (tangent modulus, column curves) starts.

**4.3 Large rotations: the Euler elastica** (`sec:rd-elastica`)
- 𝒲 = ½∫EI θ'² ds − P∫(1 − cos θ) ds; EI θ'' + P sin θ = 0: Kirchhoff's kinetic analogy with the pendulum
  (Audoly & Pomeau Ch. 3; Triantafyllidis BA-1 pp. 85–89; Timoshenko & Gere §2.7).
- Closed form: k = sin(θ₀/2), P/P_c = (2K(k)/π)², x(s), w(s) with Jacobi functions; midspan deflection and end
  shortening. Table: θ₀ = 30°, 60°, 90°, ≈130.7° (ends touch), 180°.
- Koiter with Box 2.2: η₁ = 0, P/P_c = 1 + θ₀²/8 + … (checked 23 Nov with a two-term Ritz: P/P_c = (8 + 4A²)/(8 + 3A²)).
  gbox "The elastica is stable-symmetric: the column carries more load after buckling, but very little".
  Engineering reading: 1 % more load at θ₀ ≈ 16°; post-buckling strength of columns is negligible, unlike plates (Ch. 6).
- Higher modes are unstable (sketch); clamped–free elastica (Euler 1744) as an exercise.
- Mathematica: elliptic functions, series of K(k), the five shapes. Physical example: a ruler, a strip, hair (A&P Ch. 4).

**4.4 Beams on an elastic foundation: wavelength selection** (`sec:rd-foundation`)
- EI w'''' + P w'' + k w = 0. P(q) = EI q² + k/q², minimum at q_c = (k/EI)^{1/4}, P_c = 2√(kEI): the wavelength
  2π(EI/k)^{1/4} is set by the material, not by the length. Finite length: mode number n jumps, festoon of P_n(L)
  curves (Timoshenko & Gere §2.10).
- Examples: thermal buckling of rails, upheaval of buried pipelines, a stiff film on a soft substrate (forward to Ch. 6, 9).
- Post-buckling with the elastica on a linear foundation: P/P_c ≈ 1 − A²/8, **unstable** (checked 23 Nov with a
  two-harmonic Ritz; to be confirmed with Box 2.2 and Hunt et al.). gbox "A foundation selects the wavelength and makes
  the post-buckling unstable". Localisation and amplitude modulation, cited only (Potier-Ferry 1983; Hunt, Bolt &
  Thompson 1989; Tvergaard & Needleman 1980).

**4.5 Twist and natural curvature** (`sec:rd-twist`), short or moved (open question 3)
- Kirchhoff rod in 3D: frame, curvatures and twist, ½EI(κ₁² + κ₂²) + ½GJτ²; Greenhill's twisted shaft;
  the localised helix (A&P Ch. 3); naturally curved rods → tape springs (Ch. 8).

**Summary** (gbox*): rotations decide post-buckling; Euler loads and effective length; elastica stable but weak;
foundation picks the wavelength and is unstable; a code is trusted after the elastica.

## Exercises
- Short questions: effective lengths of a frame member; why the von Kármán branch is flat; Southwell from three
  readings; the pendulum analogy; θ₀ for 10 % above P_c; rail wavelength with real numbers; why a thin rod bends rather
  than stretches (h² vs h⁴); which column fails by yielding (Hibbeler, SI units).
- Problems: simply supported beam under axial load, Koiter (Triantafyllidis H3); same with a wavy imperfection (H4);
  the clamped–free elastica; finite beam on a foundation and mode switching; design of a steel and an aluminium
  column with the secant formula (Hibbeler §13.4, Examples converted to SI).
- Computer: elastica by shooting in Python (`solve_ivp` + root finding, then continuation with
  `ch01_bifurcation/code/python/arclength.py`); Mathematica elliptic solution and series; FEniCS and Cast3M
  (geometrically nonlinear beam, imperfection in the first mode, as in Ch. 3 §3.7) against the closed form;
  discrete elastic rods (Bergou et al. 2008), optional.
- 2 h session: (a) Euler loads and Koiter by hand; (b) shooting and continuation in Python; (c) FEniCS / Cast3M
  comparison on P/P_c(θ₀).

## Decisions and open questions
1. (author, 23 Nov 2026) The 3D bifurcation section goes in Chapter 3; if it grows too long, it becomes a chapter
   of its own between the present Chapters 3 and 4.
2. (author, 23 Nov 2026) The energy is 𝒲 (`\mathcal{W}`) in the whole book. Switched from ℰ on 23 Nov in Ch. 2–3,
   the sessions, `preamble/notation.tex` and the notation list. Ch. 1 keeps plain W (Lyapunov).
3. (author, 23 Nov 2026) Twist and natural curvature: a remark at the end of this chapter; the full treatment
   in Chapter 8 (tape springs). §4.5 becomes a short remark.
4. (author, 23 Nov 2026) FEniCS and Cast3M: both a 1D rod model (geometrically exact beam; Cast3M POUT with
   `pasapas` 'GRANDS_DEPLACEMENTS') and a thin 2D strip (plane strain), each against the elastica. The 2D strip
   also illustrates §4.1: the rod is the thin limit of the 2D body.
5. The slides use λ for the load; the book keeps η (decision of 21 Nov).
6. Figures (CLAUDE.md, 23 Nov): TikZ sketches in `figures/tikz/` for the fibre kinematics, the four supports, the
   elastica shapes, the beam on a foundation; plots from `code/figures/` for the three diagrams of slide 11,
   P/P_c(θ₀) exact vs Koiter vs codes, and P(q) on a foundation.

## Sources
- Author's slides C04 "Rappel, rôle des rotations, bifurcation en déformation finie" (29 Jan 2026, 28 p.): 𝒲, D_u𝒲,
  D_uu𝒲, limit vs bifurcation (pp. 9, 21–28); inverted pendulum and mechanisms (pp. 2–10). Uploaded 23 Nov.
- Author's slides C05 "Poutres" (29 Jan 2026, 22 p., handwritten): fibre strain (8), kinematics (9), three rod models (11),
  equilibrium (12), energy and second variation (16), adjacent equilibrium (17), four supports (19), imperfection (20–21).
- Hibbeler, *Mechanics of Materials*, 9th ed. (Pearson, 2014), Ch. 13 "Buckling of Columns", book pp. 661–720
  (PDF page = book page + 25): §13.1 critical load (rigid bar + spring), §13.2 ideal pinned column and slenderness,
  §13.3 other supports and effective length, §13.4 secant formula, §13.5 inelastic buckling (Ch. 5), §13.6–13.7
  design for concentric and eccentric loading (steel, 2014-T6 aluminium, timber; Ch. 5). US units: convert to SI.
- Audoly & Pomeau (2010), uploaded 23 Nov (PDF page = book page + 11):
  App. A "Calculus of variations: a worked example", book pp. 546–557: the elastica clamped at the base with a weight
  on top. A.2 energy as a Riemann sum (the discrete rod of the computer exercise), A.3 Euler–Lagrange and the natural
  condition θ'(L) = 0, A.4 a constraint by a Lagrange multiplier, A.5 linear stability (L_c² = π²EI/4Mg),
  A.6 exact solution, expansion ψ²(L) ≈ 32(L − L_c)/(√2π) (supercritical), pendulum analogy, and the constrained
  elastica as a cusp (links to Ch. 1). Source of §4.3 and of a problem. Ch. 3 rods: §3.3 bending energy from 3D
  (p. 63, a physical companion to Ciarlet), §3.7 inextensibility and validity of Kirchhoff (p. 90), §3.8 kinetic
  analogy (p. 92) with the planar elastica in §3.8.2, §3.9 localized helix (p. 96, the remark of §4.5).
  Ch. 8: §8.5 Euler column as an exact solution (p. 265), §8.7 its stability (p. 282), for Ch. 6.
- Triantafyllidis, MEC563 notes (2011), uploaded 23 Nov (PDF page = book page): BA-1 elastica pp. 85–89. Clamped
  ends sliding without rotation (the λ_c = EI(π/L)² of θ(0) = θ(L) = 0), 𝒲(θ, λ) = ∫[½EIθ'² − λ(1 − cos θ)],
  stability of the principal branch by Fourier series (BA-1.5–1.7), exact solution sin(θ/2) = k sn(μs),
  μL = 2K(k), λ/λ_c = 1 + ½k² + … (BA-1.13); LSK: 𝒲,uλ¹u = 0 (bifurcation), 𝒲,uuu = 0 (λ₁ = 0), λ₂ from
  AC-3.14, ξ = √2 k (BA-1.23). Section AC (continuum LSK, pp. 46–82) is the source of the 3D section in Ch. 3.
- Still to upload: Triantafyllidis MEC553 L3–L4 slides and homeworks H3, H4; Timoshenko & Gere Ch. 2.
- References to check before the chapterbib: Bermúdez & Viaño, RAIRO Anal. Numér. 18 (1984); Trabucho & Viaño (1996);
  Cimetière et al., J. Elasticity 19 (1988) 111–161; Mora & Müller, Calc. Var. PDE 18 (2003) 287–305;
  Mora & Müller, Ann. IHP Anal. Non Linéaire 21 (2004) 271–293; Ciarlet (1988); Potier-Ferry (1983);
  Hunt, Bolt & Thompson (1989).
