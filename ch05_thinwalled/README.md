# Chapter 5: Thin-walled members and real materials

Label prefix `tw` (`sec:tw-*`, `eq:tw-*`, `fig:tw-*`, `exo:tw-*`, bibitem keys `tw-*`).
Status: **outline drafted; §5.4 written (23 Nov 2026)**. `notes/ch05_thinwalled.tex`: Outline in prose; §5.4
`sec:tw-shanley` (inelastic buckling, Shanley's model, Hutchinson's asymptotics, the plastic buckling paradox) written
from Hutchinson (1974) and Hibbeler §13.5, with `fig:tw-shanley` and `code/python/shanley.py`; the other sections are
`\draftnote`s.

## §5.4 as written
- Tangent vs reduced modulus; Example `ex:tw-rod` (Hibbeler Ex. 13.5: 231 → 185 MPa, P_t = 131 kN; rectangle with E_r:
  134 GPa, 206 MPa).
- Shanley's model (Hutchinson's version, K = 0): flanges k_t (loading), k (unloading) at ±d, rigid bars of length L.
  Derived here: P = P_b + (P_r − P_b) x/(c + x), x = Lθ/d, c = (k − k_t)/(k + k_t), for every P_t ≤ P_b ≤ P_r; initial
  slope P_t at P_b = P_t (neutral loading). `shanley.py`: closed form = step-by-step solution to 1e-15.
  gbox `sec:tw-shanley-box`: bifurcation at P_t under increasing load; uniqueness, not stability, is lost.
- Imperfections: no maximum with constant E_t (P → P_r); with a destabilising geometry the drop ∝ θ̄^{1/2}·E/E_t
  (Hutchinson Eq. 2.20); Duberg & Wilder: P_max ≈ P_t.
- Real column (solid circular): P/P_t = 1 + 4ξ + a₂ξ^{4/3} (Hutchinson writes λ₂), P_max/P_t ≈ 1 + (E − E_t)/(3πE_t(1 + q)) (Eqs. 4.59, 4.61);
  1.106 for E_t = E/3, q = 1 (checked). 3/2 power for the spring bed (Eq. 2.47).
- Plastic buckling paradox on the cruciform (pp. 99–101): flow theory keeps G; deformation theory Ḡ (Eq. 3.52), = GE_s/E
  for ν = ½; Gerard & Becker tests; corner (Batdorf, Sanders) or imperfections (Onat & Drucker); Cast3M is a flow theory.

## Thread
Chapter 4 promised two things: columns that twist and columns that yield. The running structure is the Hartford
Civic Center roof (1978), whose top chords were four-angle cruciforms. The cruciform carries the chapter: its
elastic torsional load does not depend on the length, it sits close to yield, and its plastic buckling is the
classic "plastic buckling paradox". The chapter ends with the column curves of the codes.

## Outline (sections and labels)
1. `sec:tw-3d` From 3D to the thin-walled bar (≈15 %). GJ ∝ bt³ vs EI ∝ b³t: open sections twist first; Bredt for
   tubes. Vlasov kinematics (twist φ, sectorial coordinate ω, warping constant Γ, shear centre y₀, z₀). Energy from the
   Ch. 4 fibre strain applied to a fibre at (y, z): the Wagner term ½P r₀²φ'². Γ-convergence: Freddi, Morassi & Paroni
   (J. Elasticity 86, 2007, 263–296; cross-sections of rectangles ε × ε²), Davini, Freddi & Paroni (2014, closed
   sections), Trabucho & Viaño (1996). Limits: local buckling (→ Ch. 6), distortion, short members.
2. `sec:tw-ft` Torsional and flexural–torsional buckling. Three coupled equations, fork supports, cubic in P.
   Doubly symmetric: P_y, P_z, P_φ = (GJ + π²EΓ/L²)/r₀². Monosymmetric: angle and channel in numbers. Lateral–torsional
   buckling of beams, M_cr = (π/L)√(EI_z GJ)√(1 + π²EΓ/(GJL²)). Failures: Dee Bridge 1847, Marcy pedestrian bridge 2002.
   Physical box: a ruler on its edge (P_cr ∝ √(EI_z GJ)/L²).
