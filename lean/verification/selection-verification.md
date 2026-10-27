# Selection scalar lemmas: actual local verification

Verified 2026-10-26 (Japan time), with the pinned toolchain:

- Lean 4.35.0, compiler commit `eb6cafb7290e8bd5f2937522d8d804f58f02bafc`.
- Mathlib v4.35.0, revision `56a005855ea17e0b0958f73ec801ae140b0a1679`.
- `Selection.lean` SHA-256: `5fef2dddefd73730d111e74f6d11a34c788712438a767fa3ba908a21eab8ef29`.
- `SelectionAudit.lean` SHA-256: `e7145a0de060890bcc4381295bc0818e8a7530c5cc03a07b249f9f0e7574e2d3`.
- Source repository base: `74273e4`; new sources were uncommitted when checked, so the source hashes identify this result, not a claim of a committed CI revision.

Actual successful commands, run from `lean/` with the downloaded runtime on PATH:

```sh
lake build Selection
lake env lean SelectionAudit.lean
```

Both exited 0. `selection-build.log` and `selection-axioms.log` are copies of the actual outputs. The five reported dependencies are only `propext`, `Classical.choice`, and `Quot.sound`; no custom axiom or unfinished proof is used. Module-import style warnings are nonfatal. The large umbrella Mathlib import was replaced by specific imports; failed earlier attempts are not evidence of successful checking.

## Exact scope

| Lemma | Verified assertion |
|---|---|
| `two_point_bias_iff` | Cross-multiplication equivalence for a two-point mixture with positive denominator. |
| `finite_mixture_bias_bound` | Pairwise inequalities imply the posterior mean bound for a finite normalized outside mixture and target mass exactly a. |
| `attenuation_preserves_pair` | Ordered nonnegative attenuation factors preserve the scalar pair constraint. |
| `endpoint_acceptance_factor` | The stated endpoint acceptance factor follows algebraically from its supplied upper/lower acceptance estimates. |
| `nonnegative_dual_residual_bound` | Weak duality with an exact stationarity residual correction and coefficient magnitude bounds. |

The full function-space endpoint reduction, actual-mass p0>=a step, spectral/QSVT reduction, semi-infinite optimization, prior-width envelope, Bernstein verifier, phase interval arithmetic and concentration are not Lean formalizations. Their complete mathematical arguments or computational checks are separate in the paper/source.

A GitHub Actions definition for this target is supplied under `.github/workflows/lean-selection.yml`. It has not been pushed or run remotely in this task. There is no remote CI URL to cite and no remote-success claim.
