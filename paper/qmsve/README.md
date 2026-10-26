# QMSVE technical reassessment drafts

This directory contains Japanese and English review drafts of the supplied QMSVE manuscript. The English file is an internal technical-report draft, not an arXiv submission. Author and affiliation fields remain placeholders because the source copy does not identify them.

## Reproduce the matrix-level results

From the repository root, run:

```sh
python experiments/qmsve_matrix_level.py
python -m json.tool results/qmsve_matrix_level.json >/dev/null
```

The script uses Python, NumPy, and Matplotlib. The saved JSON records the exact versions, fixed seed, matrices, spectral weights, outcomes, and analytic-error diagnostics. It diagonalizes small matrices classically and defines the initial state in the exact right-eigenvector basis. It does not prepare unknown singular vectors, simulate a quantum circuit, synthesize QSVT phases, or establish a quantum-resource advantage.

## Build the PDFs

From `paper/qmsve/`, run:

```sh
xelatex -interaction=nonstopmode -halt-on-error main-en.tex
xelatex -interaction=nonstopmode -halt-on-error main-en.tex
xelatex -interaction=nonstopmode -halt-on-error main-ja.tex
xelatex -interaction=nonstopmode -halt-on-error main-ja.tex
```

Both drafts use the included DejaVu Sans Mono for the Lean source appendix. The Japanese draft also uses the included IPAex Gothic font; both font licenses are included. The figure path is relative to this directory and points to `figures/qmsve_matrix_level.png` at the repository root. The source package requires XeLaTeX and the `fvextra`, `fontspec`, and AMS packages.

## Formalization

`lean/QMSVE.lean` contains the scalar finite-weight postselection theorem. The formal statement begins after the finite spectral-weight reduction; matrix diagonalization, QSVT circuit completion, and readout concentration are outside its scope. See the Lean appendix in both drafts for the exact assumptions and verified status.
