import Mathlib.Basic.Real.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
Scalar algebra used in the filter-selection paper. These statements start
after spectral reduction. They do not formalize QSVT, Bernstein subdivision,
the semi-infinite optimization problem, concentration, or gate costs.
-/

theorem two_point_bias_iff
    (a b d w₀ w : ℝ) (ha : 0 < a) (ha1 : a < 1)
    (hw₀ : 0 < w₀) (hw : 0 ≤ w) :
    ((1-a)*w*d / (a*w₀+(1-a)*w) ≤ b) ↔
      (1-a)*(d-b)*w ≤ a*b*w₀ := by
  have hz : 0 < a*w₀+(1-a)*w :=
    add_pos_of_pos_of_nonneg (mul_pos ha hw₀)
      (mul_nonneg (by linarith) hw)
  rw [div_le_iff₀ hz]
  constructor <;> intro h <;> nlinarith only [h]

theorem finite_mixture_bias_bound
    {ι : Type*} [Fintype ι]
    (v w x : ι → ℝ) (a b e w₀ : ℝ)
    (hv : ∀ i, 0 ≤ v i) (hvs : ∑ i, v i = 1)
    (hw : ∀ i, 0 ≤ w i) (ha : 0 < a) (ha1 : a < 1)
    (hw₀ : 0 < w₀)
    (hpair : ∀ i, (1-a)*((x i-e)-b)*w i ≤ a*b*w₀) :
    let Z := a*w₀+(1-a)*∑ i, v i*w i
    ((1-a)*∑ i, v i*w i*(x i-e))/Z ≤ b := by
  dsimp only
  have hsum : 0 ≤ ∑ i, v i*w i :=
    Finset.sum_nonneg fun i _ => mul_nonneg (hv i) (hw i)
  have hz : 0 < a*w₀+(1-a)*∑ i, v i*w i :=
    add_pos_of_pos_of_nonneg (mul_pos ha hw₀)
      (mul_nonneg (by linarith) hsum)
  apply (div_le_iff₀ hz).2
  have h := Finset.sum_le_sum (s := Finset.univ)
    (fun i _ => mul_le_mul_of_nonneg_left (hpair i) (hv i))
  have hid : (∑ i, v i*((1-a)*((x i-e)-b)*w i)) =
      (1-a)*(∑ i, v i*w i*(x i-e))-b*(1-a)*(∑ i, v i*w i) := by
    simp only [Finset.mul_sum]
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i _
    ring
  have hr : (∑ i, v i*(a*b*w₀)) = a*b*w₀ := by
    rw [← Finset.sum_mul, hvs]
    ring
  rw [hid, hr] at h
  nlinarith only [h]

theorem attenuation_preserves_pair
    (A B w w₀ fx fe : ℝ)
    (hA : 0 ≤ A) (hw : 0 ≤ w)
    (hfx : 0 ≤ fx) (horder : fx ≤ fe)
    (hpair : A*w ≤ B*w₀) :
    A*(fx^2*w) ≤ B*(fe^2*w₀) := by
  have hsq : fx^2 ≤ fe^2 := pow_le_pow_left₀ hfx horder 2
  calc
    A*(fx^2*w) = fx^2*(A*w) := by ring
    _ ≤ fe^2*(A*w) := mul_le_mul_of_nonneg_right hsq (mul_nonneg hA hw)
    _ ≤ fe^2*(B*w₀) := mul_le_mul_of_nonneg_left hpair (sq_nonneg fe)
    _ = B*(fe^2*w₀) := by ring

theorem endpoint_acceptance_factor
    (a m u b S T : ℝ)
    (hu : u < 1) (hub : u+b < 1)
    (hS : S ≤ (a*m*(1-u))/(1-u-b))
    (hT : a*(1-u)^2*m ≤ T) :
    (1-u)*(1-u-b)*S ≤ T := by
  have hden : 0 < 1-u-b := by linarith
  have hcross : (1-u-b)*S ≤ a*m*(1-u) := by
    have h := (le_div_iff₀ hden).mp hS
    simpa only [mul_comm] using h
  calc
    (1-u)*(1-u-b)*S = (1-u)*((1-u-b)*S) := by ring
    _ ≤ (1-u)*(a*m*(1-u)) :=
      mul_le_mul_of_nonneg_left hcross (by linarith)
    _ = a*(1-u)^2*m := by ring
    _ ≤ T := hT

theorem nonnegative_dual_residual_bound
    {ι κ : Type*} [Fintype ι] [Fintype κ]
    (y lhs rhs : ι → ℝ) (r c B : κ → ℝ) (objective : ℝ)
    (hy : ∀ i, 0 ≤ y i) (hrow : ∀ i, lhs i ≤ rhs i)
    (hc : ∀ j, |c j| ≤ B j)
    (hid : objective = (∑ i, y i*lhs i)+(∑ j, r j*c j)) :
    objective ≤ (∑ i, y i*rhs i)+(∑ j, |r j| * B j) := by
  rw [hid]
  apply add_le_add
  · exact Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_left (hrow i) (hy i)
  · apply Finset.sum_le_sum
    intro j _
    calc
      r j*c j ≤ |r j*c j| := le_abs_self _
      _ = |r j| * |c j| := abs_mul _ _
      _ ≤ |r j| * B j := mul_le_mul_of_nonneg_left (hc j) (abs_nonneg _)
