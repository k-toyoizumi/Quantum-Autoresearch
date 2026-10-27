# Finite-sampling scalar verification (actual local execution)

Verified 2026-10-27 JST. Lean 4.35.0 / Mathlib v4.35.0, same compiler and Mathlib pin as selection-verification.md.

- FiniteSampling.lean SHA-256: `2b2abbc6b502568cefd87886ac0caab950b0217865e741ff25444ea22d7d5a5a`.
- FiniteSamplingAudit.lean SHA-256: `ccdbd29209511affce715a74c65b04e105743960672f6c9deb202adb60264edd`.
- Repository base: c3c27dc. These extension files were uncommitted when checked; hashes identify the actual checked sources.

Commands run from lean/ with the pinned runtime on PATH:

```sh
lake build FiniteSampling
lake env lean FiniteSamplingAudit.lean
```

Both succeeded. `finite-sampling-build.log` and `finite-sampling-axioms.log` are actual outputs. Each of the four lemmas reports only propext, Classical.choice and Quot.sound. No sorry/admit/custom axiom/native_decide is used. Import module-style warnings are nonfatal.

## Scope

- `inverse_count_upper`: for real m>=1, 1/m <= 1/(m+1)+3/((m+1)(m+2)).
- `finite_risk_antitone_in_inverse_count`: the scalar risk expression decreases when its inverse-count argument decreases, with mu in [0,1].
- `variance_bias_decomposition`: second-moment algebra after the moment identity is assumed.
- `moment_ratio_preserved`: preserving numerator=mu*acceptance preserves the ratio when denominators are nonzero.

The exact binomial law, monotonicity of its inverse moment, Jensen, finite-support LP theorem and full three-energy risk theorem are hand proofs, not Lean formalizations. Probability software and rational-power enclosures are independently exercised by exact-enumeration controls, not formally verified programs.

The workflow definition builds both Selection and FiniteSampling and audits both. It has not been pushed or run remotely as part of this extension. There is no successful CI URL to cite.
