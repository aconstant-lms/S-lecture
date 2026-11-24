# Chapter 5: Rods II: thin-walled members and real materials

Label prefix `tw` (`sec:tw-*`, `eq:tw-*`, `fig:tw-*`, `exo:tw-*`, bibitem keys `tw-*`).
Status: **complete draft (24 Nov 2026)**. Lecture text (5 sections), summary, exercises with solutions (8 short
questions, 5 problems, 3 computer exercises), the 2 h session with answers and instructor notes, 3 TikZ sketches,
3 plots, 3 Python codes (run, numbers below), 2 Cast3M inputs (**not run**). Slides: not started.

## Thread
Chapter 4 promised columns that twist and columns that yield. The running structure is the Hartford Civic Center
roof (1978), whose top chords were four-angle cruciforms: an elastic torsional load independent of the length,
close to yield, and the classic plastic buckling paradox. The chapter ends with the column curves of the codes.

## Content
1. `sec:tw-3d` From 3D (≈15 %). GJ/EI ~ (t/b)², gbox `sec:tw-twistfirst`; tube vs slit tube 3(R/t)² = 244 (Ch. 4 tube).
   Vlasov kinematics (shear centre, warping ω, Γ); energy 𝒲₂ (5.4) from the Ch. 4 fibre strain, Wagner term r₀²φ'².
   Why it works: Freddi–Morassi–Paroni (2007) Γ-limit for sections of rectangles ε × ε²; limits (local buckling → Ch. 6,
   distortion, short members, plasticity).
2. `sec:tw-ft` Three loads (5.6), eigenproblem K − PM (5.7) = Ch. 3 linear buckling with 3 unknowns; doubly symmetric;
   monosymmetric: Chajes–Winter interaction (5.8), cited with AISC 360-22 §E4. Example `ex:tw-struts`: angle 100×100×6
   (FT 348 kN at 1 m vs Euler 946, twist alone 361), channel 200×75×8 (FT 1190 kN at 2 m, minor-axis 791 governs; at
   1 m FT 3143 governs). Lateral–torsional M_cr (5.9), HEB 300: 1940 kN m at 4 m, 698 at 8 m. Dee Bridge, Marcy.
   Physical box `sec:tw-ruler`: ruler on edge, P = 4.013√(EI_z GJ)/L², steel 29 N, acrylic 0.44 N. `fig:tw-sections`.
3. `sec:tw-cruciform` J = 4bt³/3, r₀² = b²/3, gbox `sec:tw-cross` σ_T = G(t/b)²; why: GJφ'² and Pr₀²φ'² have the same
   derivative. Plate check k = 6(1−ν)/π² = 0.426, warping adds (b/L)². Crossover L = 2.07 b²/t; legs 120×8: 360 MPa =
   yield of S355, 3.7 m. Boxes: Hartford (`sec:tw-hartford`), card cruciform (`sec:tw-card`). Sketch `fig:tw-cruciform-sketch`.
4. `sec:tw-shanley` (written 23 Nov) tangent/reduced modulus, Hibbeler Ex. 13.5, Shanley's model in closed form,
   sketch `fig:tw-shanley-model` (added), Hutchinson's 4/3 power, plastic buckling paradox.
5. `sec:tw-curves` Residual stresses (Lehigh pattern, `fig:tw-residual`, Huber & Beedle 1954); stub column first yield
   0.7 A f_y; elastic core, gbox `sec:tw-weakaxis`; CRC parabola 1 − λ̄²/4 (Hibbeler 13-21 to 13-23); Ayrton–Perry
   derived from the Ch. 4 amplification → χ formula (5.21); European α = 0.13…0.76, χ(1) = 0.60 (b), 0.54 (c);
   fibre column `fig:tw-curves`; gbox `sec:tw-curvebox`; aluminium, timber, eccentric loads (Hibbeler 13.6–13.7);
   box Quebec Bridge (`sec:tw-quebec`).

Balance (rough, lines of the body): from 3D ≈13 %, engineering ≈70 %, physical boxes ≈12 % (ruler, card cruciform)
plus the two failure boxes.

## Checked numbers (all from the Python codes)
- `ft_section.py`: I-section Γ = t_f b³h²/24, channel shear centre 3b²/(h+6b) and Γ, angle (shear centre at the corner,
  Γ = 0), cruciform (J, r₀² = b²/3): all to machine precision. Channel FT 1190.5 kN = hand quadratic 1190.47.
  **Bug fixed 24 Nov**: the inertia matrix was first built transposed, which paired the wrong bending mode with the
  twist for unsymmetric sections (a wrong 644 kN for the channel); symmetric sections were not affected.
