# Finite-sampling extension: critical positioning

Updated 2026-10-27. The user requested ideal circuit operations with finite measurement data, research updates and a revised paper. This extension keeps that scope: the response is ideal and randomness is in independent accept/reject and Bernoulli readout events. The pre-existing paper already had a finite accepted-sample Hoeffding guarantee; adding another shot sweep alone would not constitute a new result.

## Closest additional primary literature

| Source inspected | Established overlap | Scope of the present extension |
|---|---|---|
| [Žnidarič, inverse moments, arXiv:math/0511226, Eqs. 1.1–1.4 and introduction](https://arxiv.org/html/math/0511226) | Positive-binomial inverse moments, approximations by inverse mean, integral methods, classical antecedents dating to the 1940s. | `h_T=E[1/M | M>0]` and its asymptotics are background, not new statistics. We use exact conditional risk and rational upper bounds for the supplied spectral task. |
| [Drakakis, J. Probability and Statistics 2010, 279154, Sec. 2](https://onlinelibrary.wiley.com/doi/10.1155/2010/279154) | Explicit inverse-binomial sums, integral/geometric-series rearrangements and recurrence. | The finite-sum/integral/recurrence computation is not claimed as invented here. |
| [Combes–Ferrie–Jiang–Caves, PRA 89, 052117 (2014), Secs. III–VI](https://arxiv.org/html/1309.6620) | Finite trials, success/failure cost, postselected MSE, restrictions on claims of quantum advantage. | We report abstention separately, count all executions and make no quantum-limit improvement claim. Our unknown-spectrum robust optimization is a particular estimator-design task. |
| [Winkler, Math. Oper. Res. 13, 581–587 (1988)](https://doi.org/10.1287/moor.13.4.581) | Extreme points of moment sets and finite-support representations. | The support principle is established. The paper gives its explicit application to the nonlinear conditional finite-shot risk, via acceptance minimization at fixed conditional mean. |
| [Pinelis, arXiv:1204.0249, Theorem 1 and finite-support corollaries](https://arxiv.org/pdf/1204.0249) | Moment restrictions give atomic representations and reduce extremal measure problems. | We include a self-contained finite-LP proof specialized to the two moment constraints. It is not a new general moment theorem. |
| [Dutkiewicz–O'Brien–Polla, arXiv:2603.21873v2, Sec. 6 and Lemma 29/Theorem 30](https://arxiv.org/html/2603.21873v2) | Ground-energy filter bias, estimator variance and sampling cost, with distinct readout, promises and noise regimes. | Broad bias–variance balancing is already known. We analyze the exact finite count and abstention of a fixed Bernoulli filtered mean, not their estimator or an improvement over it. |

## Precise addition

For a fixed attempt deadline, the accepted count is random. The exact conditional MSE is `(mu-e)^2+mu(1-mu)h_T(z)`, together with an explicit no-output probability and a binomial mixture for tolerance failure. Classical monotonicity of the positive-binomial inverse moment, combined with a two-constraint moment LP, yields a **three-energy representation of the worst conditional MSE over compatible spectra**. We did not identify this exact task-level characterization in the selected sources. This is an incremental structural contribution using standard ingredients, not an exhaustive priority claim or a major new quantum method.

The result does not say that three energies are necessary. No counterexample proving two energies insufficient is claimed: exploratory tests of powers and simple bumps did not supply one (`work/finite-sampling/search_support.py`, `search_bump.py`). The support theorem does not automatically extend to tolerance-failure probability, clipping or other stopping rules. A supporting numerical LP is a consistency check, not a global continuum certificate.

The bound-based finite-budget selector is new to this implementation and task formulation. Its guarantee is uniform conditional-MSE control plus a separate maximum abstention probability, within a finite candidate catalog. It does not certify the exact risk optimum over all polynomials. Bias and success extrema can be incompatible, so the convenient bound is deliberately not called exact. An example where its selected response has worse actual RMSE than the old response is retained in the paper.

## Evaluation and conclusion

The revised paper integrates six physical Ising cases, 48 budget choices, 39 fixed-response shot settings, 2.28 million sampling replicates, 183 exact-law/arithmetic checks and 100 support-reduction controls. It distinguishes conditional MSE, no-output risk and fixed-confidence accuracy. At the representative budget `10^6`, energy RMSE is within tolerance but the actual tolerance-failure probability is about 22.65%, illustrating why these metrics cannot be conflated.

This strengthens the paper as a precise finite-resource analytical/computational preprint. It does not automatically raise it to a high-impact publication, establish quantum advantage, or turn a known application into a new algorithm. The appropriate novelty claim is the scoped spectral reduction and its integration with certified prior-only selection. Independent assessment of importance and priority remains valuable. No arXiv upload or successful remote CI run is claimed.
