# Appendix text and statement mapping

## English

### Formal scope

The Lean development verifies the finite scalar inequalities after a spectral
decomposition. Let `w_i ≥ 0` be normalized weights, let `T` be the target
indices with total initial mass `a = Σ_{i∈T} w_i > 0`, and let `q_i ≥ 0` be
response values. Assume `q_i = q_* > 0` on `T` and `q_i ≤ r q_*` outside `T`,
where `0 ≤ r < 1`. For `m = 2t`, define

`P_t = Σ_i w_i q_i^m`, `F_t = a q_*^m / P_t`.

`weighted_power_postselection_bound` proves

`0 < P_t`, `a q_*^m ≤ P_t ≤ q_*^m`, and
`1 − F_t ≤ ((1−a)/a) r^m`.

The posterior moment statement is formalized separately. For normalized
posterior weights `v_i ≥ 0`, `Σ_i v_i = 1`, scalar values
`0 ≤ λ_* ≤ λ_i ≤ 1`, and `λ_i = λ_*` on `T`, let
`F = Σ_{i∈T} v_i` and `μ = Σ_i v_i λ_i`. The theorem
`posterior_moment_deviation_bound` proves

`0 ≤ μ − λ_* ≤ (1−λ_*)(1−F)`.

In the application, take `v_i = w_i q_i^m / P_t`; the first theorem ensures
that `P_t` is positive and identifies the target posterior mass with `F_t`.
This substitution is scalar normalization. It does not formalize the matrix
identity that realizes `μ` as a measured observable.

### Relation to the QMSVE algorithms

For maximum-singular-value power iteration, use normalized singular values
`s_i = σ_i/α`, `q_i = s_i²`, `q_* = s_1²`, and `r = (σ_2/σ_1)²`.
For minimum-singular-value cosine-QSVT, use `q_i = cos(β(σ_i/α)²)`,
`q_* = cos(β(σ_min/α)²)`, and an outside response
ratio bounded by `r`; this requires the chosen parameter range to keep the
responses nonnegative and ordered. If a polynomial response is signed, replace
it by its absolute value in this even-power transmission statement.

The formal result starts after the spectral-weight and response-value
reduction. The matrix/SVD reduction, cosine monotonicity and parameter-domain
conditions, QSVT realization, measured-observable identity, square-root error
conversion, and sampling concentration are not Lean-verified here. They must
be supported separately in the body or appendix and should not be attributed
to the Lean checker.

## 日本語

### 形式検証の範囲

Lean証明は、スペクトル分解後の有限個のスカラー不等式を扱う。正規化
重み `w_i ≥ 0` に対し、目標添字集合を `T`、初期目標質量を
`a = Σ_{i∈T} w_i > 0` とする。応答値 `q_i ≥ 0` が目標上で
`q_i = q_* > 0`、目標外で `q_i ≤ r q_*`（`0 ≤ r < 1`）を満たすとする。
`m = 2t`、`P_t = Σ_i w_i q_i^m`、`F_t = a q_*^m/P_t` とおけば、
`weighted_power_postselection_bound` は

`0 < P_t`, `a q_*^m ≤ P_t ≤ q_*^m`, および
`1 − F_t ≤ ((1−a)/a) r^m`

を証明する。

事後分布に対するモーメント評価は別の定理として形式化した。事後重み
`v_i ≥ 0`, `Σ_i v_i = 1`、スカラー値 `0 ≤ λ_* ≤ λ_i ≤ 1`、目標上で
`λ_i = λ_*` を仮定し、`F = Σ_{i∈T} v_i`、`μ = Σ_i v_i λ_i` とする。
`posterior_moment_deviation_bound` は

`0 ≤ μ − λ_* ≤ (1−λ_*)(1−F)`

を証明する。本文の適用では `v_i = w_i q_i^m/P_t` と置く。第一定理が
`P_t > 0` を保証し、目標事後質量が `F_t` になることを示す。この置換は
スカラーの正規化であり、測定 observable と `μ` の一致を表す行列等式の
形式証明ではない。

### QMSVEアルゴリズムとの対応

最大特異値の量子べき乗反復では正規化特異値 `s_i = σ_i/α` を用い、
`q_i = s_i²`, `q_* = s_1²`, `r = (σ_2/σ_1)²` と置く。最小特異値の
cosine-QSVTでは `q_i = cos(β(σ_i/α)²)`,
`q_* = cos(β(σ_min/α)²)` とし、目標外応答の比を `r`
以下に抑える。後者には、選んだパラメータ範囲で応答が非負かつ単調に
並ぶことが必要である。多項式応答が符号付きなら、偶数べき透過確率では
絶対値を `q_i` として用いる。

形式証明の開始点は、スペクトル重みとスカラー応答値への還元後である。
行列/SVD還元、cosineの単調性とパラメータ条件、QSVT実現、測定observable
との行列等式、平方根による誤差変換、標本濃度評価はLean検証の対象外で
あり、本文・付録で別途根拠を示す。これらをLean証明済みとは記載しない。
