import Mathlib

/-!
Finite scalar power-iteration bound used in the QMSVE appendix.

The proof starts at the spectral-weight reduction: `w` are the normalized
initial spectral weights and `q` are nonnegative scalar response values.
Matrix/SVD and QSVT realization are outside this formal statement.
-/

theorem weighted_power_postselection_bound
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (w q : ι → ℝ) (T : Finset ι) (qStar r : ℝ) (t : ℕ)
    (hw_nonneg : ∀ i, 0 ≤ w i)
    (hw_sum : ∑ i, w i = 1)
    (hq_nonneg : ∀ i, 0 ≤ q i)
    (hqStar_pos : 0 < qStar)
    (hr_nonneg : 0 ≤ r)
    (hr_lt_one : r < 1)
    (hq_target : ∀ i ∈ T, q i = qStar)
    (hq_outside : ∀ i ∉ T, q i ≤ r * qStar)
    (hmass_pos : 0 < ∑ i ∈ T, w i) :
    let a : ℝ := ∑ i ∈ T, w i
    let m : ℕ := 2 * t
    let qPow : ℝ := qStar ^ m
    let P : ℝ := ∑ i, w i * q i ^ m
    0 < P ∧ a * qPow ≤ P ∧ P ≤ qPow ∧
      1 - (a * qPow) / P ≤ ((1 - a) / a) * r ^ m := by
  dsimp only
  let a : ℝ := ∑ i ∈ T, w i
  let m : ℕ := 2 * t
  let qPow : ℝ := qStar ^ m
  let P : ℝ := ∑ i, w i * q i ^ m
  let E : ℝ := ∑ i ∈ Tᶜ, w i * q i ^ m

  have hqStar_nonneg : 0 ≤ qStar := le_of_lt hqStar_pos
  have hr_le_one : r ≤ 1 := le_of_lt hr_lt_one
  have hscale : r * qStar ≤ qStar := by
    simpa using (mul_le_mul_of_nonneg_right hr_le_one hqStar_nonneg)

  have hsplitW : a + (∑ i ∈ Tᶜ, w i) = 1 := by
    calc
      a + (∑ i ∈ Tᶜ, w i) = (∑ i ∈ T, w i) + ∑ i ∈ Tᶜ, w i := by rfl
      _ = ∑ i, w i := Finset.sum_add_sum_compl T w
      _ = 1 := hw_sum
  have hcompW_nonneg : 0 ≤ ∑ i ∈ Tᶜ, w i :=
    Finset.sum_nonneg fun i hi => hw_nonneg i
  have ha_le_one : a ≤ 1 := by linarith
  have hcompW : (∑ i ∈ Tᶜ, w i) = 1 - a := by linarith

  have hq_le_star : ∀ i, q i ≤ qStar := by
    intro i
    by_cases hi : i ∈ T
    · rw [hq_target i hi]
    · exact (hq_outside i hi).trans hscale

  have htargetP : (∑ i ∈ T, w i * q i ^ m) = a * qPow := by
    calc
      (∑ i ∈ T, w i * q i ^ m) = ∑ i ∈ T, w i * qPow := by
        apply Finset.sum_congr rfl
        intro i hi
        rw [hq_target i hi]
      _ = (∑ i ∈ T, w i) * qPow := (Finset.sum_mul T w qPow).symm
      _ = a * qPow := by rfl

  have hdecomp : a * qPow + E = P := by
    have h := Finset.sum_add_sum_compl T (fun i => w i * q i ^ m)
    rw [htargetP] at h
    simpa [P, E] using h

  have hE_nonneg : 0 ≤ E := by
    apply Finset.sum_nonneg
    intro i hi
    exact mul_nonneg (hw_nonneg i) (pow_nonneg (hq_nonneg i) m)

  have htarget_pos : 0 < a * qPow :=
    mul_pos hmass_pos (pow_pos hqStar_pos m)
  have hqPow_pos : 0 < qPow := pow_pos hqStar_pos m
  have hP_lower : a * qPow ≤ P := by linarith [hdecomp, hE_nonneg]
  have hP_pos : 0 < P := lt_of_lt_of_le htarget_pos hP_lower

  have hP_upper : P ≤ qPow := by
    calc
      P = ∑ i, w i * q i ^ m := rfl
      _ ≤ ∑ i, w i * qPow := by
        apply Finset.sum_le_sum
        intro i hi
        exact mul_le_mul_of_nonneg_left
          (pow_le_pow_left₀ (hq_nonneg i) (hq_le_star i) m) (hw_nonneg i)
      _ = (∑ i, w i) * qPow := (Finset.sum_mul Finset.univ w qPow).symm
      _ = qPow := by rw [hw_sum]; simp

  have hE_upper : E ≤ (1 - a) * r ^ m * qPow := by
    calc
      E = ∑ i ∈ Tᶜ, w i * q i ^ m := rfl
      _ ≤ ∑ i ∈ Tᶜ, w i * (r * qStar) ^ m := by
        apply Finset.sum_le_sum
        intro i hi
        exact mul_le_mul_of_nonneg_left
          (pow_le_pow_left₀ (hq_nonneg i) (hq_outside i (Finset.mem_compl.mp hi)) m)
          (hw_nonneg i)
      _ = (∑ i ∈ Tᶜ, w i) * (r * qStar) ^ m :=
        (Finset.sum_mul Tᶜ w ((r * qStar) ^ m)).symm
      _ = (1 - a) * r ^ m * qPow := by
        rw [hcompW, mul_pow]
        simp [qPow]
        ring

  have hEbound_nonneg : 0 ≤ (1 - a) * r ^ m * qPow :=
    mul_nonneg (mul_nonneg (sub_nonneg.mpr ha_le_one) (pow_nonneg hr_nonneg m))
      (pow_nonneg hqStar_nonneg m)
  have hquot : ((1 - a) * r ^ m * qPow) / (a * qPow) =
      ((1 - a) / a) * r ^ m := by
    calc
      ((1 - a) * r ^ m * qPow) / (a * qPow) = ((1 - a) * r ^ m) / a := by
        simpa [mul_assoc] using
          (mul_div_mul_right (c := qPow) ((1 - a) * r ^ m) a
            (ne_of_gt hqPow_pos))
      _ = ((1 - a) / a) * r ^ m := by ring
  have hEdiv : E / P ≤ ((1 - a) * r ^ m * qPow) / P :=
    div_le_div_of_nonneg_right hE_upper (le_of_lt hP_pos)
  have hbounddiv : ((1 - a) * r ^ m * qPow) / P ≤
      ((1 - a) * r ^ m * qPow) / (a * qPow) :=
    div_le_div_of_nonneg_left hEbound_nonneg htarget_pos hP_lower
  have hleak_eq : 1 - (a * qPow) / P = E / P := by
    rw [← hdecomp]
    field_simp [ne_of_gt hP_pos]
    ring

  exact ⟨hP_pos, hP_lower, hP_upper,
    by rw [hleak_eq]; calc
      E / P ≤ ((1 - a) * r ^ m * qPow) / P := hEdiv
      _ ≤ ((1 - a) * r ^ m * qPow) / (a * qPow) := hbounddiv
      _ = ((1 - a) / a) * r ^ m := hquot⟩

