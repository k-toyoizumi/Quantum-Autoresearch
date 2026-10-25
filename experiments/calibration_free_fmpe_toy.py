"""Small reduced-mixture screen of calibration-free phase moments.

This is a classical statistical toy, not a quantum circuit or a reproduction
of the full GDN spectrum/query model.  All N samples are retained on a full
circle; there is no window rejection.  See the companion research memo.
Run: python experiments/calibration_free_fmpe_toy.py > results/calibration_free_fmpe_toy.json
"""
from __future__ import annotations

import json
import math
import platform

import numpy as np
import scipy
from scipy.optimize import minimize, minimize_scalar

SEED = 20261025
N = 2000
REPLICATES = 20
SIGMA = 0.35
PHASE_BOUND = 0.8
TARGET_ERROR = 0.1
DELTA = 0.05
F = 0.3
A0 = 0.1
ALPHA = F * A0 / (F * A0 + 1.0 - F)


def wrapped_normal_pdf(x: np.ndarray, mu: float) -> np.ndarray:
    d = np.asarray(x) - mu
    shifts = np.arange(-3, 4)
    z = (d[..., None] + 2.0 * np.pi * shifts) / (SIGMA * math.sqrt(2.0))
    return np.exp(-(z * z)).sum(axis=-1) / (SIGMA * math.sqrt(2.0 * math.pi))


def draw_samples(rng: np.random.Generator, phase: float) -> np.ndarray:
    target = rng.random(N) < ALPHA
    x = np.empty(N)
    x[target] = phase + rng.normal(0.0, SIGMA, int(target.sum()))
    x[~target] = rng.uniform(-np.pi, np.pi, int((~target).sum()))
    return (x + np.pi) % (2.0 * np.pi) - np.pi


def negative_log_likelihood(x: np.ndarray, phase: float, alpha: float) -> float:
    density = (1.0 - alpha) / (2.0 * np.pi) + alpha * wrapped_normal_pdf(x, phase)
    return float(-np.log(np.maximum(density, 1e-300)).sum())


def oracle_alpha_mle(x: np.ndarray) -> tuple[float, bool]:
    fit = minimize_scalar(
        lambda phase: negative_log_likelihood(x, phase, ALPHA),
        bounds=(-PHASE_BOUND, PHASE_BOUND),
        method="bounded",
    )
    boundary = abs(fit.x) >= PHASE_BOUND - 1e-5
    return float(fit.x), bool(fit.success and not boundary)


def profile_mle(x: np.ndarray) -> tuple[float, float, bool]:
    first_moment = np.mean(np.exp(1j * x))
    phase0 = float(np.angle(first_moment))
    alpha0 = float(np.clip(abs(first_moment) / math.exp(-SIGMA**2 / 2.0), 0.005, 0.995))
    fit = minimize(
        lambda values: negative_log_likelihood(x, float(values[0]), float(values[1])),
        np.array([phase0, alpha0]),
        method="L-BFGS-B",
        bounds=[(-PHASE_BOUND, PHASE_BOUND), (1e-7, 1.0 - 1e-7)],
        options={"maxiter": 80, "ftol": 1e-11},
    )
    boundary = abs(fit.x[0]) >= PHASE_BOUND - 1e-5
    return float(fit.x[0]), float(fit.x[1]), bool(fit.success and not boundary)


def pilot_plugin(x: np.ndarray) -> tuple[float, float, bool]:
    pilot_n = N // 4
    pilot = x[:pilot_n]
    target = x[pilot_n:]
    first_moment = np.mean(np.exp(1j * pilot))
    alpha_hat = float(np.clip(abs(first_moment) / math.exp(-SIGMA**2 / 2.0), 1e-4, 0.9999))
    fit = minimize_scalar(
        lambda phase: negative_log_likelihood(target, phase, alpha_hat),
        bounds=(-PHASE_BOUND, PHASE_BOUND),
        method="bounded",
    )
    boundary = abs(fit.x) >= PHASE_BOUND - 1e-5
    return float(fit.x), alpha_hat, bool(fit.success and not boundary)


