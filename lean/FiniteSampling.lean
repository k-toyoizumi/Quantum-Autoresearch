import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! Scalar ingredients for the finite-attempt extension. This file does not
formalize the binomial distribution, conditional expectations, support-reduction
LP, or the full statistical theorem. -/

theorem inverse_count_upper (m : ℝ) (hm : 1 ≤ m) :
    1 / m ≤ 1 / (m + 1) + 3 / ((m + 1) * (m + 2)) := by
  have hp : 0 < m := by linarith
  have hp1 : 0 < m + 1 := by linarith
  have hp2 : 0 < m + 2 := by linarith
  apply (div_le_iff₀ hp).2
  field_simp
  nlinarith

theorem finite_risk_antitone_in_inverse_count
    (mu e h₁ h₂ : ℝ) (hmu : 0 ≤ mu) (hmu1 : mu ≤ 1)
    (hh : h₂ ≤ h₁) :
    (mu - e)^2 + mu * (1 - mu) * h₂ ≤
      (mu - e)^2 + mu * (1 - mu) * h₁ := by
  have hv : 0 ≤ mu * (1 - mu) := mul_nonneg hmu (by linarith)
  nlinarith

theorem variance_bias_decomposition
    (second mu e variance : ℝ) (hsecond : second = mu^2 + variance) :
    second - 2 * e * mu + e^2 = (mu-e)^2 + variance := by
  rw [hsecond]
  ring

theorem moment_ratio_preserved
    (z z' numerator numerator' mu : ℝ)
    (hz : z ≠ 0) (hz' : z' ≠ 0)
    (hm : numerator = mu*z) (hm' : numerator' = mu*z') :
    numerator'/z' = numerator/z := by
  rw [hm, hm']
  field_simp
