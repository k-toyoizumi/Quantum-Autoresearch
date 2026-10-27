#!/usr/bin/env python3
"""Small TFIM application: analytic priors, prior-only design, spectral/QSP audit.

The Hamiltonian signal is an ideal normalized Hermitian block encoding.
Physical gate synthesis, classical superiority and scaling advantage are not claimed.
"""
import argparse
import contextlib
from fractions import Fraction as F
import hashlib
import io
import json
import math
from pathlib import Path

import numpy as np
from pyqsp.sym_qsp_opt import newton_solver
import filter_selection as design
import selection_certificates as cert
import selection_qsp as qsp

ROOT = Path(__file__).resolve().parents[1]
SAFETY = F(19, 20)


def prior(n, interaction_norm):
    v = interaction_norm
    # H0=-sum X, V=-J sum ZZ, psi=|+>^n. In the orthogonal block,
    # H>=-n+2-v, and ||QV psi||^2=(n-1)J^2=v^2/(n-1).
    t2 = v*v/(n-1)
    shift = t2/(2-v)
    a = 1/(1+t2/(2-v)**2)
    lower, upper, radius = -n-shift, F(-n), n+v
    scale = radius-lower
    u = shift/scale
    return a, u, u/8, lower, upper, scale


def hamiltonian(n, v):
    size = 2**n
    indices = np.arange(size)
    spins = 1-2*((indices[:, None] >> np.arange(n)) & 1)
    diagonal = -float(v/(n-1))*np.sum(spins[:, :-1]*spins[:, 1:], axis=1)
    H = np.diag(diagonal)
    for site in range(n):
        H[indices, indices ^ (1 << site)] -= 1
    return H


def general_phase_bound(phases, target):
    """Enclose Im U00(2x-1)-target(x), all x in [0,1]."""
    coefficients = qsp.qsp_coefficients(phases)
    lo, hi = [F(0)]*len(coefficients), [F(0)]*len(coefficients)
    for j, value in enumerate(coefficients):
        left, right = (F(endpoint, qsp.S) for endpoint in value[1])
        for k in range(j+1):
            factor = F(math.comb(j, k)*2**k*(-1)**(j-k))
            lo[k] += factor*(left if factor >= 0 else right)
            hi[k] += factor*(right if factor >= 0 else left)
    size = max(len(lo), len(target))
    lo += [F(0)]*(size-len(lo)); hi += [F(0)]*(size-len(hi))
    for k, value in enumerate(target):
        lo[k] -= value; hi[k] -= value
    bounds = (tuple(math.floor(x*qsp.S) for x in cert.bernstein(lo)),
              tuple(cert.ceil(x*qsp.S) for x in cert.bernstein(hi)))
    low, high = cert.range_bound(bounds, 8)
    return max(abs(low), abs(high))


def realize(record, xs):
    """Separate even/odd QSP then average their extracted responses.

    P(x)=F(2x-1), F=Fe+Fo. Each part is bounded by one on [-1,1].
    Each QSP block implements safety*part, and averaging costs one factor 1/2.
    Serial controlled extraction uses at most 4*n signal calls.
    """
    c = list(map(F, record['chebyshev_coefficients']))
    norm = F(record['certificate']['global_normalization_exact'])
    grid = np.linspace(-1, 1, 1025)
    points = np.r_[2*xs-1, grid]
    response = np.zeros(len(points))
    error, degree_sum, protocols = F(0), 0, []
    for parity in [0, 1]:
        part = [value if k % 2 == parity else F(0) for k, value in enumerate(c)]
        while part and part[-1] == 0:
            part.pop()
        if not part:
            continue
        reduced = np.array([float(SAFETY*value/norm) for value in part[parity::2]])
        with contextlib.redirect_stdout(io.StringIO()):
            _, residual, iterations, protocol = newton_solver(reduced, parity, crit=1e-14, maxiter=100)
        assert residual < 1e-11
        phases = [F(str(float(p))) for p in protocol.full_phases]
        values = qsp.signal_response(points, list(map(float, phases)))[:, 0, 0].imag
        response += values/2
        target = [SAFETY*p/norm for p in cert.cheb_power(part)]
        eta = general_phase_bound(phases, target)
        error += eta/2
        degree_sum += len(phases)-1
        protocols.append({'parity': parity, 'phases_exact': list(map(str, phases)),
                          'solver_residual': float(residual), 'iterations': iterations,
                          'uniform_error_upper_exact': str(eta)})
    target = float(SAFETY/2/norm)*np.polynomial.chebyshev.chebval(points, list(map(float, c)))
    numeric_error = float(np.max(np.abs(response-target)))
    reserve = F(record['implementation_bias_reserve'])
    success = F(record['certificate']['success_lower_exact'])
    assert 4*error**2 <= reserve**2*success
    assert 2*degree_sum <= 4*record['degree_lambda']
    return response[:len(xs)], {'protocols': protocols,
        'uniform_amplitude_error_upper_exact': str(error),
        'uniform_amplitude_error_upper': float(error), 'grid_error': numeric_error,
        'serial_signal_queries': 2*degree_sum,
        'accounted_signal_queries': 4*record['degree_lambda'],
        'implementation_reserve_certified': True}


