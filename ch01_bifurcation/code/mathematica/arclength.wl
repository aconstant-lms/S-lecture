(* Chapter 1 -- pseudo-arclength continuation in Mathematica (same steps as arclength.py).
   Printed in the book from line 4 on (\lstinputlisting[firstline=4]).
   Run: wolframscript -file arclength.wl *)

continuation[F_, x0_, tguess_, ds_, nsteps_] :=
 Module[{z, vars, Fv, JF, ff, jf, tangent, x, t, xp, R, A, dx, pts, tans, dets},
  vars = Array[z, Length[x0]];                 (* x = (y_1, ..., y_n, r) *)
  Fv = F[vars]; JF = D[Fv, {vars}];            (* [J  F_r], exact derivatives *)
  ff[p_] := Fv /. Thread[vars -> p];
  jf[p_] := JF /. Thread[vars -> p];
  tangent[p_, told_] :=                        (* [J F_r; told] t = e_{n+1} *)
   Normalize[LinearSolve[Append[jf[p], told], UnitVector[Length[p], Length[p]]]];
  x = N[x0]; t = tangent[x, N[tguess]];
  pts = {x}; tans = {t}; dets = {Det[Append[jf[x], t]]};
  Do[
   xp = x + ds t;                              (* 1. predictor *)
   Do[R = Append[ff[xp], t . (xp - x) - ds];   (* 2. Newton corrector *)
    A = Append[jf[xp], t];
    dx = LinearSolve[A, -R]; xp = xp + dx;
    If[Norm[dx] < 10^-10, Break[]], {10}];
   t = tangent[xp, t]; x = xp;                 (* 3. new tangent *)
   AppendTo[pts, x]; AppendTo[tans, t];        (* 4. monitor *)
   AppendTo[dets, Det[Append[jf[x], t]]],
   {nsteps}];
  {pts, tans, dets}]

(* points where a monitor v changes sign, by linear interpolation *)
zeros[pts_, v_] := Table[
  pts[[i]] + v[[i]]/(v[[i]] - v[[i + 1]]) (pts[[i + 1]] - pts[[i]]),
  {i, Select[Range[Length[v] - 1], Sign[v[[#]]] != Sign[v[[# + 1]]] &]}]

(* 1. S-curve y' = h + y - y^3, x = (y, h): folds where t_h changes sign *)
{pts, tans, dets} = continuation[{#[[2]] + #[[1]] - #[[1]]^3} &, {-1.3, -1.3^3 + 1.3}, {0, 1}, 0.05, 70];
Print["folds (y, h): ", zeros[pts, tans[[All, 2]]], "   theory: ", N[{-1/Sqrt[3], 2/(3 Sqrt[3])}]];
Export["s_curve.pdf", ListLinePlot[pts[[All, {2, 1}]], Mesh -> All, AxesLabel -> {"h", "y"}]];

(* 2. Perfect bar theta - p Sin[theta] = 0, x = (theta, p): branch point on theta = 0 *)
{pts, tans, dets} = continuation[{#[[1]] - #[[2]] Sin[#[[1]]]} &, {0., 0.}, {0, 1}, 0.1, 15];
xb = First[zeros[pts, dets]];
Print["branch point at p = ", xb[[2]]];
{ptsb, tansb, detsb} = continuation[{#[[1]] - #[[2]] Sin[#[[1]]]} &, xb + {0.05, 0}, {1, 0}, 0.1, 15];
Print["buckled branch: max |p - theta/sin theta| = ",
  Max[Abs[#[[2]] - #[[1]]/Sin[#[[1]]]] & /@ Rest[ptsb]]];
