# Claim and evidence ledger

| Claim in draft | Evidence | Status and limits |
|---|---|---|
| The QMSVE cosine rule for a rectangular matrix acts on the normalized right Gram operator `G=(A/alpha)^dagger(A/alpha)`. | Algebraic spectral reduction in the manuscript; 7 small matrices in `experiments/qmsve_matrix_level.py`. | Hand derivation and classical matrix audit. The normalization bound and its acquisition cost are inputs. |
| A finite spectral filter with target mass `a>0` and response ratio `r<1` has conditional leakage at most `((1-a)/a) r^(2t)`. | Proof in Appendix A and `lean/QMSVE.lean`. | Lean checks the scalar finite-weight statement only. The matrix-to-weight identification is not formalized. |
| Gram expectation readout converts additive error to a singular-value error bound. | Bernoulli/Hoeffding calculation in Methods and Appendix A. | Analytic derivation assuming ideal accepted-state preparation and independent readout. Circuit error, synthesis, and end-to-end cost are not included. |
| Taylor cosine proxies are bounded on the normalized spectrum. | Taylor remainder scaling argument; diagnostics and values in the saved JSON. | Uniform analytic bound; no QSVT phase sequence, completion, or compiled circuit is supplied. |
| The examples show dependence on overlap, gap, degeneracy, and the right kernel. | Reproducible matrix-level JSON and figure; seed 20261026. | Controlled spectral-weight audit using exact classical right eigenvectors, not an unknown-state preparation experiment. |
| The cosine-Gram and dilation cosine responses differ in convergence and success probability. | Exact response calculations in the matrix-level script. | Their polynomial degree, encoding, and compiled cost are not matched. |
| The proposal is novel or has an end-to-end speedup. | No supporting evidence. | Explicitly not claimed. |
