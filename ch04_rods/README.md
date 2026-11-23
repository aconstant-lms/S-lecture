# Chapter 4: Rods: the elastica and beyond

Label prefix `rd` (`sec:rd-*`, `eq:rd-*`, `fig:rd-*`, `exo:rd-*`, bibitem keys `rd-*`).
Status: **complete draft (23 Nov 2026)**. Lecture text, exercises with solutions, the 2 h session with answers and
instructor notes, figures and codes. The Mathematica, FEniCSx and Cast3M inputs have not been run (marked
`\untested` in the instructor manual). Slides: not started.

## Spine (author's slides C05 "Poutres", slide 11)
One column, three energies, three bifurcation diagrams (`fig:rd-models`): no rotation (bar, no bifurcation),
small rotations (Euler loads, flat branches), large rotations (elastica, rising branches). The rotations, not the
strains, decide the post-buckling. Prerequisite: Ch. 3 `sec:nc-bif` (bifurcation of an elastic body, Koiter by
variations, the elastica as worked example).

## Content
1. `sec:rd-3d` From the 3D body to the rod. Fibre strain e = u' + ½(u'² + w'²) → u' + ½w'² (slide 8); Euler–Bernoulli
   kinematics e = u' + ½w'² − zw'' (slide 9, `fig:rd-fibre` TikZ); energy 𝒲 = ½∫EA(u'+½w'²)² + ½∫EIw''² + P u(L)
   (slide 16); N' = 0, (EIw'')'' − Nw'' = 0 (slide 12). Gbox `sec:rd-scales` (table of the three energies). Why it works:
   EA ∝ h², EI ∝ h⁴; Ciarlet's asymptotic method (Bermúdez–Viaño 1984, Trabucho–Viaño 1996, Cimetière et al. 1988);
   Γ-convergence (Mora–Müller 2003: energy/volume ~ h², inextensible bending–torsion rod; 2004: lower energy, von Kármán
   rod); Audoly–Pomeau §3.3. Cited, not proved.
2. `sec:rd-euler` Small rotations. Second variation on the principal branch, adjacent equilibrium (B&A §1.3), four
   supports (`fig:rd-supports` TikZ, B&A Table 2.1): K = 1, 0.699, 0.5, 2; effective length (Hibbeler §13.3, K = 0.7);
   Euler hyperbola; gbox `sec:rd-slender` (KL/r > π√(E/σ_Y) = 88.9). Example `ex:rd-tube` (CHS 114.3 × 6, 4 m, SI):
   370 kN pinned, 370 MPa > yield clamped–pinned, 93 kN flagpole. Why the branch is flat (N = −P, linear equation).
   Imperfect column (B&A §1.4, Triantafyllidis H4): a_n = ā_n P/(P_n − P); Southwell plot; secant formula
   (Hibbeler Eq. 13-19): first yield at 232 kN = 0.63 P_c for e = 10 mm. `fig:rd-imperfect`.
3. `sec:rd-elastica` Large rotations. 𝒲(θ,P), EIθ'' + P sinθ = 0, Kirchhoff's kinetic analogy (`fig:rd-pendulum` TikZ,
   A&P §3.8); exact P/P_c = (2K(k)/π)², w/L = k/K, Δ/L = 2 − 2E/K (Triantafyllidis BA-1); `tab:rd-elastica`,
   `fig:rd-elastica`; ends touch at 130.71°, 2.1834 P_c. Gbox `sec:rd-reserve`: 1 % above P_c at θ₀ = 16°, w = 0.089 L.
   A rod standing up (A&P App. A).
4. `sec:rd-foundation` Foundation (B&A §2.2d, Alfutov §3.3). P(q) = EIq² + k/q², q_c = (k/EI)^{1/4}, P_c = 2√(kEI); gbox
   `sec:rd-wavelength`; festoon and mode jumps at L q_c/π = √(n(n+1)) (`fig:rd-foundation`, `fig:rd-foundation-sketch`);
   Alfutov's two cautions (search all n; √(kEI) if one end may sway); rails, pipelines, wrinkling (Cerda–Mahadevan 2003).
   Post-buckling with the elastica: P/P_c = (8 + A²)/(8 + 3A²) ≈ 1 − A²/4 against (8 + 4A²)/(8 + 3A²) ≈ 1 + A²/8 free.
   Gbox `sec:rd-foundation-unstable`; localisation (Hunt, Wadee & Shiacolas 1993).
5. `sec:rd-twist` A remark: Kirchhoff rod in 3D, spinning top, Greenhill, localised helix; full treatment in Ch. 8.

Exercises: 8 short questions (effective length, flat branch, Southwell, pendulum, ten per cent more, rails, bend or
stretch, yield or buckle); 5 problems (the kinematics decide the post-buckling = H3 Problem 1, the wavy column = H4,
a rod standing up = A&P App. A, finite beam on a foundation, secant design); 3 computer exercises (shooting and
continuation, foundation, FEniCS and Cast3M).

## Checked numbers (all from the Python codes)
- Elastica: shooting = exact to all digits; continuation (Ch. 1 `arclength.py`) 161 points to 141°, error 2e-11.
- H3 kinematics (inextensible limit, shooting): small rotations 0, "improved" strain e = u' + ½(u'² + w'²): −3/8 (unstable),
  exact: +1/8.
- Foundation coefficient −1/4: two-harmonic Ritz on the quartic energy, confirmed with four extra harmonics and the full
  energy (A = 0.02 gives 0.2500). Springs act per unit base length (dx = cos θ ds); with ds instead one gets −1/8:
  a wrong model, noted here because it is an easy mistake.

