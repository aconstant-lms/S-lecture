# Stability in Mechanics: lecture notes (working title, first draft)

**Latest PDF:** [releases/latest](https://github.com/aconstant-lms/s-lecture/releases/latest) — rebuilt automatically on every push to `main`.

Same LaTeX model as the notes *Nonlinear Problems in Mechanics*
([npm-lecture](https://github.com/aconstant-lms/npm-lecture)): style, notation and chapter frame are shared.

## Build
    pdflatex main && pdflatex main && pdflatex main        # the book
    pdflatex instructor_manual (twice), pdflatex exercise_sheets (twice)   # after the book
    cd ch01_bifurcation/slides && pdflatex c01_bifurcation  # a deck, from its folder
No BibTeX: every chapter carries its own `chapterbib` list (keys must be unique book-wide).
The index is produced by makeindex, run automatically by `imakeidx` (style `preamble/index.ist`).
`\drafttrue` / `\draftfalse` in `main.tex` shows/hides the red notes to the author.
Uncomment `\includeonly{...}` in `main.tex` to compile a single chapter.

## Layout
One folder per chapter, the same sub-folders everywhere:

    main.tex                      the book (lecture notes)
    exercise_sheets.tex           exercise sessions, questions only
    instructor_manual.tex         exercise sessions with answers and instructor notes
    preamble/                     style.tex, notation.tex (book), manual.tex (sessions), slides.tex (Beamer)
    ch00_intro/                   title page, course overview, list of notation
    ch01_bifurcation/ ... ch09_solids/
        README.md                 planned content, status, decisions
        notes/                    the chapter (chNN_<name>.tex)
        exercises/                the 2 h session (chNN_session.tex)
        slides/                   Beamer deck (cNN_<name>.tex), compiled from its folder
        figures/                  PDF figures (notes and slides)
        code/python  code/mathematica  code/fenics  code/cast3m  code/figures (figure scripts)
        extra/                    material kept for later revisions
    appendices/appA_template/     appendices, same sub-folders

| Ch | Folder | Title |
|---|---|---|
| 1 | `ch01_bifurcation` | Differential equations and bifurcation (drafted) |
| 2 | `ch02_discrete` | Discrete systems: energy and Lagrangian mechanics |
| 3 | `ch03_continuation` | Continuation and finite elements |
| 4 | `ch04_rods` | Rods: the elastica and beyond |
| 5 | `ch05_thinwalled` | Thin-walled members and real materials |
| 6 | `ch06_plates` | Plates |
| 7 | `ch07_cylinders` | Cylindrical shells and imperfection sensitivity |
| 8 | `ch08_shells` | Shells in service: nozzles, prestress and deployable structures |
| 9 | `ch09_solids` | Three-dimensional bodies |

Course plan, conventions, references and the rules for the chapter threads: `CLAUDE.md`.

## Release
[releases/latest](https://github.com/aconstant-lms/s-lecture/releases/latest) holds
`S_lecture_notes.pdf` (every push to `main`), and `S_exercise_sheets.pdf`, `S_instructor_manual.pdf`,
`S_slides_cNN_*.pdf` (rebuilt when exercises, slides or preambles change, or by hand from the Actions tab).

## Notation (preamble/notation.tex)
    vectors, 2nd-order tensors   bold italic    \vect{u} \tens{\sigma}  shortcuts \vu \vn \sig \eps
    4th-order tensors            blackboard     \tensf{C}               shortcuts \bbC \bbS \bbI
    matrices (discrete)          bold upright   \mat{K} \mat{B}
    operators                    \dive \tr \dev \sym \argmin, \T (transpose), \dd (measure), \jump{}
