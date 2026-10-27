# Positioning and critical novelty review

The paper is a focused analytical/computational preprint about a specified estimator. It does not present “use different QSVT functions for different problems” as a discovery.

## Closest primary sources inspected

| Source | Inspected overlap | Difference used in this paper |
|---|---|---|
| [Ge–Tura–Cirac, arXiv:1712.03193v2, Sec. III, Eqs. 7–22](https://arxiv.org/html/1712.03193v2) | Cosine powers, response ratios, energy shifts, target survival, LCU and amplification. | No invention of cosine iteration is claimed. The present loss is a uniform gap-free mean over an unknown target interval. |
| [Lin–Tong, arXiv:1910.14596v4, Sec. 3](https://arxiv.org/html/1910.14596v4) | Known isolated target, polynomial minimax projector, target normalization. | We do not claim to invent polynomial minimax or unit-target normalization. Our coupled target/tail constraints and endpoint-nulling acceptance comparison specify a different robust task. |
| [Lee et al., FQPE, arXiv:2510.04294v2, main II and supplementary IV–V](https://arxiv.org/html/2510.04294v2) | Generic bases, cost/overlap tradeoff, coarse information, two stages, known-center minimax, Gaussian/Krylov comparisons. | Strong overlap with the broad original idea. The current contribution is the explicit structural endpoint restriction and its loss factor, followed by certified optimization of a fixed Bernoulli mean/restart model. No improvement to their QPE-based theorem is asserted. |
| [Dong et al., constrained minimax, arXiv:2608.30937](https://arxiv.org/html/2608.30937v1) | Semi-infinite QSP constraints, LP discretization, exchange, continuous feasibility, completion and synthesis. | LP/exchange and phase-aware feasibility are established. Here exact dual residual corrections and rational interval checks are applied to the particular coupled mean-bias selection objective; not a claim of a new approximation algorithm. |
| [Filip–Fitzpatrick, arXiv:2508.00533v3](https://arxiv.org/html/2508.00533v3) | Coarse upper-energy prior, success versus serial queries, implementation normalization. | Prior-sensitive filtering is known. We supply a precise `(1-u)(1-u-b)` comparison for endpoint nulling in the stated mean model; no claim that coarse-prior tradeoffs are first recognized here. |
| [He–Zhang–Wang, arXiv:2112.06026v2, Appendix C](https://arxiv.org/html/2112.06026v2) | Gaussian filtering and cosine approximation comparisons. | No invention of Gaussian/local cosine scaling or superiority over their algorithm. |
| [Dong–Lin–Ni–Wang, arXiv:2307.12468](https://arxiv.org/abs/2307.12468) | Symmetric QSP Newton phase solver. | This is the existing algorithm used by pyqsp, not a new synthesis method. |

The bibliography additionally identifies QSVT foundations, finite-energy/virtual filtering, classical fractional optimization, Bernstein analysis, QET-U and modern alternative estimators.

## Contribution claimed, with limits

The strongest precise result is the controlled endpoint-nulling reduction and its explicit acceptance/cost factor, together with the exact worst-restart characterization after that restriction. These connect a robust unknown-target bias requirement to an operationally exact convex polynomial objective. The numerical study uses continuous certificates and rigorous dual bounds to report a restricted optimality gap, and a continuous certificate for the saved phase response connects the designed polynomial to the ideal oracle implementation.

The ingredients are elementary or established. We did not identify the exact endpoint factor and this coupled mean/restart characterization in the selected closest references or targeted searches. This supports a narrowly stated contribution, not an exhaustive claim of priority over all approximation theory or quantum estimation literature. The paper therefore avoids “first,” general quantum optimality and broad performance claims. If an earlier source contains the same structural theorem and task characterization, the contribution must be reclassified accordingly.

## Objections resolved during the work

1. **Prior already solves the problem.** Early diagnostic cases had u<=4E and were unsuitable as evidence for singular-value estimation. They were removed. Every main case has u>4E, and the no-computation baseline is explicit.
2. **A gridded LP is not a proof.** Candidates require rational continuous certification; dual objectives get exact stationarity corrections. Failed certificates do not become successes through dense-grid checks.
3. **Endpoint nulling is an arbitrary restriction.** Theorem 2 controls its loss with one additional degree, while stating the degree-cap caveat. Near-optimality factors are nevertheless only for the restricted class.
4. **Repeated normalization exaggerates the problem.** Whole-polynomial QSP synthesis applies the safety margin once. The paper does not describe an avoidable per-step scale penalty as a fundamental lower bound.
5. **Scalar diagonal weights do not test the quantum response.** Full block-matrix QSP/LCU checks use a fixed computational input. The synthetic-oracle and hardware limitations remain explicit.
6. **The scalar attaining profile is nonanalytic.** That alone does not rule out another analytic/polynomial attaining profile. The paper explicitly avoids the unsupported generic nonattainment inference found in an earlier project note.
7. **Large costs can conceal weak practical value.** Absolute counts up to billions are shown. No practical quantum advantage is claimed.

## Readiness assessment

The work has a complete stated problem, proofs, related-work comparison, nontrivial numerical cases, code/data/phase certificates, a scoped local Lean check, and self-contained bilingual source. This is an appropriate preparation target for an analytical arXiv preprint, without a claim that arXiv moderation or a journal will accept it. Independent expert review of significance and prior literature remains valuable. Author metadata was intentionally omitted at the user's request; no upload/submission has occurred.
