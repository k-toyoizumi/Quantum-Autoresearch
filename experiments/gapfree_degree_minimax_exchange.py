"""Finite-grid minimax screens for gap-free filtered-mean weights.

Requires the already installed NumPy/SciPy environment. No randomness is used.
Run: python experiments/gapfree_degree_minimax_exchange.py > results/gapfree_degree_minimax_exchange.json
"""
import json
import math
import platform

import numpy as np
import scipy
from numpy.polynomial.chebyshev import chebvander
from numpy.polynomial.chebyshev import chebval
from scipy.optimize import linprog

ETA = 0.1
BIAS_TARGET = 0.01
A_TARGET = BIAS_TARGET * ETA / (1.0 - ETA)
SCALAR_OPTIMUM = 1.0 / 59049.0
L = -0.05
U = 0.05
EMAX = 1.0
W = U - L
R = EMAX - L
T_SCALE = math.sqrt(SCALAR_OPTIMUM)
BASE_GROUND_N = 21
BASE_EXCITED_N = 101
BASE_SUPPORT_N = 201
VALIDATION_GROUND_N = 101
VALIDATION_EXCITED_N = 501
VALIDATION_SUPPORT_N = 501
EXCHANGE_ROUNDS = 5
CUTS_PER_ROUND = 4
PRIMAL_TOL = 1e-9
DUAL_TOL = 1e-9


def basis(x, degree):
    return chebvander(2.0 * np.asarray(x) / R - 1.0, degree)


def pair_row_weight(v_ground, v_excited, distance, bias):
    a = bias * ETA / (1.0 - ETA)
    # Equivalent to (d-b) w(y) <= A w(x); row scaling by A avoids tiny rows.
    return ((distance - bias) / a) * v_excited - v_ground


def pair_row_amplitude(v_ground, v_excited, distance, bias):
    a = bias * ETA / (1.0 - ETA)
    q = math.sqrt(a / (distance - bias))
    # For nonnegative p, this is equivalent to |p(y)|^2/|p(x)|^2 <= A/(d-b).
    return v_excited / q - v_ground


def primal_dual_diagnostics(result, matrix, rhs, objective):
    primal = float(np.max(matrix @ result.x - rhs))
    marginals = result.ineqlin.marginals
    dual_objective = float(rhs @ marginals)
    stationarity = float(np.max(np.abs(objective - matrix.T @ marginals)))
    return {
        "max_primal_inequality_violation": primal,
        "dual_objective": dual_objective,
        "primal_objective": float(result.fun),
        "primal_minus_dual_gap": float(result.fun - dual_objective),
        "dual_stationarity_inf_norm": stationarity,
        "interpretation": "floating-point HiGHS diagnostics, not an exact certificate",
    }


