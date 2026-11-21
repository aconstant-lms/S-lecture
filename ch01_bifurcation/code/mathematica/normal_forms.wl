(* Chapter 1 -- reduction to normal forms in Mathematica (same steps as normal_forms_sympy.py).
   Printed in the book from line 4 on (\lstinputlisting[firstline=4]).
   Run: wolframscript -file normal_forms.wl *)

(* 1. Type of the bifurcation of y' = f(y, r) at (y0, r0), from the Taylor coefficients. *)
classify[f_, {y_, y0_}, {r_, r0_}, assum_ : True] :=
 Module[{d, f0, fy, fr, fyy, fyr, fyyy},
  d[n_, m_] := Simplify[D[f, {y, n}, {r, m}] /. {y -> y0, r -> r0}, assum];
  {f0, fy, fr, fyy, fyr, fyyy} = {d[0, 0], d[1, 0], d[0, 1], d[2, 0], d[1, 1], d[3, 0]};
  Which[
   f0 =!= 0 || fy =!= 0, "not a bifurcation point",
   fr =!= 0 && fyy =!= 0,
    {"fold", "R" -> fr fyy/2 (r - r0), "Y" -> fyy/2 (y - y0)},
   fr === 0 && fyy =!= 0 && fyr =!= 0,
    {"transcritical", "R" -> fyr (r - r0), "Y" -> -fyy/2 (y - y0)},
   fr === 0 && fyy === 0 && fyr =!= 0 && fyyy =!= 0,
    {If[TrueQ[Simplify[fyyy < 0, assum]], "supercritical", "subcritical"] <> " pitchfork",
     "R" -> fyr (r - r0), "fyyy" -> fyyy},
   True, "degenerate: look at higher derivatives"]]

Print[classify[r - y - Exp[-y], {y, 0}, {r, 1}]];             (* the saddle-node in disguise *)
Print[classify[y (1 - y) - r y, {y, 0}, {r, 1}]];              (* proportional catch *)
bar = (-k y + r L Sin[y])/c;                                   (* rigid bar, r = P *)
Print[classify[bar, {y, 0}, {r, k/L}, k > 0 && L > 0 && c > 0]];

(* 2. The normal form of the bar seen directly: Taylor series at the critical load. *)
Print[Normal[Series[bar /. r -> k/L + mu, {y, 0, 3}]] // Expand];

(* 3. The cusp: eliminate y between f = 0 and f_y = 0. *)
fc = h + r y - y^3;
Print[Factor[Resultant[fc, D[fc, y], y]] == 0];
Print[Solve[Resultant[fc, D[fc, y], y] == 0, h]];

(* 4. First Lyapunov coefficient (Guckenheimer & Holmes, eq. 3.4.11) of
      x' = -w y + F(x, y), y' = w x + G(x, y) at the Hopf point. *)
lyapunov1[F_, G_, {x_, y_}, w_] := Module[{d},
  d[e_, n_, m_] := D[e, {x, n}, {y, m}] /. {x -> 0, y -> 0};
  Simplify[(d[F, 3, 0] + d[F, 1, 2] + d[G, 2, 1] + d[G, 0, 3])/16 +
    (d[F, 1, 1] (d[F, 2, 0] + d[F, 0, 2]) - d[G, 1, 1] (d[G, 2, 0] + d[G, 0, 2]) -
       d[F, 2, 0] d[G, 2, 0] + d[F, 0, 2] d[G, 0, 2])/(16 w)]]

(* van der Pol x'' - (mu - x^2) x' + x = 0 at mu = 0, with y = -x' *)
Print["van der Pol: l1 = ", lyapunov1[0, -x^2 y, {x, y}, 1]];
(* galloping x'' + w^2 x = gamma x' - beta x'^3 at gamma = 0, with y = -x'/w *)
Print["galloping:  l1 = ", lyapunov1[0, -beta w^2 y^3, {x, y}, w]];

(* 5. Galloping amplitude: rho' = (gamma/2) rho + l1 rho^3 = 0. *)
Print[Solve[gamma/2 - 3 beta w^2 A^2/8 == 0, A]];
