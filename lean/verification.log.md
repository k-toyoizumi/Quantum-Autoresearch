# Lean verification record

Date: 2026-10-26 UTC

## Toolchain and dependency

- Elan: `4.2.4 (227caca13 2026-08-25)`.
- Lean: `4.35.0`, `x86_64-unknown-linux-gnu`, commit
  `eb6cafb7290e8bd5f2937522d8d804f58f02bafc`.
- Lake: `5.0.0-src+eb6cafb (Lean version 4.35.0)`.
- Mathlib: tag `v4.35.0`, manifest revision
  `56a005855ea17e0b0958f73ec801ae140b0a1679`.
- Main proof source SHA-256:
  `bc9a5a6729b813b1695519174c0ae0f87db7ec00c2c52448b7bc4e9c7e7ada75`.
- Audit source SHA-256:
  `ff58647bcb964095adb3ff826a80d186bb157882722fd859c677971e7feed5ec`.

## Executor workaround

The installed Lean binary initially returned `error: failed to locate
application`. Inspection showed `getpid()` returned an executor-local PID that
was absent from the mounted procfs; the standard `/proc/self/exe` link itself
worked. `tools/procfs_exe_compat.c` is an `LD_PRELOAD` shim for this executor
only. It intercepts numeric `/proc/<pid>/exe` readlink calls and returns the
path supplied by `LEAN_PROC_EXE_OVERRIDE`; all other `readlink` calls pass
through unchanged. It leaves Lean's proof kernel and all proof checking code
untouched. Shim source SHA-256:
`32d15e5330b4bd82971ae17093559b117e48fb300dc3ec389d94bc27d7d3fb8c`.

For the logged local checks, the shim was compiled as
`/tmp/lean-procfs-compat.so` with:

```sh
cc -shared -fPIC -o /tmp/lean-procfs-compat.so tools/procfs_exe_compat.c -ldl
export PATH="$HOME/.elan/bin:$PATH"
export LEAN_PROC_EXE_OVERRIDE="$(elan which lean)"
export LD_PRELOAD=/tmp/lean-procfs-compat.so
```

## Checks and exact results

1. `lean --version` — exit code 0:

   ```text
   Lean (version 4.35.0, x86_64-unknown-linux-gnu, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release)
   ```

2. `lake env lean QMSVE.lean` — exit code 0. The file containing both theorem
   proofs compiled without errors. It reports one harmless linter warning:
   the explicit `hlambda0_nonneg` assumption documents the paper's eigenvalue
   domain `[0,1]` but is not needed for this particular inequality.

3. `lake build QMSVE` — exit code 0:

   ```text
   ⚠ [9047/9048] Built QMSVE (8.4s)
   warning: QMSVE.lean: imports `Mathlib` from package `mathlib`, which is designed for use with the module system; consider adding `module` to the start of this file
   warning: QMSVE.lean:147:5: Variable name `hlambda0_nonneg` is not explicitly referenced.
   Build completed successfully (9048 jobs).
   ```

4. `lake env lean Audit.lean` — exit code 0:

   ```text
   'weighted_power_postselection_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
   'posterior_moment_deviation_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
   ```

5. `rg -n '\b(sorry|admit|axiom)\b' QMSVE.lean Audit.lean` — no matches.

No GitHub Actions run is claimed. The repository root currently has no
`.github/workflows/` entry, and the verified source has not been pushed by this
Lean task. Standard CI verification remains available after stage1 integrates
the files.