def zero_dc_ratio(x: np.ndarray) -> tuple[float | None, float, float, float | None, bool]:
    # h0=cos(x), h1=sin(x) both have zero uniform mean. Their population
    # ratio is tan(phi) for the reduced wrapped-normal-plus-uniform model.
    m0 = float(np.mean(np.cos(x)))
    m1 = float(np.mean(np.sin(x)))
    e = math.sqrt(math.log(4.0 / DELTA) / (2.0 * len(x)))
    if m0 <= e:
        return None, m0, m1, None, False
    phase_hat = math.atan(m1 / m0)
    ratio_bound = math.tan(PHASE_BOUND)
    half_width = e * (1.0 + ratio_bound) / m0
    return phase_hat, m0, m1, half_width, half_width <= TARGET_ERROR


def summarize(values: list[float], valid: list[bool], true_phase: float) -> dict[str, float | int | None]:
    arr = np.asarray(values, dtype=float)
    finite = np.isfinite(arr)
    mse = float(np.mean((arr[finite] - true_phase) ** 2)) if finite.any() else None
    ok = np.asarray(valid, dtype=bool) & finite
    failures = int(REPLICATES - ok.sum())
    # Replace each uncertified/nonconverged run by the maximum squared error
    # allowed by the declared phase interval; do not double-count its estimate.
    worst_case_risk = float(((arr[ok] - true_phase) ** 2).sum() + failures * (2 * PHASE_BOUND) ** 2) / REPLICATES
    return {"mse_when_estimate_returned": mse, "failure_count": failures,
            "failure_rate": failures / REPLICATES, "worst_case_risk_with_failure_penalty": worst_case_risk}


def run_case(rng: np.random.Generator, phase: float) -> dict:
    estimates = {"oracle_alpha_mle_proxy": [], "profile_mle": [], "pilot_plugin_mle": [], "zero_dc_ratio": []}
    valid = {key: [] for key in estimates}
    half_widths: list[float] = []
    cover_count = 0
    profile_alphas: list[float] = []
    pilot_alphas: list[float] = []
    for _ in range(REPLICATES):
        x = draw_samples(rng, phase)
        ph, ok = oracle_alpha_mle(x)
        estimates["oracle_alpha_mle_proxy"].append(ph)
        valid["oracle_alpha_mle_proxy"].append(ok)
        ph, alpha_hat, ok = profile_mle(x)
        estimates["profile_mle"].append(ph)
        profile_alphas.append(alpha_hat)
        valid["profile_mle"].append(ok)
        ph, alpha_hat, ok = pilot_plugin(x)
        estimates["pilot_plugin_mle"].append(ph)
        pilot_alphas.append(alpha_hat)
        valid["pilot_plugin_mle"].append(ok)
        ph, _, _, half_width, certified = zero_dc_ratio(x)
        estimates["zero_dc_ratio"].append(float("nan") if ph is None else ph)
        valid["zero_dc_ratio"].append(certified)
        if half_width is not None:
            half_widths.append(half_width)
            cover_count += int(abs(ph - phase) <= half_width)
    return {
        "true_phase": phase,
        "results": {name: summarize(values, valid[name], phase) for name, values in estimates.items()},
        "profile_alpha_mean": float(np.mean(profile_alphas)),
        "pilot_alpha_mean": float(np.mean(pilot_alphas)),
        "zero_dc_ci_available_count": len(half_widths),
        "zero_dc_ci_empirical_coverage_count": cover_count,
        "zero_dc_ci_half_width_median": float(np.median(half_widths)) if half_widths else None,
    }


def main() -> None:
    rng = np.random.default_rng(SEED)
    result = {
        "metadata": {
            "seed": SEED,
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "N_statistical_samples_per_run": N,
            "replicates_per_case": REPLICATES,
            "sigma": SIGMA,
            "F_original_parameter": F,
            "a0_original_parameter": A0,
            "alpha_reduced_mixture": ALPHA,
            "phase_bound": PHASE_BOUND,
            "confidence_delta": DELTA,
            "target_phase_error": TARGET_ERROR,
            "profile_mle_optimizer": "SciPy L-BFGS-B, maxiter=80, ftol=1e-11; moment initialization",
            "oracle_and_plugin_optimizer": "SciPy bounded scalar minimization on [-0.8,0.8]",
            "plugin_pilot_fraction": 0.25,
            "sampling_model": "full-circle reduced normalized mixture: alpha*wrapped_normal + (1-alpha)*uniform",
            "not_simulated": ["original GDN query/depth budget", "window rejection/discard counts", "quantum circuits", "physical gates"],
        },
        "cases": [run_case(rng, 0.0), run_case(rng, 0.2 * SIGMA)],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
