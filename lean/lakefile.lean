import Lake
open Lake DSL

package qmsveFormalization

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.35.0"

lean_lib QMSVE

lean_lib Selection

lean_lib FiniteSampling
