(* elastica.wl -- Chapter 4: the pinned Euler elastica in closed form, and its asymptotics.
   Same numbers as ../python/elastica.py.  Load with  Get["elastica.wl"].
   Units EI = L = 1, P_c = Pi^2.  Mathematica's EllipticK[m] uses the parameter m = k^2. *)

pOverPc[t0_] := (2 EllipticK[Sin[t0/2]^2]/Pi)^2;               (* P/P_c, t0 = end rotation *)
wOverL[t0_]  := Sin[t0/2]/EllipticK[Sin[t0/2]^2];               (* mid-length deflection *)
dOverL[t0_]  := 2 - 2 EllipticE[Sin[t0/2]^2]/EllipticK[Sin[t0/2]^2];   (* end shortening *)

(* 1. Koiter's expansion from the exact solution *)
Print["P/Pc = ", Normal@Series[pOverPc[t], {t, 0, 4}]];        (* 1 + t^2/8 + 11 t^4/1536 + ... *)

(* 2. the table of the chapter *)
Print[TableForm[
  Table[{d, pOverPc[d Degree], 1 + (d Degree)^2/8, wOverL[d Degree], dOverL[d Degree]} // N,
   {d, {10, 20, 40, 60, 90, 120, 150}}],
  TableHeadings -> {None, {"theta0", "P/Pc", "Koiter", "w/L", "Delta/L"}}]];

(* 3. ends touch: 2E(m) = K(m) *)
mt = m /. FindRoot[2 EllipticE[m] == EllipticK[m], {m, 0.8}];
Print["ends touch at theta0 = ", 2 ArcSin[Sqrt[mt]]/Degree, " deg, P/Pc = ", (2 EllipticK[mt]/Pi)^2];

(* 4. shapes: sin(theta/2) = k sn(sqrt(P) s + K, m), pinned at s = 0 *)
shape[t0_] := Module[{m = Sin[t0/2]^2, q, th, sol},
  q = 2 EllipticK[m];                                            (* sqrt(P) for L = 1 *)
  th[s_] := 2 ArcSin[Sqrt[m] JacobiSN[q s + EllipticK[m], m]];
  sol = NDSolve[{x'[s] == Cos[th[s]], y'[s] == Sin[th[s]], x[0] == 0, y[0] == 0}, {x, y}, {s, 0, 1}];
  ParametricPlot[Evaluate[{x[s], y[s]} /. sol], {s, 0, 1}]];
Show[shape /@ ({20, 60, 90, 130.71, 160} Degree), PlotRange -> All, AspectRatio -> Automatic]

(* 5. Koiter's coefficients from the energy (Chapter 3, Section "Bifurcation of an elastic body"):
      clamped--sliding rod, mode Sqrt[2] Sin[Pi s], <v,w> = Integrate[v w, {s,0,1}]. *)
mode = Sqrt[2] Sin[Pi s];
kp = -Integrate[mode^2, {s, 0, 1}];                               (* kappa' = -1 *)
w4 = Pi^2 Integrate[mode^4, {s, 0, 1}];                           (* W4 = 3 Pi^2/2 *)
Print["eta2/eta_c = ", Simplify[-w4/(3 kp)/Pi^2]];                (* 1/2 *)
