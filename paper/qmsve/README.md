# Sharp gap-free bias analysis: QMSVE paper drafts

This directory contains revised Japanese and English drafts based on the QMSVE proposal. The analytical focus is now an exact two-point worst-case mean-bias envelope and sharp gap-free constants for specified cosine and polynomial filters. The combined statement is a small contribution candidate with unresolved priority and publication significance; it is not a new quantum filtering primitive. The drafts remain internal and have not been submitted. Author and affiliation fields remain placeholders.

- `QMSVE-en.pdf`: 12 pages; `main-en.tex` plus `gapfree-en.tex`.
- `QMSVE-ja.pdf`: 10 pages; `main-ja.tex` plus `gapfree-ja.tex`.
- `literature-comparison.md`: overlap and differences from the selected primary literature.
- `claim-evidence.md`: hand proofs, numerical checks, inherited Lean status, and limitations.

## Reproduce the matrix-level results

From the repository root, run:

```sh
python experiments/qmsve_matrix_level.py
python -m json.tool results/qmsve_matrix_level.json >/dev/null
python experiments/qmsve_gapfree_envelope.py
```

Install `requirements-numerics.txt` in a virtual environment first (Python 3.12 was used). The matrix script uses NumPy/Matplotlib; the new envelope script also uses SciPy. Saved JSON records versions, seeds, parameters and outcomes; the new script also records its source hash and base commit. The envelope audit checks 1,000 many-level distributions, dense grids, sharp constants and the global-normalization penalty. Both are scalar/classical audits, not state-preparation or quantum-circuit simulations. Re-running overwrites their named JSON/figure outputs; preserve historical results if required.

## Build the PDFs

From the repository root, run:

```sh
sh paper/qmsve/build.sh
sh paper/qmsve/package-arxiv-source.sh
```

The helper uses XeLaTeX if installed, otherwise Tectonic. It also supports the locally downloaded Tectonic 0.17.0 under `work/tools/` and ICU71 data under `work/tools/icu71/`, using `work/cache/`. These ignored runtime files are not part of the source archive. Japanese line breaking with that static Tectonic build requires the matching ICU data. Standard XeLaTeX needs `fontspec`, `fvextra`, and AMS packages. The included IPAex/DejaVu font licenses are preserved. Successful builds refresh the named `QMSVE-*.pdf` artifacts. The English source ZIP is validated by compilation in an empty directory before replacement; its filename/script name does not imply submission to arXiv.

## Formalization

`lean/QMSVE.lean` contains the unchanged finite-weight leakage and posterior-moment theorems and their inherited successful checker record. The new exact envelope, sharp rates and perturbation results have complete hand proofs in the article but are **not Lean-verified**. Lean/lake was unavailable in this revision's execution environment; no new Lean or CI success is claimed. Matrix reduction, QSVT realization and measurement concentration also remain outside the formalized scope.