3. `sec:tw-cruciform` The cruciform. σ_T = G(t/b)², independent of L (gbox). Same as a long plate with one free edge:
   k = 6(1−ν)/π² = 0.426 (textbook 0.425), k = 0.425 + (b/a)² with the legs' own warping → bridge to Ch. 6. Crossover
   length L = π(b²/t)√(E/6G) ≈ 2.07 b²/t for steel. Box: Hartford (Loomis et al. 1980; Martin & Delatte 2001); the mode
   was not in the model (Ch. 3, `sec:nc-trust`). Physical box: a card cruciform cut shorter and shorter.
4. `sec:tw-shanley` Inelastic buckling. Tangent modulus (Engesser), reduced modulus (Considère, Engesser, von Kármán),
   Shanley's paradox and his two-flange model (2 dof, the method of Ch. 2), the imperfect model's maximum load;
   Hutchinson (1974) asymptotics; the plastic buckling paradox of the cruciform (flow vs deformation theory,
   imperfections; Onat & Drucker 1953, Hutchinson & Budiansky 1976, Becque 2016, Shamass 2020 — to check). Hill's
   uniqueness cited, owned by Ch. 9. Hibbeler §13.5 worked example.
5. `sec:tw-curves` Residual stresses and column curves. Rolled, welded, cold-formed patterns; σ₀ self-equilibrated;
   elastic core, weak axis (b_e/b)³ vs strong axis b_e/b; CRC parabola (B&A §2.6). Ayrton–Perry with α(λ̄ − 0.2) →
   European curves (α = 0.13, 0.21, 0.34, 0.49, 0.76; > 1000 ECCS tests; χ(1) = 0.60 on b, 0.54 on c, checked);
   SSRC, AISC; Hibbeler §13.6–13.7 (steel, aluminium, timber; eccentric loads). gbox: a column curve is the maximum
   load of an imperfect, residually stressed, inelastic column. Box: Quebec Bridge 1907 (built-up chord with weak
   latticing = shear-soft column of Ch. 3; bow 19 → 57 mm in two weeks, a Southwell signal of Ch. 4).

Balance target: from 3D ≈15 %, engineering ≈65 %, physical ≈20 % (two table-top boxes: ruler, card cruciform;
CLAUDE.md flagged Ch. 5 as at risk of too little physics).

## Exercises (planned)
- Short questions (8): tubes don't twist; cruciform crossover length; angle strut mode; tangent vs reduced modulus;
  Shanley in one sentence; χ from curve b; weak axis lower; Hartford and the computer model.
- Problems (7): H-section loads and channel cubic; cruciform and the plate check; Shanley perfect and imperfect;
  Lehigh residual stresses and the CRC parabola; Ayrton–Perry vs secant formula; steel/aluminium/timber design
  (Hibbeler numbers); lateral–torsional buckling of a ruler and of a girder during a pour.