def audit(n, v, physical, case):
    lower, upper, scale = physical
    # Only after design is fixed do we compute the true spectrum and overlaps.
    H = hamiltonian(n, v)
    eigenvalues, vectors = np.linalg.eigh(H)
    psi = np.ones(2**n)/math.sqrt(2**n)
    weights = np.abs(vectors.T@psi)**2
    xs = (eigenvalues-float(lower))/float(scale)
    a, u = F(case['prior']['a']), F(case['prior']['u'])
    assert 0 <= xs[0] <= float(u)+1e-12 and xs[-1] <= 1+1e-12
    assert weights[0]+1e-12 >= float(a)
    tolerance = float(scale*F(case['prior']['mean_error']))
    families = []
    for record in case['certified_families']:
        c = np.array(list(map(lambda x: float(F(x)), record['chebyshev_coefficients'])))
        response = float(SAFETY/2)*np.polynomial.chebyshev.chebval(2*xs-1, c)/record['certificate']['global_normalization']
        success = float(weights@response**2)
        mean = float((weights*response**2)@eigenvalues/success)
        assert mean-eigenvalues[0] <= float(scale*F(record['bias']))+1e-10
        actual_cost = record['samples']*((n+4*record['degree_lambda'])/success+1)
        families.append({'family': record['family'], 'degree': record['degree_lambda'],
                         'bias_allocation': record['bias'], 'success': success,
                         'energy_bias': mean-eigenvalues[0], 'samples': record['samples'],
                         'audited_expected_cost': actual_cost,
                         'guaranteed_cost_upper': record['cost_upper']})
    response, phase = realize(case['selected'], xs)
    success = float(weights@response**2)
    mean = float((weights*response**2)@eigenvalues/success)
    M = case['selected']['samples']
    rng = np.random.default_rng(20261029+n+int(100*v))
    normalized_mean = (mean-float(lower))/float(scale)
    energies = float(lower)+float(scale)*rng.binomial(M, normalized_mean, 200)/M
    no_filter_bias = -n-eigenvalues[0]
    return {'spins': n, 'J': str(v/(n-1)), 'h': 1, 'boundary': 'open',
            'lower_energy_bound': str(lower), 'upper_energy_bound': str(upper),
            'energy_normalization': str(scale), 'energy_tolerance': tolerance,
            'prior_midpoint_error_bound': float((upper-lower)/2),
            'exact_energy': float(eigenvalues[0]), 'exact_ground_overlap': float(weights[0]),
            'unfiltered_product_state_energy': -n, 'unfiltered_energy_bias': float(no_filter_bias),
            'unfiltered_meets_target': bool(no_filter_bias <= tolerance),
            'certified_family_audits': families, 'selected_qsp': phase,
            'selected_qsp_success': success, 'selected_qsp_energy_bias': mean-eigenvalues[0],
            'sampling_replicates': 200,
            'sampling_confidence_failures': int(np.sum(abs(energies-eigenvalues[0]) > tolerance))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pilot', action='store_true')
    args = parser.parse_args()
    # Reuse the same optimizer with the parity-combination success margin.
    # Do not change the original paper's immutable design/results.
    design.KAPPA = SAFETY/2
    rows = []
    parameters = [(4, F(4, 5))] if args.pilot else [(n, v) for n in [4, 6, 8] for v in [F(2, 5), F(4, 5)]]
    output = ROOT/'results'/('selection_ising_pilot.json' if args.pilot else 'selection_ising_application.json')
    for n, v in parameters:
        a, u, E, lower, upper, scale = prior(n, v)
        assert (upper-lower)/2 > scale*E
        case = design.run_case(a, u, E, 16, n)
        row = {'parameters': {'spins': n, 'interaction_norm': str(v)}, 'design': case}
        if 'selected' in case:
            row['audit'] = audit(n, v, (lower, upper, scale), case)
        rows.append(row)
        sources = ['selection_ising_application.py', 'filter_selection.py', 'selection_certificates.py', 'selection_qsp.py']
        metadata = {'seed_base': 20261029, 'pilot': args.pilot,
                    'source_sha256': {s: hashlib.sha256((ROOT/'experiments'/s).read_bytes()).hexdigest() for s in sources},
                    'signal': 'ideal block encoding of Y=2*(H-LI)/(R-L)-I',
                    'success_amplitude_scale': str(SAFETY/2),
                    'scope': 'small TFIM application; analytic priors; continuous polynomial/phase certificates; no physical gate compilation'}
        output.write_text(json.dumps({'metadata': metadata, 'cases': rows}, indent=2)+'\n')
        print(json.dumps({'spins': n, 'v': str(v), 'status': case.get('status', 'certified'),
                          'family': case.get('selected', {}).get('family'),
                          'ratio': case.get('selected_to_optimum_upper_ratio'),
                          'seconds': case['elapsed_seconds']}), flush=True)


if __name__ == '__main__':
    main()
