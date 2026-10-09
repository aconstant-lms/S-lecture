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
  `chapters/ch1_stability.tex` is the template.
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
- New symbols go into the notation list `front/notation_list.tex` as well as `preamble/notation.tex`.
- Each chapter ends with its own `chapterbib`; bibitem keys must be unique across the whole book.
- Labels are prefixed per chapter: ch1 `*:st-*` (to be fixed for the following chapters), appendices `app:*`.
- Author comments in the sources look like `%% AC: ...`; process them when asked, then delete them.
- Red `\draftnote{...}` marks open questions for the author; leave them unless resolved.

## Workflow
- One conversation per chapter; touch other files only when needed (cross-references, notation).
- Build: `pdflatex -interaction=nonstopmode main.tex` three times. Before committing, the log must have
  no undefined references, no multiply-defined labels and no overfull boxes.
- Python lives in `python/`: figure scripts in `python/figures/<chapter>/` (outputs into `figures/<chapter>`),
  exercise code in `python/examples/<chapter>/`, printed in exercise solutions with
  `\lstinputlisting[firstline=4]{...}` after the results stated in words. Never paste code inline in the .tex.
  The book itself does not mention the repository.
- Commit with a clear message per round of corrections and push to `main`. The commit message becomes
  the release note, so make it readable for the author.
- Every push to `main` triggers `.github/workflows/build-pdf.yml`, which compiles the book and publishes
  `S_lecture_notes.pdf` on the release "latest": https://github.com/aconstant-lms/s-lecture/releases/latest
  After pushing, check the run succeeded and give the author that link.
