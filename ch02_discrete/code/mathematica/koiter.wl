(* koiter.wl -- Chapter 2: Koiter (LSK) coefficients of a simple critical point, n dof.
   Same steps as ../python/koiter_sympy.py.  Load with  Get["koiter.wl"]  and run the examples.
   Convention: eta = etac + eta1 xi + eta2 xi^2/2 + ...   (Triantafyllidis, AC-3.13/14). *)

lsk[e_, u_List, eta_, uc_List, du0_List, etac_, mode_List] :=
 Module[{n = Length[u], sub, u1, K, Kp, d3, e3, rhs, v, mu, vs, sol, e4},
  sub = Join[Thread[u -> uc], {eta -> etac}];
  u1 = mode/Sqrt[mode . mode];
  K = D[e, {u, 2}] /. sub;
  If[Simplify[K . u1] =!= ConstantArray[0, n], Print["mode is not a null vector"]; Abort[]];
  (* rate of loss of stiffness along the principal path *)
  Kp = Simplify[(D[D[e, {u, 2}], {u}] . du0 + D[e, {u, 2}, eta] /. sub) . u1 . u1];
  d3 = D[e, {u, 3}] /. sub;
  e3 = Simplify[d3 . u1 . u1 . u1];
  If[e3 =!= 0, Return[{Simplify[-e3/(2 Kp)], None}]];
  (* second-order field: K v = -E_uuu[u1,u1] + mu u1, v orthogonal to u1 *)
  rhs = -d3 . u1 . u1;
  vs = Array[vv, n];
  sol = First@Solve[Join[Thread[K . vs == rhs + mu u1], {u1 . vs == 0}], Append[vs, mu]];
  v = vs /. sol;
  e4 = (D[e, {u, 4}] /. sub) . u1 . u1 . u1 . u1;
  {0, Simplify[-(e4 + 3 d3 . v . u1 . u1)/(3 Kp)]}]

(* ---- examples (compare with koiter_sympy.py) ---- *)
eT = ee (v^2 + (l th)^2) + k/2 (L th)^2 + m/3 (L th)^3 + n/4 (L th)^4 - eta (v + L th^2/2);
etacT = (2 ee l^2 + k L^2)/L;
Print["T model, m != 0: ", lsk[eT, {v, th}, eta, {etacT/(2 ee), 0}, {1/(2 ee), 0}, etacT, {0, 1}]];
Print["T model, m = 0 : ", lsk[eT /. m -> 0, {v, th}, eta, {etacT/(2 ee), 0}, {1/(2 ee), 0}, etacT, {0, 1}]];
Print["bar, lateral   : ", lsk[k (L Sin[th])^2/2 - eta L (1 - Cos[th]), {th}, eta, {0}, {0}, k L, {1}]];
lsp = Sqrt[(L Sin[th] + L)^2 + (L Cos[th])^2];
Print["bar, inclined  : ", lsk[k (lsp - Sqrt[2] L)^2/2 - eta L (1 - Cos[th]), {th}, eta, {0}, {0}, k L/2, {1}]];
eA = c1 x^2/2 + c2 y^2/2 + eta L (-x^2/2 - y^2/2 + x^4/24 + y^4/24 - x^2 y^2/4);
Print["Augusti, mode 1: ", lsk[eA, {x, y}, eta, {0, 0}, {0, 0}, c1/L, {1, 0}]];
Print["Augusti, diag. : ", lsk[Expand[eA /. {c1 -> c, c2 -> c, x -> y}], {y}, eta, {0}, {0}, c/L, {1}]];
