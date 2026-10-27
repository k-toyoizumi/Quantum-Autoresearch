#!/usr/bin/env python3
"""Ideal circuits, finite total budget: prior-only selection and TFIM audits."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog
import filter_selection as design
import selection_certificates as cert
import finite_sampling as fs
from selection_ising_application import hamiltonian

ROOT = Path(__file__).resolve().parents[1]
BUDGETS = [100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]


def make_catalog(row):
    prior = row['design']['prior']
    a, u = F(prior['a']), F(prior['u'])
    catalog = []
    for index, record in enumerate(row['design']['certified_families']):
        catalog.append({'id': 'original-'+record['family'], 'family': record['family'],
                        'degree': record['degree_lambda'], 'bias': record['bias'],
                        'coefficients': record['chebyshev_coefficients'],
                        'certificate': record['certificate']})
    for fraction in [F(1, 32), F(1, 16), F(1, 8), F(1, 4), F(1, 2)]:
        bias = u*fraction
        for n in [1, 2, 3, 4, 5, 6, 8, 10, 12, 16]:
            c, info = design.solve(a, u, bias*F(49, 50), n)
            if info['grid_objective'] <= 1e-6:
                continue
            passed, _ = design.float_screen(c, a, u, bias)
            if not passed:
                continue
            certificate = cert.certify(c, a, u, bias*F(99, 100), F(19, 40))
            if not certificate['certified']:
                continue
            catalog.append({'id': f'budget-LP-{fraction}-{n}', 'family': 'optimized',
                            'degree': n, 'bias': str(bias), 'coefficients': list(map(str, c)),
                            'certificate': certificate})
    catalog.append({'id': 'unfiltered', 'family': 'unfiltered', 'degree': 0,
                    'bias': str(1-a), 'coefficients': ['1'],
                    'certificate': {'success_lower_exact': '1', 'global_normalization_exact': '1'}})
    return catalog


def select(catalog, u, prep, budget):
    best = {'id': 'prior-midpoint', 'degree': 0,
            'conditional_mse_upper_exact': str(u*u/4), 'conditional_mse_upper': float(u*u/4),
            'abstention_upper_exact': '0', 'abstention_upper': 0., 'attempts': 0}
    considered = []
    for candidate in catalog:
        T = budget//(prep+4*candidate['degree']+1)
        if T < 1:
            continue
        bounds = fs.certified_risk(T, F(candidate['certificate']['success_lower_exact']), u, F(candidate['bias']))
        feasible = F(bounds['abstention_upper_exact']) <= F(1, 20)
        record = {'id': candidate['id'], 'degree': candidate['degree'], 'attempts': T,
                  'coverage_requirement_met': feasible, **bounds}
        considered.append(record)
        if feasible and F(bounds['conditional_mse_upper_exact']) < F(best['conditional_mse_upper_exact']):
            best = record
    return best, considered


def spectral_parameters(candidate, eigenvalues, weights):
    if candidate['id'] == 'unfiltered':
        return 1., float(weights@eigenvalues)
    norm = F(candidate['certificate']['global_normalization_exact'])
    c = list(map(lambda value: float(F(value)), candidate['coefficients']))
    response = float(F(19, 40)/norm)*np.polynomial.chebyshev.chebval(2*eigenvalues-1, c)
    z = float(weights@response**2)
    mu = float((weights*response**2)@eigenvalues/z)
    return z, mu


def audit_candidate(candidate, T, xs, weights, E, scale, repeats, rng):
    e = float(xs[0])
    z, mu = spectral_parameters(candidate, xs, weights)
    risk = fs.conditional_mse(T, z, mu, e)
    zero = math.exp(T*math.log1p(-z)) if z < 1 else 0.
    simulation = fs.simulate(T, z, mu, e, E, repeats, rng)
    if simulation['conditional_mse_mc_se'] is not None:
        # Sampling fluctuation is tested as a diagnostic, not declared impossible.
        difference = abs(simulation['conditional_mse_empirical']-risk)
        simulation['mse_agreement_standard_errors'] = difference/max(1e-20, simulation['conditional_mse_mc_se'])
    return {'success': z, 'conditional_mean': mu, 'true_minimum': e,
            'ideal_conditional_mse': risk, 'ideal_energy_rmse': scale*math.sqrt(risk),
            'expected_accepted': T*z, 'abstention_probability': zero,
            'replacing_random_count_by_mean_mse': (mu-e)**2+mu*(1-mu)/(T*z),
            'failure_law': fs.failure_probability(T, z, mu, e, E), 'simulation': simulation}


def reduce_support(eigenvalues, weights, response_squared, a, T):
    """Finite LP counterpart of the three-energy reduction theorem."""
    x, p, w = map(np.asarray, [eigenvalues, weights, response_squared])
    e = x[0]; z = float(p@w); mu = float((p*w)@x/z)
    mandatory = a*w[0]
    moment = (x-mu)*w
    rhs = a*(mu-e)*w[0]/(1-a)
    rescale = max(float(np.max(np.abs(moment))), abs(rhs), 1e-16)
    result = linprog(w, A_eq=np.array([np.ones(len(x)), moment/rescale]),
                     b_eq=np.array([1, rhs/rescale]), bounds=(0, None), method='highs')
    assert result.success
    outside = result.x
    assert np.count_nonzero(outside > 1e-8) <= 2
    reduced = (1-a)*outside
    reduced[0] += a
    znew = float(reduced@w)
    munew = float((reduced*w)@x/znew)
    assert znew <= z+1e-9 and abs(munew-mu) < 1e-8
    original = fs.conditional_mse(T, z, mu, e)
    after = fs.conditional_mse(T, znew, munew, e)
    assert after >= original-1e-10
    used = np.flatnonzero(reduced > 1e-8)
    return {'target': e, 'mean_before': mu, 'mean_after': munew,
            'success_before': z, 'success_after': znew,
            'conditional_mse_before': original, 'conditional_mse_after': after,
            'support_count': len(used), 'energies': x[used].tolist(),
            'weights': reduced[used].tolist()}


def support_controls():
    rng = np.random.default_rng(20261030)
    rows = []
    for index in range(100):
        e = rng.uniform(0, .2)
        x = np.r_[e, e+(1-e)*np.sort(rng.uniform(1e-6, 1, 20))]
        a = .3; mass = rng.uniform(a, 1)
        p = np.r_[mass, (1-mass)*rng.dirichlet(np.ones(20))]
        w = (1-x)**8
        rows.append(reduce_support(x, p, w, a, [4, 16, 128, 4096][index % 4]))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pilot', action='store_true')
    parser.add_argument('--repeats', type=int, default=20000)
    args = parser.parse_args()
    inputs = ROOT/'results/selection_ising_application.json'
    physical = json.loads(inputs.read_text())['cases']
    if args.pilot:
        physical = physical[:1]
    output = ROOT/'results'/('finite_budget_pilot.json' if args.pilot else 'finite_budget.json')
    rows = []; rng = np.random.default_rng(20261031)
    for source in physical:
        started = time.monotonic()
        audit = source['audit']; prior = source['design']['prior']
        n, v = audit['spins'], F(source['parameters']['interaction_norm'])
        a, u, E = F(prior['a']), F(prior['u']), F(prior['mean_error'])
        catalog = make_catalog(source)
        # True spectra appear only in the audit, after catalog construction.
        values, vectors = np.linalg.eigh(hamiltonian(n, v))
        weights = np.abs(vectors.T@np.full(2**n, 1/math.sqrt(2**n)))**2
        scale = float(F(audit['energy_normalization']))
        xs = (values-float(F(audit['lower_energy_bound'])))/scale
        curves = []
        old = next(c for c in catalog if c['id'] == 'original-'+source['design']['selected']['family'])
        for budget in BUDGETS:
            selected, all_bounds = select(catalog, u, n, budget)
            T_old = budget//(n+4*old['degree']+1)
            old_audit = audit_candidate(old, T_old, xs, weights, float(E), scale, args.repeats, rng)
            if selected['id'] == 'prior-midpoint':
                actual = {'ideal_conditional_mse': (float(u)/2-xs[0])**2,
                          'ideal_energy_rmse': scale*abs(float(u)/2-xs[0]),
                          'abstention_probability': 0.,
                          'deterministic_failure': bool(abs(float(u)/2-xs[0]) > float(E))}
            else:
                chosen = next(c for c in catalog if c['id'] == selected['id'])
                actual = audit_candidate(chosen, selected['attempts'], xs, weights, float(E), scale, args.repeats, rng)
                assert actual['ideal_conditional_mse'] <= selected['conditional_mse_upper']*(1+1e-9)+1e-15
            curves.append({'budget': budget, 'selection': selected, 'candidate_bounds': all_bounds,
                           'selected_audit': actual, 'original_fixed_design_audit': old_audit})
        rows.append({'parameters': source['parameters'], 'prior': prior,
                     'energy_scale': scale, 'energy_tolerance': audit['energy_tolerance'],
                     'catalog': catalog, 'curves': curves, 'elapsed_seconds': time.monotonic()-started})
        source_names = ['finite_sampling.py', 'selection_finite_budget.py', 'filter_selection.py',
                        'selection_certificates.py', 'selection_ising_application.py']
        metadata = {'seed': 20261031, 'pilot': args.pilot, 'replicates_per_setting': args.repeats,
                    'input_sha256': hashlib.sha256(inputs.read_bytes()).hexdigest(),
                    'source_sha256': {p: hashlib.sha256((ROOT/'experiments'/p).read_bytes()).hexdigest() for p in source_names},
                    'circuits': 'ideal exact target polynomial; no gate noise or angle perturbation',
                    'budget': 'T=floor(B/(prep+4*degree+1)); readout reserved even on rejection',
                    'selection': 'minimum certified conditional-MSE upper bound, prior-only finite catalog; abstention<=0.05',
                    'scope': 'conditional risk and separately reported abstention; no unconditional quantum advantage'}
        payload = {'metadata': metadata, 'cases': rows, 'support_reduction_controls': support_controls()}
        output.write_text(json.dumps(payload, indent=2, allow_nan=False)+'\n')
        print(json.dumps({'spins': n, 'v': str(v), 'certified_candidates': len(catalog),
                          'selections': [r['selection']['id'] for r in curves],
                          'seconds': rows[-1]['elapsed_seconds']}), flush=True)


if __name__ == '__main__':
    main()
