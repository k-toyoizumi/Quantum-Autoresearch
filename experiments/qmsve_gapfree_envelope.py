#!/usr/bin/env python3
"""Scalar audit of sharp gap-free bias envelopes; no quantum circuit simulation.

The supremum is evaluated by a unique stationary-point equation, independently
checked against dense grids, many-level mixtures, and asymptotic constants.
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
import subprocess
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.optimize import brentq
from scipy.special import lambertw

ROOT = Path(__file__).resolve().parents[1]
BETA = 1.2
SEED = 20261027
METHODS = {"cos_gram": 2, "cos_dilation": 1,
           "polynomial_gram": 2, "polynomial_direct": 1}


def log_response(x, method):
    x = np.asarray(x, dtype=float)
    c = BETA**2 / 2
    if method == "cos_gram":
        # log1p avoids loss of significance close to the right kernel.
        return np.log1p(-2 * np.sin(BETA * x / 2)**2)
    if method == "cos_dilation":
        return np.log1p(-2 * np.sin(BETA * np.sqrt(x) / 2)**2)
    return np.log1p(-c * x ** METHODS[method])


def neg_log_derivative(x, method):
    c = BETA**2 / 2
    if method == "cos_gram":
        return BETA * math.tan(BETA * x)
    if method == "cos_dilation":
        return c if x == 0 else BETA * math.tan(BETA * math.sqrt(x)) / (2 * math.sqrt(x))
    k = METHODS[method]
    return c * k * x ** (k - 1) / (1 - c * x**k)


def two_point(a, target, excited, t, method):
    log_r = 2 * t * float(log_response(excited, method) - log_response(target, method))
    r = math.exp(log_r)
    relative_success = a + (1 - a) * r
    return ((excited - target) * (1 - a) * r / relative_success,
            2 * t * float(log_response(target, method)) + math.log(relative_success))


def envelope(a, target, t, method):
    def stationary(d):
        r = math.exp(2 * t * float(log_response(target + d, method) - log_response(target, method)))
        return 2 * t * d * neg_log_derivative(target + d, method) - 1 - (1 - a) * r / a
    upper = 1 - target
    d = upper if stationary(upper) <= 0 else brentq(stationary, 0, upper, xtol=1e-15)
    bias, log_success = two_point(a, target, target + d, t, method)
    return {"bias": bias, "excited_lambda": target + d,
            "log_success": log_success, "success": math.exp(log_success)}


def constant(a, k):
    # The transcendental stationary equation and Lambert W are separate checks.
    y = brentq(lambda y: k * y - 1 - (1 - a) / a * math.exp(-y), 1 / k, 100)
    y_w = 1 / k + float(lambertw((1 - a) / (k * a) * math.exp(-1 / k)).real)
    assert abs(y - y_w) < 1e-12
    return y ** (1 / k) / (1 + a / (1 - a) * math.exp(y))


def main():
    rng = np.random.default_rng(SEED)
    random_checks = []
    for method, k in METHODS.items():
        max_violation = 0.0
        max_grid_excess = 0.0
        for _ in range(250):
            a = float(rng.uniform(.02, .98))
            target = float(rng.uniform(0, .85))
            t = int(rng.integers(1, 4097))
            xs = np.r_[target, target + (1-target)*rng.uniform(1e-10, 1, size=12)]
            ps = np.r_[a, (1-a)*rng.dirichlet(np.ones(12))]
            ratios = np.exp(2*t*(log_response(xs, method)-log_response(target, method)))
            bias = float(np.dot(ps*ratios, xs-target) / np.dot(ps, ratios))
            env = envelope(a, target, t, method)["bias"]
            upper = constant(a, k)/(t*BETA**2)**(1/k)
            max_violation = max(max_violation, bias-env, env-upper)
            grid = np.linspace(target, 1, 20001)
            rr = np.exp(2*t*(log_response(grid, method)-log_response(target, method)))
            grid_bias = (grid-target)*(1-a)*rr/(a+(1-a)*rr)
            max_grid_excess = max(max_grid_excess, float(grid_bias.max())-env)
        assert max_violation < 2e-12 and max_grid_excess < 2e-12
        random_checks.append({"method": method, "mixtures": 250,
                              "max_bound_violation": max_violation,
                              "max_grid_excess_over_stationary_maximum": max_grid_excess})

    rows = []
    for a in [.1, .4, .9]:
        for method, k in METHODS.items():
            c = constant(a, k)
            for t in [4, 16, 64, 256, 1024, 4096, 16384, 65536]:
                row = envelope(a, 0, t, method)
                bound = c/(t*BETA**2)**(1/k)
                row.update(a=a, target=0, method=method, iterations=t,
                           uniform_upper_bound=bound, ratio_to_asymptotic= row["bias"]/bound,
                           normalized_sigma_error=math.sqrt(row["bias"]))
                rows.append(row)
    assert all(.999 < r["ratio_to_asymptotic"] <= 1+1e-10
               for r in rows if r["iterations"] == 65536)

    # Identical posteriors, radically different success: global Taylor margin.
    delta = BETA**4/math.factorial(4)
    margins = []
    for t in [8, 64, 128, 1024]:
        row = envelope(.4, 0, t, "polynomial_gram")
        factor = (1+delta)**(-2*t)
        margins.append({"iterations": t, "delta": delta,
                        "zero_preserving_success": row["success"],
                        "global_margin_success": row["success"]*factor,
                        "success_ratio": factor})

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for method in METHODS:
        group = [r for r in rows if r["a"] == .4 and r["method"] == method]
        ts = [r["iterations"] for r in group]
        axes[0].loglog(ts, [r["bias"] for r in group], marker=".", label=method.replace("_", " "))
        axes[1].semilogx(ts, [r["ratio_to_asymptotic"] for r in group], marker=".")
    axes[0].set(xlabel="Scalar iterations t", ylabel="Exact worst-case Gram-mean bias")
    axes[1].set(xlabel="Scalar iterations t", ylabel="Exact bias / asymptotically sharp upper bound")
    for ax in axes:
        ax.grid(alpha=.25)
    axes[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(ROOT/"figures/qmsve_gapfree_envelope.png", dpi=180)
    plt.close(fig)
    result = {
        "metadata": {"base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                     "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     "python": platform.python_version(), "numpy": np.__version__,
                     "scipy": scipy.__version__, "matplotlib": matplotlib.__version__,
                     "beta": BETA, "seed": SEED,
                     "scope": "Scalar exact-response audit. No QSVT synthesis or query advantage."},
        "verification": random_checks, "kernel_boundary_envelopes": rows,
        "global_margin_penalty": margins,
    }
    out = ROOT/"results/qmsve_gapfree_envelope.json"
    out.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"verification": random_checks, "margin_penalty": margins,
                      "a_point4_constants": {str(k): constant(.4,k) for k in [1,2]}}, indent=2))


if __name__ == "__main__":
    main()