- Computer: `code/python/ft_section.py` (thin-walled section properties and the three loads); `shanley.py`
  (continuation with Ch. 1 `arclength.py`); `fibre_column.py` (fibre column with residual stresses and bow, max load vs
  slenderness: the closed-form check for the FE); Cast3M `column_curve.dgibi` (multifibre beams, initial fibre stresses,
  elastic–plastic, bow L/1000, `pasapas` large displacements) and `cruciform.dgibi` (shells, `flambage` at three
  lengths, then plastic: Cast3M's flow theory shows the paradox).
- Session (2 h): (a) by hand, cruciform and angle (30 min); (b) Shanley and Ayrton–Perry in Python (40 min);
  (c) Cast3M column with residual stresses vs the European curve (50 min).

## Decisions and open questions
1. (author, 23 Nov 2026, to confirm) Title "Rods II: thin-walled members and real materials". Folder `ch05_thinwalled`
   and prefix `tw` unchanged. If accepted, the hub updates the plan tables (CLAUDE.md, course_plan), README.md and
   `ch00_intro/notes/overview.tex`.
2. Notation to add (proposal): v (second lateral displacement), φ twist, J, Γ, ω, y₀, z₀, r₀, G, E_t, E_r, P_t, P_r,
   χ, α (imperfection factor). Clashes to accept or avoid: λ̄ (code slenderness) vs λ (growth rate, multiplier, Lamé);
   α vs thermal expansion (Ch. 4 rail exercise). Proposal: keep the code symbols λ̄, χ, α, as Ch. 4 kept k and K.
3. Cast3M syntax for initial fibre stresses in multifibre beams (`pasapas` table, 'CONTRAINTES' at time 0) is to be
   checked; the author's `Castem_Introduction` repository may hold a template. Fallback: shell model of the I-section.
4. FEniCS: optional in this chapter (shells come in Ch. 7); the Python fibre column is the closed-form check.
6. (23 Nov 2026) Sources: Bažant & Cedolin, Trahair, Shanley (1947) and the SSRC chapter are not available. Hutchinson
   (1974) was uploaded and carries §5.4. Free substitutes to fetch: Hutchinson 1972 (JAM, Harvard page), Stowell NACA
   Rep. 898 and Rep. 946 (cruciform), Fang & Winter 1965 (Scholars' Mine, torsional–flexural), Lehigh Fritz Lab reports
   (Huber & Beedle 1954, Bjorhovde 1972). Shanley's paper is cited through Hutchinson's account.
7. Notation added to the notation list: E_t, E_s, E_r, P_t, P_r, G, Ḡ, and Shanley's k, k_t, d, c (k also is the
   foundation stiffness of Ch. 4 and k_t has no clash).
5. From 3D (hub, 23 Nov 2026): Trabucho & Viaño (1996) and Viaño's later work justify Saint-Venant and Vlasov models;
   Freddi–Morassi–Paroni (2007) checked and added to the chapterbib.

## Hibbeler, *Mechanics of Materials*, 9th ed. (2014), Ch. 13 (uploaded 23 Nov 2026; PDF page = book page + 25)
- §13.5 Inelastic buckling, pp. 688–695 (PDF 713–720): short/intermediate/long columns; Eq. 13-20 tangent modulus
  (Engesser 1889), Fig. 13-18; Shanley named in words only. Example 13.5: rod Ø30 mm, L = 600 mm, pinned, bilinear
  σ–ε (150 MPa at 0.001, 270 MPa at 0.002): elastic guess 231 MPa > σ_pl, so E_t = 120 GPa, σ_cr = 185 MPa, P = 131 kN.
  Prob. 13-70: tangent modulus from σ = 40 ksi at KL/r = 60.
- §13.6 Concentric loading, pp. 696–705 (PDF 721–730): Fig. 13-20 tests vs the secant curves, "accidental"
  ec/r² = 0.1–0.6. AISC (ASD): Euler with F.S. 23/12 (Eq. 13-21); (KL/r)_c = √(2π²E/σ_Y) because residual stresses
  reach ½σ_Y (Eq. 13-22); the CRC parabola with a variable F.S. (Eq. 13-23). Aluminium 2014-T6, Eqs. 13-24–13-26;
  timber (NFPA), Eqs. 13-27–13-29. Examples 13.6 (W10×100, A992, pinned), 13.7 (rod fixed at both ends, 18 kip),
  13.8 (2014-T6 bar, 30 in., 12 kip, section b × 2b), 13.9 (timber board 5.5 × 1.5 in., 5 kip, longest L).
- §13.7 Eccentric loading, pp. 707– (PDF 732–): Eq. 13-30 σ_max = P/A + Mc/I against σ_allow; Examples 13.10
  (2014-T6, fixed–free), 13.11 (A-36 W6×20).
- Problems that fit this chapter: 13-9 (four laced angles, 25 ft: a built-up column → Quebec, shear-soft column of Ch. 3);
  13-11 (single angle about its weakest axis a–a: Hibbeler checks flexure only; our exercise adds the flexural–torsional
  load). Hibbeler has no torsional or flexural–torsional buckling: §5.1–5.3 need other sources.
- Units: Hibbeler mixes US and SI; the book converts to SI.

## Sources
Bažant & Cedolin (thin-walled beams and elastoplastic buckling; chapter numbers to check on the file), Trahair (1993),
Shanley (1947), Hutchinson (1974), Ziemian / SSRC guide (2010), Brush & Almroth §2.5–2.6, Bushnell §7, Hibbeler 9th ed.
Ch. 13 §13.5–13.7. Failures: Loomis et al. (1980), Martin & Delatte (2001), Pearson & Delatte (2006); Marcy and Dee
Bridge sources to pick. To upload in this thread: Hibbeler Ch. 13, Bažant & Cedolin, Trahair, Shanley (1947),
Hutchinson (1974), the SSRC column chapter. Details and page numbers: `SOURCES.md`.
