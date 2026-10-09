# Stability in Mechanics: lecture notes (working title, first draft)

**Latest PDF:** [releases/latest](https://github.com/aconstant-lms/s-lecture/releases/latest) — rebuilt automatically on every push to `main`.

Same LaTeX model as the notes *Nonlinear Problems in Mechanics*
([npm-lecture](https://github.com/aconstant-lms/npm-lecture)): style, notation and chapter frame are shared.

## Build
    pdflatex main && pdflatex main && pdflatex main
No BibTeX: every chapter carries its own `chapterbib` list (keys must be unique book-wide).
The index is produced by makeindex, run automatically by `imakeidx` (style `preamble/index.ist`).
`\drafttrue` / `\draftfalse` in `main.tex` shows/hides the red notes to the author.
Uncomment `\includeonly{...}` in `main.tex` to compile a single chapter.

## Layout
    main.tex                      book skeleton (frontmatter, notation list, chapters, appendices)
    preamble/style.tex            RG-style typography: sans-serif headings, gray boxes (gbox),
                                  \exercise{...} + solution environment, chapterbib, TikZ styles
    preamble/notation.tex         notation (copied from the NPM notes, kept in sync)
    front/titlepage.tex           title page
    front/overview.tex            course overview (one page, to be written)
    front/notation_list.tex       list of notation (after the table of contents)
    chapters/ch1_stability.tex    Ch. 1  template chapter with the full frame
    appendices/appA_template.tex  appendix template
    figures/<chapter>/            figures (PDF) produced by the scripts below
    python/figures/<chapter>/     figure scripts (run from their own directory)
    python/examples/<chapter>/    exercise code, printed in the book with \lstinputlisting

## Notation (preamble/notation.tex)
    vectors, 2nd-order tensors   bold italic    \vect{u} \tens{\sigma}  shortcuts \vu \vn \sig \eps
    4th-order tensors            blackboard     \tensf{C}               shortcuts \bbC \bbS \bbI
    matrices (discrete)          bold upright   \mat{K} \mat{B}
    operators                    \dive \tr \dev \sym \argmin, \T (transpose), \dd (measure), \jump{}