- `shanley.py`: closed form = step-by-step solution to 1e-15.
- `fibre_column.py` (HEB 300, S235, bow L/1000, residual 0.3 f_y, Ježek's sinusoidal shape): χ at λ̄ = 0.6/1.0/1.5:
  strong 0.86/0.65/0.38, weak 0.80/0.58/0.35, weak without residual 0.90/0.67/0.38. EC3 b 0.84/0.60/0.34, c 0.79/0.54/0.32.
- Design exercise (Ch. 4 tube): λ̄ = 1.175, curve a χ = 0.546, 278 kN; AISC ASD 175 kN (FS 1.91).

## Files
- `notes/ch05_thinwalled.tex`; figures `figures/tw_shanley.pdf`, `tw_sections.pdf`, `tw_curves.pdf` from
  `code/figures/fig_ch5.py`; TikZ `figures/tikz/tw_cruciform.tex`, `tw_shanley_model.tex`, `tw_residual.tex`.
- `code/python/ft_section.py`, `shanley.py`, `fibre_column.py`.
- `code/cast3m/column_curve.dgibi` (multifibre beam, initial fibre stresses, pasapas large displacements) and
  `cruciform.dgibi` (COQ4 shells, flambage at 1, 2, 3 m; plastic case sketched in comments). **Not run.**
- `exercises/ch05_session.tex` (a: twisting columns by hand; b: Shanley and Ayrton–Perry in Python; c: column curve,
  fibre model and Cast3M). Listed in `preamble/manual_chapters.tex`.

## Decisions and open questions
- (author, 24 Nov 2026) Eurocode 3 is taken: EN 1993-1-1 §6.3 column curves (already compared in `fibre_column.py`) and lateral-torsional buckling §6.3.2 (to add: M_cr, χ_LT); keep AISC as comparison.
- (author, 24 Nov 2026) Add the buckling of a thin shell under residual internal stresses (eigenstrain, no external load: welding/forming stresses, rolled or quenched thin tube). Ch. 8 keeps prestress used on purpose. Ask the author for the papers.
- Table-top: ruler cantilever loaded on its edge (LTB), paper cruciform, curled strip (residual stress).
1. (author, 24 Nov 2026) Title "Rods II: thin-walled members and real materials"; folder and prefix unchanged.
2. Notation (author, 24 Nov 2026, confirmed): code symbols λ̄, χ, α kept (as Ch. 4 kept k and K); the Ayrton–Perry imperfection is **ζ**, not
   the usual η, because η is the load parameter of the book.
3. Sources (24 Nov): Fang & Winter (1965) read but not cited (rarely cited; it restates Chajes & Winter). §5.2 cites
   Chajes & Winter (1965) and AISC 360-22 §E4 (free); Trahair, SSRC, Bažant & Cedolin still not available and cited only
   for standard formulas. Hutchinson (2016, spheres) goes to Ch. 7–8 (SOURCES.md §4g).
4. Draft notes resolved 24 Nov: Dee Bridge → Petroski, Civil Engineering 64(4) (1994) 52–55; Marcy → ENR, 11 Oct 2002
   (steel tub girders rolled to one side during the deck pour; no cause stated there); Quebec bow 19 → 57 mm → Brady,
   Engineers Journal, 29 May 2019; ruler constant 4.013 confirmed (Harvey et al., Eng. Struct. preprint, cites Timoshenko
   & Gere). Left: the Cast3M syntax (multifibre model, initial stresses in pasapas).
5. FEniCS: not used in this chapter (shells come in Ch. 7); the Python fibre column is the closed-form check.
6. The Hartford box says "four steel angles arranged in a cross"; whether they were bolted or welded is not in the
   sources read.

## Sources
Hutchinson (1974), Hibbeler 9th ed. Ch. 13 (PDF = book + 25), Chajes & Winter (1965), AISC 360-22 §E4, Freddi, Morassi &
Paroni (2007), Huber & Beedle (1954), Gerard & Becker (1957) via Hutchinson, Duberg & Wilder (1952), Onat & Drucker (1953),
Martin & Delatte (2001), Loomis et al. (1980), Pearson & Delatte (2006), Petroski (1994), ENR (2002), Brady (2019), Bushnell §7.
Photographs: none in the book. Magazine and press photos (ENR, STRUCTURE, Engineers Journal, LZA/AP for Hartford) are
copyrighted and the repository is public; candidates that can be used are public-domain images (Quebec Bridge 1907,
Library and Archives Canada / Wikimedia Commons; Dee Bridge 1847, Illustrated London News engraving), to be uploaded
by the author. Details: `SOURCES.md`.

## Papers needed
(ask the author to upload them; tick when received)
- [ ] EN 1993-1-1 (2005, or the 2022 revision) §6.3: column curves and lateral-torsional buckling
- [ ] Royal Commission, Quebec Bridge Inquiry Report (1908)
- [ ] papers on buckling of thin shells under residual / welding stresses (author's choice)
