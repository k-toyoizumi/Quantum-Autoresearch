#!/usr/bin/env python3
"""Deterministic matrix-level audit of QMSVE power and cosine-Gram filters.

This script diagonalizes small matrices classically. It does not construct a
block-encoding, synthesize QSVT phases, or simulate a quantum circuit.
"""
from __future__ import annotations

import json
import math
import platform
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "qmsve_matrix_level.json"
FIG = ROOT / "figures" / "qmsve_matrix_level.png"
SEED = 20261026
ALPHA = 1.0
BETA = 1.2
ITERATIONS = [0, 1, 2, 4, 8, 16, 32, 64]
SHOT_COUNT = 2000
SHOT_DELTA = 0.05


def make_cases():
    return [
        {
            "name": "square_gap",
            "A": np.diag([0.12, 0.48, 0.86]),
            "probabilities": np.array([0.40, 0.35, 0.25]),
            "description": "full-rank square matrix with a separated minimum",
        },
        {
            "name": "near_degenerate_minimum",
            "A": np.diag([0.20, 0.205, 0.80]),
            "probabilities": np.array([0.30, 0.30, 0.40]),
            "description": "small gap between the two smallest singular values",
        },
        {
            "name": "degenerate_minimum",
            "A": np.diag([0.20, 0.20, 0.70]),
            "probabilities": np.array([0.15, 0.25, 0.60]),
            "description": "two-dimensional minimum-singular subspace",
        },
        {
            "name": "zero_minimum_overlap",
            "A": np.diag([0.12, 0.48, 0.86]),
            "probabilities": np.array([0.0, 0.40, 0.60]),
            "description": "initial state has no component in the minimum eigenspace",
        },
        {
            "name": "wide_full_row_rank",
            "A": np.array([[0.40, 0.0, 0.0], [0.0, 0.80, 0.0]]),
            "probabilities": np.array([0.16, 0.16, 0.68]),
            "description": "wide full-row-rank matrix; right Gram includes a kernel",
        },
        {
            "name": "rank_deficient_square",
            "A": np.diag([0.0, 0.40, 0.80]),
            "probabilities": np.array([0.30, 0.30, 0.40]),
            "description": "square singular matrix; zero is the smallest singular value",
        },
        {
            "name": "rotated_tall_full_column_rank",
            "A": (np.linalg.qr(np.array([[1.0, 2.0], [3.0, 1.0], [2.0, -1.0]]))[0]
                 @ np.diag([0.15, 0.65])
                 @ np.array([[math.cos(0.37), math.sin(0.37)],
                             [-math.sin(0.37), math.cos(0.37)]])),
            "probabilities": np.array([0.35, 0.65]),
            "description": "non-diagonal tall full-column-rank matrix in rotated singular bases",
        },
    ]


def transformed_distribution(probabilities, response, power):
    unnormalized = probabilities * np.power(response, 2 * power)
    success = float(unnormalized.sum())
    if success <= 0.0:
        return None, success
    return unnormalized / success, success


def posterior_metrics(lambdas, probabilities, response, power, target_mode="min"):
    posterior, success = transformed_distribution(probabilities, response, power)
    if posterior is None:
        return {"success_probability": success, "estimate_sigma": None,
                "target_mass": None, "mean_lambda": None,
                "target_mode": target_mode}
    target_lambda = lambdas.min() if target_mode == "min" else lambdas.max()
    target = np.isclose(lambdas, target_lambda, rtol=0.0, atol=1e-14)
    mean_lambda = float(np.dot(posterior, lambdas))
    return {
        "success_probability": success,
        "estimate_sigma": float(math.sqrt(max(0.0, mean_lambda)) * ALPHA),
        "target_mass": float(posterior[target].sum()),
        "mean_lambda": mean_lambda,
        "target_mode": target_mode,
    }


