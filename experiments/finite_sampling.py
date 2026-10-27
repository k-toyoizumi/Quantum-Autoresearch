#!/usr/bin/env python3
"""Finite-attempt Bernoulli thinning, exact rational risk bounds, numeric audits.

Binomial inverse moments are classical; the implementation separates numerical
law evaluation from outward-rational uniform selection bounds.
"""
from fractions import Fraction as F
import math
import numpy as np
from scipy.stats import binom

BITS = 180
SCALE = 2**BITS
GL_X, GL_W = np.polynomial.legendre.leggauss(128)


def power_enclosure(base, exponent):
    """Directed fixed-point interval for rational base**integer exponent."""
    assert 0 <= base <= 1 and exponent >= 0
    floor = lambda x: x.numerator//x.denominator
    ceil = lambda x: -((-x.numerator)//x.denominator)
    lo, hi = floor(base*SCALE), ceil(base*SCALE)
    outlo = outhi = SCALE
    def multiply(a, b, c, d):
        return a*c//SCALE, -((-b*d)//SCALE)
    while exponent:
        if exponent & 1:
            outlo, outhi = multiply(outlo, outhi, lo, hi)
        exponent //= 2
        if exponent:
            lo, hi = multiply(lo, hi, lo, hi)
    return F(outlo, SCALE), F(outhi, SCALE)


def certified_inverse_bound(attempts, success):
    """Bound h=E[1/M | M>0] using classical shifted-inverse moments.

    1/m <= 1/(m+1)+3/((m+1)(m+2)) for m>=1.
    The m=0 correction is 5/2 times its probability.
    """
    T, z = attempts, F(success)
    assert T >= 1 and 0 < z <= 1
    qlo, qhi = power_enclosure(1-z, T)
    nextlo, _ = power_enclosure(1-z, T+1)
    coverage_lower = 1-qhi
    if coverage_lower <= 0:
        return F(1), qhi
    A = (1-nextlo)/((T+1)*z)
    B = (1-(1+(T+1)*z)*nextlo)/((T+1)*(T+2)*z*z)
    upper = (A+3*B-F(5, 2)*qlo)/coverage_lower
    assert upper >= 0
    return min(F(1), upper), qhi


def inverse_positive_binomial(T, success):
    """Numerical integral evaluation of the exact inverse-binomial moment.

    Quadrature is for audits only; certified decisions use the function above.
    The transformed large-mean integral is truncated at 48.
    """
    z = np.asarray(success, dtype=float)
    scalar = z.ndim == 0
    z = np.atleast_1d(z)
    assert T >= 1 and np.all((z > 0) & (z <= 1))
    result = np.empty_like(z)
    exact = z == 1
    result[exact] = 1/T
    for low_mean in [True, False]:
        mask = (~exact) & ((T*z <= 50) if low_mean else (T*z > 50))
        zz = z[mask]
        if not len(zz):
            continue
        logq = np.log1p(-zz)
        zero = np.exp(T*logq)
        coverage = -np.expm1(T*logq)
        if low_mean:
            t = (GL_X+1)/2
            exponent = T*np.log1p(-zz[:, None]*(1-t))
            delta = exponent-T*logq[:, None]
            integrand = np.empty_like(exponent)
            stable = zero >= 1e-12
            integrand[stable] = zero[stable, None]*np.expm1(delta[stable])/t
            integrand[~stable] = (np.exp(exponent[~stable])-zero[~stable, None])/t
            H = integrand@GL_W/2
        else:
            v = (GL_X+1)*24
            mean = T*zz
            integrand = (np.exp(T*np.log1p(-v/T))[None, :]-zero[:, None])/(1-v/mean[:, None])
            H = (integrand@GL_W)*24/mean
        result[mask] = H/coverage
    return float(result[0]) if scalar else result


def conditional_mse(T, z, mu, target):
    return (mu-target)**2+mu*(1-mu)*inverse_positive_binomial(T, z)


def certified_risk(T, success_lower, u, bias):
    h, abstention = certified_inverse_bound(T, success_lower)
    endpoint = min(F(1, 2), F(u)+F(bias))
    variance = endpoint*(1-endpoint)
    risk = F(bias)**2+variance*h
    return {'conditional_mse_upper_exact': str(risk), 'conditional_mse_upper': float(risk),
            'abstention_upper_exact': str(abstention), 'abstention_upper': float(abstention),
            'inverse_binomial_upper_exact': str(h)}


def failure_probability(T, z, mu, target, tolerance, omitted=1e-12):
    """Numerical exact-binomial mixture; omitted mass bounds truncation error."""
    lower = max(1, int(binom.ppf(omitted/2, T, z)))
    upper = min(T, int(binom.isf(omitted/2, T, z)))
    m = np.arange(lower, upper+1)
    probabilities = binom.pmf(m, T, z)
    lower_threshold = np.ceil(m*(target-tolerance)).astype(np.int64)-1
    upper_threshold = np.floor(m*(target+tolerance)).astype(np.int64)
    tails = binom.cdf(lower_threshold, m, mu)+binom.sf(upper_threshold, m, mu)
    zero = math.exp(T*math.log1p(-z)) if z < 1 else 0.
    omitted_mass = max(0., 1-zero-float(probabilities.sum()))
    fail = zero+float(probabilities@tails)
    return {'failure_probability_lower_numeric': fail,
            'failure_probability_upper_numeric': min(1., fail+omitted_mass),
            'omitted_probability_numeric': omitted_mass,
            'binomial_terms': len(m)}


def simulate(T, z, mu, target, tolerance, repeats, rng):
    accepted = rng.binomial(T, z, repeats)
    ones = rng.binomial(accepted, mu)
    available = accepted > 0
    estimates = ones[available]/accepted[available]
    squared = (estimates-target)**2
    failures = (~available).sum()+np.sum(abs(estimates-target) > tolerance)
    return {'replicates': repeats, 'accepted_count_mean': float(accepted.mean()),
            'zero_success_fraction': float(np.mean(~available)),
            'conditional_mse_empirical': float(squared.mean()) if len(squared) else None,
            'conditional_mse_mc_se': float(squared.std(ddof=1)/math.sqrt(len(squared))) if len(squared)>1 else None,
            'failure_fraction': float(failures/repeats)}
