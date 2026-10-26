# QMSVE scalar Lean appendix

This folder contains two finite-sum theorems for the scalar stage of the
QMSVE analysis. The first theorem formalizes the power-iteration leakage bound
after spectral reduction. The second theorem formalizes the posterior moment
bound used to convert target mass into scalar readout bias.

## Formal statements and paper mapping

`weighted_power_postselection_bound` assumes a finite normalized spectral
weight distribution `w`, nonnegative scalar responses `q`, `qStar > 0`, and
`0 ≤ r < 1`. For a target set `T`, every target response equals `qStar` and
every outside response is at most `r*qStar`. With target mass
`a = Σ_{i∈T} wᵢ`, iteration count `t`, and
`P = Σᵢ wᵢ qᵢ^(2t)`, it proves

`0 < P`, `a*qStar^(2t) ≤ P ≤ qStar^(2t)`, and
`1 − a*qStar^(2t)/P ≤ ((1−a)/a) r^(2t)`.

For max-singular-value power iteration, set `qᵢ = (σᵢ/α)²`,
`qStar = (σ₁/α)²`, and `r = (σ₂/σ₁)²`. For min-singular-value cosine-QSVT,
set `qᵢ = cos(β (σᵢ/α)²)`, `qStar = cos(β (σ_min/α)²)`, and bound the outside response
ratio by `r` (for ordered nonnegative cosine values,
`r = cos(β σ_next²)/cos(β σ_min²)`). For a signed polynomial response, use
its absolute value as `qᵢ`; the even power in the transmission is unchanged.
The theorem begins after matrix/SVD spectral reduction. It does not formalize
the matrix reduction, cosine monotonicity or angle-domain restrictions, QSVT
realization, or the derivation of the scalar response.

`posterior_moment_deviation_bound` assumes normalized posterior weights `v`,
`0 ≤ lambda0`, and eigenvalues `lambda0 ≤ lamᵢ ≤ 1`, with `lamᵢ = lambda0`
on `T`. For target posterior mass `F = Σ_{i∈T} vᵢ` and moment
`μ = Σᵢ vᵢ lamᵢ`, it proves

`0 ≤ μ − lambda0 ≤ (1−lambda0)(1−F)`.

This is the scalar finite-sum readout step. State preparation and measurement
concentration (including Hoeffding bounds), the matrix identity connecting
the measured observable to this moment, and square-root conversion are outside
the Lean scope and must remain separately sourced or hand-proved in the paper.

## Reproduction

The project pins Lean 4.35.0 and Mathlib tag `v4.35.0`; the exact Mathlib
commit is pinned in `lake-manifest.json`. In a standard Linux environment:

```sh
lake build QMSVE
lake env lean Audit.lean
```

The current executor has a process-PID/procfs namespace mismatch: Lean cannot
resolve `/proc/<pid>/exe` even though `/proc/self/exe` works. For local checks
in that executor only, compile `tools/procfs_exe_compat.c` as a temporary
`LD_PRELOAD` shim and set `LEAN_PROC_EXE_OVERRIDE` to `elan which lean`.
The shim redirects only numeric `/proc/<pid>/exe` lookups. It does not change
Lean, Mathlib, proof terms, or the kernel. A normal CI/Linux runner should use
the two commands above without the shim. The checked local commands and shim
details are recorded in `verification.log.md`.

No `sorry`, `admit`, or user-declared axiom appears in the theorem source.
`#print axioms` reports only Lean's standard `propext`, `Classical.choice`,
and `Quot.sound` dependencies for each theorem.