## Files
- `notes/ch04_rods.tex`. Figures: `figures/rd_models.pdf`, `rd_elastica.pdf`, `rd_foundation.pdf`, `rd_imperfect.pdf` from
  `code/figures/fig_ch4.py`; TikZ sketches `figures/tikz/rd_fibre.tex`, `rd_supports.tex`, `rd_pendulum.tex`,
  `rd_foundation_sketch.tex`.
- `code/python/elastica.py` (exact, shooting, continuation), `ex_columns.py` (supports, imperfection, Southwell, secant,
  SI tube), `ex_foundation.py` (festoon, Ritz post-buckling, rail), `ex_kinematics.py` (H3, three strain measures).
- `code/mathematica/elastica.wl` (elliptic solution, series, shapes, Koiter by integrals). **Not run.**
- `code/fenics/elastica_rod_fenicsx.py` (1D rod in θ, clamped–sliding, load control from the mode) and
  `elastica_strip_fenicsx.py` (plane-strain SVK strip 1 × 0.01, clamped, shortened, reaction vs elastica after removing
  the axial shortening). dolfinx 0.9 API. **Not run.**
- `code/cast3m/elastica_poutre.dgibi` (standing rod, `poutre`, `flambage`, `pasapas` large rotations) and
  `elastica_strip.dgibi` (`qua8` plane strain, imposed shortening). **Not run.**
- `exercises/ch04_session.tex`: (a) Euler's columns by hand, (b) shooting and continuation with Algorithm 4.1,
  (c) FEniCS / Cast3M. Listed in `preamble/manual_chapters.tex`.

## Decisions and open questions
- Balance (hub, 23 Nov 2026): from 3D ≈20 %, engineering ≈70 %, physical ≈10 % but scattered. Candidate: gather the rod standing up, the pendulum analogy and the localised helix into one boxed example; move the skin-on-soft-core / thin-film remark to Ch. 6 and keep a forward reference. See "Balance check" in CLAUDE.md.
1. (author, 23 Nov 2026) The 3D bifurcation section is in Ch. 3 (`sec:nc-bif`, about 3 pages). Done.
2. (author, 23 Nov 2026) Energy 𝒲 in the whole book. Done in Ch. 2–4.
3. (author, 23 Nov 2026) Twist and natural curvature: a remark here (`sec:rd-twist`), full treatment in Ch. 8.
4. (author, 23 Nov 2026) FEniCS and Cast3M: 1D rod and 2D strip, both against the elastica. Written, not run.
5. (author, 23 Nov 2026) Timoshenko & Gere is not available: the foundation follows Alfutov §3.3 and Brush & Almroth
   §2.2d; Brush & Almroth §1.3–1.4 and §2.2 for the engineering view of columns. Notation kept as in the book (EI, k, w),
   which is also Brush & Almroth's; Alfutov writes EJ, κ, v.
6. Open (notation): `k` is both the elliptic modulus sin(θ₀/2) (§4.3, as in Triantafyllidis and A&P) and the foundation
   stiffness (§4.4, as in B&A); `K` is both the effective-length factor and the elliptic integral K(k). Both pairs are
   standard in their fields and live in different sections; rename one (e.g. foundation `k_f`) if the author prefers.
7. Open: H3 Problem 2 (bimetallic Al/Cu beam, thermal buckling, LSK with u₂) is not used yet; candidate for Ch. 5
   (real materials) or a second problem here.
8. Open: the stability of the higher elastica branches is stated, not shown (Maddocks 1984 would be the reference).
9. Slides use λ for the load; the book keeps η, and P for a physical end load (as in Ch. 3).

## Sources
- Author's slides C04 "Rappel, rôle des rotations, bifurcation en déformation finie" (29 Jan 2026) and C05 "Poutres"
  (29 Jan 2026, handwritten: fibre strain 8, kinematics 9, three models 11, equilibrium 12, second variation 16, adjacent
  equilibrium 17, four supports 19, imperfection 20–21).
- Triantafyllidis MEC563 notes (2011): BA-1 elastica pp. 85–89; AC (LSK continuum) pp. 46–82 for Ch. 3. MEC553 (2018):
  L3 slides 7–30, L4 slides 26–38; homeworks H3 (Problem 1 used, Problem 2 open) and H4 (used).
- Audoly & Pomeau (2010), PDF = book + 11: App. A pp. 546–557 (elastica, Riemann sum, standing rod, cusp); §3.3 p. 63
  (bending energy from 3D); §3.6–3.9 pp. 82–102 (Kirchhoff equations, spinning top, localised helix); §8.5, §8.7 for Ch. 6.
- Hibbeler, *Mechanics of Materials*, 9th ed. (2014), Ch. 13, PDF = book + 25: Eqs. 13-5, 13-6 (Euler), 13-10 to 13-12 and
  Fig. 13-10 (effective length), 13-19 (secant formula); §13.5–13.7 for Ch. 5.
- Brush & Almroth (1975), PDF = book + 13: §1.3 adjacent equilibrium p. 11, §1.4 slightly crooked column p. 13, §2.2
  flexural instability and Table 2.1, §2.2d column on an elastic foundation pp. 35–36, §2.5 beam columns, §2.6 failure of
  slender bars (tangent modulus, CRC guide) for Ch. 5; §4.6 ring on an elastic foundation for Ch. 7.
- Alfutov, *Stability of Elastic Structures* (Springer, 2000), PDF = book + 10: §3.3 columns on elastic foundations and
  elastic supports, pp. 103–107 (Eq. 3.33, Fig. 3.13, the √(κEJ) limit with a free end).
- Checked references: Bermúdez & Viaño (1984), Trabucho & Viaño (Handbook IV, 487–974; zbMATH lists 1995, the volume is
  dated 1996), Cimetière et al. (1988), Mora & Müller (2003, 2004), Cerda & Mahadevan (2003), Hunt, Wadee & Shiacolas (1993).