def cos_taylor_polynomial(x, beta, m):
    """Degree 2m Taylor polynomial with an analytic global scaling margin."""
    value = np.zeros_like(np.asarray(x, dtype=float))
    for j in range(m + 1):
        value += ((-1.0) ** j) * beta ** (2 * j) * np.asarray(x) ** (2 * j) / math.factorial(2 * j)
    remainder_bound = beta ** (2 * m + 2) / math.factorial(2 * m + 2)
    # |P-cos(beta*x)| <= remainder_bound on [-1,1], hence |P|<=1+bound.
    return value / (1.0 + remainder_bound), remainder_bound


def main():
    rng = np.random.default_rng(SEED)
    cases_out = []
    plot_rows = {}
    for case in make_cases():
        A = case["A"]
        sv = np.linalg.svd(A, compute_uv=False)
        # Diagonalize the right Gram matrix, retaining right-kernel eigenvectors.
        n = A.shape[1]
        B = A / ALPHA
        gram = B.conj().T @ B
        lambdas, right_vectors = np.linalg.eigh(gram)
        lambdas = np.maximum(lambdas, 0.0)
        if np.linalg.norm(A, 2) > ALPHA + 1e-14:
            raise ValueError(f"normalization alpha={ALPHA} is below ||A||")
        probabilities = case["probabilities"]
        if len(probabilities) != n or np.any(probabilities < 0) or not np.isclose(probabilities.sum(), 1):
            raise ValueError(f"bad initial spectral weights for {case['name']}")
        initial_state = right_vectors @ np.sqrt(probabilities).astype(complex)
        if not np.allclose(np.abs(right_vectors.conj().T @ initial_state) ** 2, probabilities, atol=1e-12):
            raise AssertionError(f"initial-state spectral weights do not match for {case['name']}")
        sigmas = np.sqrt(lambdas)
        responses = {
            "unfiltered": (np.ones_like(lambdas), "min"),
            "gram_power": (lambdas, "max"),
            "cos_gram": (np.cos(BETA * lambdas), "min"),
            "cos_singular_value_variant": (np.cos(BETA * sigmas), "min"),
        }
        rows = []
        for t in ITERATIONS:
            row = {"iterations": t}
            for method, (response, target_mode) in responses.items():
                row[method] = posterior_metrics(lambdas, probabilities, response, t, target_mode)
            rows.append(row)

        polynomial_rows = []
        grid = np.linspace(-1.0, 1.0, 200001)
        for m in [1, 2, 3, 6]:
            q, error_bound = cos_taylor_polynomial(grid, BETA, m)
            max_abs = float(np.max(np.abs(q)))
            # The analytic remainder bound implies the scaled polynomial is bounded by 1.
            assert max_abs <= 1.0 + 2e-12
            q_at_spectrum, _ = cos_taylor_polynomial(lambdas, BETA, m)
            finite = posterior_metrics(lambdas, probabilities, q_at_spectrum, 8)
            polynomial_rows.append({
                "taylor_half_degree": m,
                "polynomial_degree": 2 * m,
                "uniform_error_upper_bound": float(2.0 * error_bound / (1.0 + error_bound)),
                "empirical_grid_max_abs": max_abs,
                "t8_estimate_sigma": finite["estimate_sigma"],
                "t8_target_mass": finite["target_mass"],
                "t8_success_probability": finite["success_probability"],
            })

        shot_row = None
        if case["name"] == "square_gap":
            response = responses["cos_gram"][0]
            posterior, success = transformed_distribution(probabilities, response, 8)
            mean_lambda = float(np.dot(posterior, lambdas))
            outcomes = rng.binomial(1, mean_lambda, size=SHOT_COUNT)
            empirical = float(outcomes.mean())
            radius = math.sqrt(math.log(2.0 / SHOT_DELTA) / (2.0 * SHOT_COUNT))
            estimate_sigma = ALPHA * math.sqrt(empirical)
            shot_row = {
                "shots_are_accepted_spectral_simulator_draws": SHOT_COUNT,
                "seed": SEED,
                "target_delta": SHOT_DELTA,
                "exact_filtered_mean_lambda": mean_lambda,
                "empirical_bernoulli_mean": empirical,
                "hoeffding_radius_lambda": radius,
                "interval_contains_mean": abs(empirical - mean_lambda) <= radius,
                "empirical_sigma_estimate": estimate_sigma,
                "expected_filter_attempts_for_shots": SHOT_COUNT / success,
                "warning": "conditional shot model only; preparation attempts are counted in expectation, no circuit is simulated",
            }
        cases_out.append({
            "name": case["name"],
            "description": case["description"],
            "matrix_shape": list(A.shape),
            "singular_values_as_returned": [float(x) for x in sv],
            "right_gram_eigenvalues": [float(x) for x in lambdas],
            "initial_spectral_probabilities": [float(x) for x in probabilities],
            "initial_state_is_defined_in_exact_right_eigenbasis": True,
            "min_eigenspace_initial_mass": float(probabilities[np.isclose(lambdas, lambdas.min(), atol=1e-14, rtol=0)].sum()),
            "iterations": rows,
            "cos_gram_taylor_proxies": polynomial_rows,
            "shot_readout": shot_row,
        })
        plot_rows[case["name"]] = rows

    # A normalization failure is deliberately detected, not passed to the filter model.
    normalization_failure = None
    try:
        A_bad = np.diag([0.2, 1.01])
        if np.linalg.norm(A_bad, 2) > ALPHA + 1e-14:
            raise ValueError("normalization alpha is below operator norm")
    except ValueError as exc:
        normalization_failure = str(exc)

    data = {
        "experiment": "QMSVE matrix-level filter audit",
        "model": "exact right-Gram spectral weights with analytic cosine-Taylor proxies and Bernoulli moment readout",
        "seed": SEED,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
        "normalization_alpha": ALPHA,
        "beta": BETA,
        "beta_condition": "0 < beta < pi/2, so cos(beta*x) is positive and decreasing on x in [0,1]",
        "iterations": ITERATIONS,
        "normalization_failure_case": normalization_failure,
        "cases": cases_out,
        "limitations": [
            "classical diagonalization of small matrices; no quantum circuit or QSVT phase synthesis",
            "conditional postselection probabilities are ideal spectral-model probabilities",
            "polynomial boundedness follows from a Taylor remainder scaling argument; empirical grid maxima are diagnostic only",
            "no end-to-end gate/query advantage is claimed",
            "a zero initial overlap with the target eigenspace prevents convergence to that eigenspace",
            "wide matrices target the zero eigenvalue of the right Gram unless the right kernel is excluded by an explicit promise",
        ],
    }
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Figure: exact target-mass and ideal postselection probability, two gap regimes.
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0), constrained_layout=True)
    for name, label in [("square_gap", "Separated minimum"), ("near_degenerate_minimum", "Near-degenerate minimum")]:
        rows = plot_rows[name]
        ts = [r["iterations"] for r in rows]
        axes[0].plot(ts, [r["cos_gram"]["target_mass"] for r in rows], marker="o", label=label)
        axes[1].semilogy(ts, [r["cos_gram"]["success_probability"] for r in rows], marker="o", label=label)
    axes[0].set(xlabel="Filter iterations t", ylabel="Minimum-eigenspace weight", ylim=(0, 1.02))
    axes[1].set(xlabel="Filter iterations t", ylabel="Ideal postselection probability")
    axes[0].grid(alpha=0.25)
    axes[1].grid(alpha=0.25, which="both")
    axes[0].legend(frameon=False)
    axes[1].legend(frameon=False)
    fig.suptitle(r"Right-Gram cosine filter $C=\cos(\beta G)$, $\beta=1.2$")
    fig.savefig(FIG, dpi=180)
    plt.close(fig)
    print(f"wrote {OUT}")
    print(f"wrote {FIG}")
    print(f"shot interval contains exact mean: {next(c['shot_readout']['interval_contains_mean'] for c in cases_out if c['shot_readout'] is not None)}")


if __name__ == "__main__":
    main()
