# Literature comparison and novelty boundary

Checked 2026-10-26. This is a bounded primary-source survey, not a proof of priority. The manuscript now has 16 references, including the unpublished source and prior project context. References were added for specific overlapping claims, not to increase the count alone.

| Primary work | Evidence inspected | What is already established / difference from this draft |
|---|---|---|
| [Gilyén et al., QSVT (2019)](https://arxiv.org/abs/1806.01838) | Primary abstract/metadata; standard transformation cited for implementation context. | Polynomial singular-value transformation is the underlying existing primitive; no new QSVT construction here. |
| [Seki–Yunoki (2021)](https://arxiv.org/abs/2008.03661) | Primary abstract/metadata. | Quantum powers and moment-based methods already exist. No claim that power iteration is new. |
| [Kyriienko (2020)](https://doi.org/10.1038/s41534-019-0239-7) | Inherited citation; not re-audited in full text in this revision. | Inverse iteration is established background; no detailed comparative theorem asserted. |
| [Nghiem et al. (2024 preprint / 2025 paper)](https://arxiv.org/html/2407.11744v1) | Sec. II, Lemmas 3–5, Eq. (10)–(11). | Exponentially small power-method success and alternative QSVT transforms are explicitly addressed. Current restart audit cannot be described as the first identification of success overhead. |
| [Ge–Tura–Cirac (2019)](https://arxiv.org/html/1712.03193v2) | Sec. III, Eq. (7)–(22), and overview of known/unknown ground energy. | Powers of cosine, response-ratio convergence, energy shifts, target survival, LCU and amplification predate this draft. This directly overlaps with the original QMSVE analysis. The current result concerns a fixed unshifted response's exact gap-free mean-bias envelope, rather than a preparation theorem with energy/gap information. |
| [Lin–Tong, optimal polynomial filtering (2020)](https://arxiv.org/html/1910.14596v4) | Sec. 3, Lemma 2, minimax problem and target normalization. | Optimizing a polynomial projector with P(0)=1 is prior work. Our maximization is over spectra for a fixed response, not over polynomial design. Kernel preservation and normalized polynomial filtering are not new principles. |
| [Lin–Tong, near-optimal preparation (2020)](https://quantum-journal.org/papers/q-2020-12-14-372/) | Primary abstract and problem assumptions. | Ground-state preparation/energy estimation with overlap/gap information has much stronger algorithmic results; current scalar bounds do not improve those query complexities. |
| [Lu–Bañuls–Cirac (2021)](https://doi.org/10.1103/PRXQuantum.2.020321) | Primary paper's setup and description of cosine filtering and reconstructed observables. | Cosine filters and virtual filtered observables are established. A restart penalty for physical preparation is not a universal cost of virtual filtering. |
| [He–Zhang–Wang (2022)](https://arxiv.org/html/2112.06026v2) | Appendix C, Eq. (20) and comparison with cosine filtering; algorithm overview. | Cosine powers approximate Gaussian filtering. The local Gaussian expansion used in our proof is background. No Gaussian-filter invention is claimed. |
| [Dong–Lin–Tong (2022)](https://arxiv.org/abs/2204.05955) | Primary abstract and oracle/amplification distinctions. | QET-U offers a different input model and stronger algorithmic guarantees; scalar iteration counts cannot be equated to its resource count. |
| [Jo (2026 preprint)](https://arxiv.org/html/2602.19556v1) | Sec. II.1–II.2, Eq. (1)–(9); abstract. | Repeated cosine envelope of controlled time evolution and resonance assumptions overlap. The preprint's performance claims were not independently verified and are not adopted. |
| [Charnes–Cooper (1962)](https://doi.org/10.1002/nav.3800090303) | Original bibliographic record and original fractional-programming context. | Extreme-point / ratio-of-affine optimization is classical. The short two-point argument is self-contained; no new optimization principle is claimed. |
| [Musco–Musco (2015)](https://arxiv.org/abs/1504.05477) | Primary abstract and task description. | Gap-independent approximation in classical power/Krylov methods is established. Their low-rank/PCA task differs from our fixed-response scalar estimator. |

The two QCG-related project references remain background from the inherited bibliography, not additional independent novelty evidence for QMSVE. The supplied unpublished QMSVE PDF itself was not included in the pulled checkout; its original attribution and wording remain an inherited provenance limitation.

## Narrow candidate contribution

1. Exact worst-case filtered-mean envelope for a fixed response, target value and target mass, with an attaining two-level spectrum.
2. For cosine-Gram versus dilation responses, uniform gap-free mean-bias rates with the explicit Lambert-W leading constants and matching varying-spectrum witnesses; conversion to the specified square-root estimator.
3. The same constants for elementary kernel-preserving polynomial baselines, and the exact contrast with exponentially attenuating repeated Taylor normalization.

These statements are fully hand-derived in the revised paper. The ingredients (fractional maximization, Laplace/Gaussian scaling, low-degree filters and postselection perturbations) are elementary or known. The selected works did not expose the same combined sharp statement, but a search miss cannot establish novelty. A reasonable current positioning is a focused analytical note or technical report. We have not established sufficient novelty/significance for a research-journal submission.

## Search and falsification record

Queries included quantum power method / postselection success; cosine filter / gap-free / gap-independent / mean bias; imaginary time / Lambert W / energy error; power method / Lambert W / two-eigenvalue worst case; and classical gap-independent power/Krylov analysis. Broad keyword search is noisy. The most consequential findings were the direct cosine-power analysis in Ge et al. and the target-normalized minimax polynomial in Lin–Tong; both are now explicitly acknowledged in the article.

The candidate must be downgraded to a reproduction if an earlier source gives the same fixed-response overlap-dependent exact envelope and sharp cosine-Gram/dilation constants. Even if priority survives, the result may be too elementary for a standalone paper. A claim of algorithmic improvement would additionally require matched encoding, query/degree, success, state-preparation and readout costs; that claim is not made.