/-!
If the postselected spectral weights are `v`, the scalar moment differs from
the selected extremal eigenvalue by at most the unselected mass.  This is the
finite-sum readout step; measurement concentration is not part of the theorem.
-/

theorem posterior_moment_deviation_bound
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (v lam : ι → ℝ) (T : Finset ι) (lambda0 : ℝ)
    (hv_nonneg : ∀ i, 0 ≤ v i)
    (hv_sum : ∑ i, v i = 1)
    (hlambda0_nonneg : 0 ≤ lambda0)
    (hlam_bounds : ∀ i, lambda0 ≤ lam i ∧ lam i ≤ 1)
    (hlam_target : ∀ i ∈ T, lam i = lambda0) :
    let F : ℝ := ∑ i ∈ T, v i
    let μ : ℝ := ∑ i, v i * lam i
    0 ≤ μ - lambda0 ∧ μ - lambda0 ≤ (1 - lambda0) * (1 - F) := by
  dsimp only
  let F : ℝ := ∑ i ∈ T, v i
  let μ : ℝ := ∑ i, v i * lam i
  let Vout : ℝ := ∑ i ∈ Tᶜ, v i
  let Mout : ℝ := ∑ i ∈ Tᶜ, v i * lam i

  have hFsplit : F + Vout = 1 := by
    calc
      F + Vout = (∑ i ∈ T, v i) + ∑ i ∈ Tᶜ, v i := by rfl
      _ = ∑ i, v i := Finset.sum_add_sum_compl T v
      _ = 1 := hv_sum

  have hMsplit : lambda0 * F + Mout = μ := by
    have hTarget : (∑ i ∈ T, v i * lam i) = lambda0 * F := by
      calc
        (∑ i ∈ T, v i * lam i) = ∑ i ∈ T, v i * lambda0 := by
          apply Finset.sum_congr rfl
          intro i hi
          rw [hlam_target i hi]
        _ = (∑ i ∈ T, v i) * lambda0 := (Finset.sum_mul T v lambda0).symm
        _ = lambda0 * F := by dsimp [F]; ring
    have h := Finset.sum_add_sum_compl T (fun i => v i * lam i)
    rw [hTarget] at h
    simpa [μ, Mout] using h

  have hGapEq : μ - lambda0 = ∑ i ∈ Tᶜ, v i * (lam i - lambda0) := by
    calc
      μ - lambda0 = (lambda0 * F + Mout) - lambda0 := by rw [hMsplit]
      _ = Mout - lambda0 * Vout := by linear_combination lambda0 * hFsplit
      _ = (∑ i ∈ Tᶜ, v i * lam i) - lambda0 * (∑ i ∈ Tᶜ, v i) := by
        simp [Mout, Vout]
      _ = (∑ i ∈ Tᶜ, v i * lam i) - ∑ i ∈ Tᶜ, v i * lambda0 := by
        rw [← Finset.sum_mul]
        ring
      _ = ∑ i ∈ Tᶜ, (v i * lam i - v i * lambda0) :=
        (Finset.sum_sub_distrib (s := Tᶜ) (fun i => v i * lam i)
          (fun i => v i * lambda0)).symm
      _ = ∑ i ∈ Tᶜ, v i * (lam i - lambda0) := by
        apply Finset.sum_congr rfl
        intro i hi
        ring

  have hGap_nonneg : 0 ≤ ∑ i ∈ Tᶜ, v i * (lam i - lambda0) := by
    apply Finset.sum_nonneg
    intro i hi
    exact mul_nonneg (hv_nonneg i) (sub_nonneg.mpr (hlam_bounds i).1)

  have hGap_upper : (∑ i ∈ Tᶜ, v i * (lam i - lambda0)) ≤
      (1 - lambda0) * (1 - F) := by
    calc
      (∑ i ∈ Tᶜ, v i * (lam i - lambda0)) ≤ ∑ i ∈ Tᶜ, v i * (1 - lambda0) := by
        apply Finset.sum_le_sum
        intro i hi
        exact mul_le_mul_of_nonneg_left
          (sub_le_sub_right (hlam_bounds i).2 lambda0) (hv_nonneg i)
      _ = Vout * (1 - lambda0) := by
        change (∑ i ∈ Tᶜ, v i * (1 - lambda0)) =
          (∑ i ∈ Tᶜ, v i) * (1 - lambda0)
        exact (Finset.sum_mul Tᶜ v (1 - lambda0)).symm
      _ = (1 - lambda0) * (1 - F) := by rw [← hFsplit]; ring

  exact ⟨by rw [hGapEq]; exact hGap_nonneg,
    by rw [hGapEq]; exact hGap_upper⟩