def run_lp(family, amplitude_degree, design_bias, p_floor=0.0):
    if family not in ("weight", "amplitude"):
        raise ValueError(family)
    degree = 2 * amplitude_degree if family == "weight" else amplitude_degree
    nvar = degree + 2
    t_index = degree + 1
    A_design = design_bias * ETA / (1.0 - ETA)
    x0 = np.linspace(0.0, W, BASE_GROUND_N)
    y = np.linspace(0.0, R, BASE_EXCITED_N)
    xs = np.linspace(0.0, R, BASE_SUPPORT_N)
    V0, Vy, Vs = basis(x0, degree), basis(y, degree), basis(xs, degree)
    rows, rhs = [], []

    for v in Vs:
        rows.append(np.r_[v, 0.0]); rhs.append(1.0)
        rows.append(np.r_[-v, 0.0]); rhs.append(0.0 if family == "weight" else -p_floor)
    for v in V0:
        rows.append(np.r_[-v / T_SCALE, 1.0]); rhs.append(0.0)
    pair_count = 0
    for i, ground in enumerate(x0):
        for j, excited in enumerate(y):
            d = excited - ground
            if d > design_bias:
                pair = (pair_row_weight(V0[i], Vy[j], d, design_bias)
                        if family == "weight"
                        else pair_row_amplitude(V0[i], Vy[j], d, design_bias))
                rows.append(np.r_[pair, 0.0]); rhs.append(0.0); pair_count += 1

    history, cuts = [], []
    for iteration in range(EXCHANGE_ROUNDS + 1):
        matrix = np.asarray(rows)
        rhs_array = np.asarray(rhs)
        objective = np.zeros(nvar)
        objective[t_index] = -1.0
        result = linprog(
            objective,
            A_ub=matrix,
            b_ub=rhs_array,
            bounds=[(None, None)] * nvar,
            method="highs",
            options={"primal_feasibility_tolerance": PRIMAL_TOL,
                     "dual_feasibility_tolerance": DUAL_TOL},
        )
        if not result.success:
            return {"family": family, "amplitude_degree": amplitude_degree,
                    "weight_degree": 2 * amplitude_degree, "status": result.status,
                    "message": result.message, "iterations": history, "cuts": cuts}

        coefficients = result.x[:degree + 1]
        grid_min_amplitude = result.x[t_index] * T_SCALE
        x0v = np.linspace(0.0, W, VALIDATION_GROUND_N)
        yv = np.linspace(0.0, R, VALIDATION_EXCITED_N)
        xsv = np.linspace(0.0, R, VALIDATION_SUPPORT_N)
        ground_values = basis(x0v, degree) @ coefficients
        excited_values = basis(yv, degree) @ coefficients
        support_values = basis(xsv, degree) @ coefficients
        dmat = yv[:, None] - x0v[None, :]
        weight_ground = ground_values**2 if family == "amplitude" else ground_values
        weight_excited = excited_values**2 if family == "amplitude" else excited_values
        if family == "weight":
            denom = ETA * weight_ground[None, :] + (1.0 - ETA) * weight_excited[:, None]
            bias_matrix = np.divide(
                (1.0 - ETA) * weight_excited[:, None] * dmat,
                denom,
                out=np.zeros_like(dmat), where=denom > 1e-300)
            ratio_violation = np.divide(
                (dmat - design_bias) * weight_excited[:, None],
                A_design * weight_ground[None, :],
                out=np.full_like(dmat, np.inf), where=weight_ground[None, :] > 1e-300) - 1.0
        else:
            denom = ETA * weight_ground[None, :] + (1.0 - ETA) * weight_excited[:, None]
            bias_matrix = np.divide(
                (1.0 - ETA) * weight_excited[:, None] * dmat,
                denom,
                out=np.zeros_like(dmat), where=denom > 1e-300)
            q = np.sqrt(A_design / np.maximum(dmat - design_bias, 1e-300))
            ratio_violation = np.divide(
                np.abs(excited_values[:, None]), q * np.abs(ground_values[None, :]),
                out=np.full_like(dmat, np.inf), where=np.abs(ground_values[None, :]) > 1e-300) - 1.0
        pair_mask = dmat > design_bias
        ratio_violation[~pair_mask] = -np.inf
        bias_mask = dmat >= BIAS_TARGET
        dense_max_bias = float(np.max(bias_matrix[bias_mask]))
        max_relative_violation = float(np.max(ratio_violation[pair_mask]))
        l1_norm = float(np.sum(np.abs(coefficients)))
        if family == "weight":
            grid_ground_weight = float(grid_min_amplitude)
            dense_bracket_weight = max(0.0, float(np.min(ground_values)))
        else:
            grid_ground_weight = float(grid_min_amplitude**2)
            dense_bracket_weight = (max(0.0, float(np.min(ground_values))) / max(l1_norm, 1.0))**2
        diagnostics = primal_dual_diagnostics(result, matrix, rhs_array, objective)
        history.append({
            "exchange_round": iteration,
            "grid_objective_min_ground_response": float(grid_min_amplitude),
            "grid_objective_min_ground_weight_before_l1_scaling": grid_ground_weight,
            "dense_min_ground_amplitude": float(np.min(ground_values)),
            "dense_min_support_amplitude_or_weight": float(np.min(support_values)),
            "dense_max_support_amplitude_or_weight": float(np.max(support_values)),
            "dense_max_filtered_mean_bias_at_target": dense_max_bias,
            "dense_max_relative_pair_violation_at_design_bias": max_relative_violation,
            "chebyshev_coefficient_l1_norm": l1_norm,
            "bracket_min_weight_after_global_l1_scaling": dense_bracket_weight,
            "lp_diagnostics": diagnostics,
        })

        if iteration == EXCHANGE_ROUNDS:
            break
        # Add the four worst dense-grid pair constraints. This is an exchange
        # screen, not a continuous optimization or a convergence certificate.
        valid_indices = np.argwhere(pair_mask)
        valid_scores = ratio_violation[pair_mask]
        top = np.argpartition(valid_scores, -min(CUTS_PER_ROUND, len(valid_scores)))[-min(CUTS_PER_ROUND, len(valid_scores)):]
        added_this_round = 0
        for idx in top:
            iy, ix = valid_indices[idx]
            score = float(valid_scores[idx])
            if score <= 1e-8:
                continue
            distance = float(dmat[iy, ix])
            vg = basis([float(x0v[ix])], degree)[0]
            ve = basis([float(yv[iy])], degree)[0]
            pair = (pair_row_weight(vg, ve, distance, design_bias)
                    if family == "weight"
                    else pair_row_amplitude(vg, ve, distance, design_bias))
            rows.append(np.r_[pair, 0.0]); rhs.append(0.0)
            cuts.append({"ground_offset": float(x0v[ix]), "excited_offset": float(yv[iy]),
                         "distance": distance, "relative_violation_before_cut": score})
            added_this_round += 1
        # Add worst continuous-validation grid support violation as another cut.
        if family == "weight":
            lower_bad = float(np.min(support_values)) < -1e-8
            upper_bad = float(np.max(support_values)) > 1.0 + 1e-8
        else:
            lower_bad = float(np.min(support_values)) < p_floor - 1e-8
            upper_bad = float(np.max(support_values)) > 1.0 + 1e-8
        if lower_bad:
            j = int(np.argmin(support_values)); v = basis([float(xsv[j])], degree)[0]
            rows.append(np.r_[-v, 0.0]); rhs.append(0.0 if family == "weight" else -p_floor)
        if upper_bad:
            j = int(np.argmax(support_values)); v = basis([float(xsv[j])], degree)[0]
            rows.append(np.r_[v, 0.0]); rhs.append(1.0)
        if added_this_round == 0 and not lower_bad and not upper_bad:
            break

    return {
        "family": family,
        "amplitude_degree": amplitude_degree,
        "weight_degree": 2 * amplitude_degree,
        "design_bias": design_bias,
        "validation_bias_target": BIAS_TARGET,
        "minimum_amplitude_floor_on_support_grid": p_floor,
        "status": result.status,
        "status_message": result.message,
        "base_grids": {"ground": BASE_GROUND_N, "excited": BASE_EXCITED_N,
                       "support": BASE_SUPPORT_N, "pair_constraints": pair_count},
        "validation_grids": {"ground": VALIDATION_GROUND_N,
                              "excited": VALIDATION_EXCITED_N,
                              "support": VALIDATION_SUPPORT_N},
        "iterations": history,
        "pair_cuts": cuts,
        "final_raw_chebyshev_coefficients": coefficients.tolist(),
        "coefficient_l1_norm": l1_norm,
        "final_dense_validation_passes_target": dense_max_bias <= BIAS_TARGET,
        "continuous_certificate": False,
        "lp_optimum_status_warning": "HiGHS floating optimum and primal/dual residuals are not exact certificates; primal objective is not by itself an upper bound on the relaxed optimum",
    }


def main():
    specs = [
        ("weight", 16, BIAS_TARGET, 0.0),
        ("weight", 30, BIAS_TARGET, 0.0),
        ("amplitude", 16, BIAS_TARGET, 0.0),
        ("amplitude", 20, BIAS_TARGET, 0.0),
        ("amplitude", 20, 0.0095, 1e-5),
    ]
    runs = [run_lp(*spec) for spec in specs]
    output = {
        "metadata": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "seed": None,
            "deterministic": True,
            "parameters": {"eta": ETA, "bias_target": BIAS_TARGET,
                           "ground_bracket": [L, U], "support": [L, EMAX],
                           "gap": "unknown", "A": A_TARGET,
                           "scalar_unconstrained_optimum": SCALAR_OPTIMUM,
                           "shifted_power_degree_58_raw_transmission": 9.077777240596324e-6},
            "basis": "Chebyshev T_k(z), z=2(E-L)/(Emax-L)-1",
            "warning": "Finite-grid LP/exchange screening only; no continuous bias certificate, QSVT parity/phase synthesis, compiled depth, or LCU circuit cost. Weight LP is a superset relaxation and the LP solver output is floating point.",
        },
        "runs": runs,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
