#!/usr/bin/env python3
"""Hold ideal filters fixed and sweep finite attempts through the bias floor."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import math
import numpy as np
import finite_sampling as fs
from selection_ising_application import hamiltonian
from selection_finite_budget import spectral_parameters

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT/'results/finite_budget.json'
    case = json.loads(source.read_text())['cases'][1]
    physical = json.loads((ROOT/'results/selection_ising_application.json').read_text())['cases'][1]
    n = 4; v = F(4, 5)
    values, vectors = np.linalg.eigh(hamiltonian(n, v))
    weights = np.abs(vectors.T@np.full(2**n, 1/math.sqrt(2**n)))**2
    scale = case['energy_scale']
    xs = (values-float(F(physical['audit']['lower_energy_bound'])))/scale
    target = float(xs[0]); E = float(F(case['prior']['mean_error']))
    names = ['budget-LP-1/8-4', 'original-optimized', 'budget-LP-1/32-10']
    rng = np.random.default_rng(20261101)
    curves = []
    for name in names:
        candidate = next(c for c in case['catalog'] if c['id'] == name)
        z, mu = spectral_parameters(candidate, xs, weights)
        rows = []
        for power in range(13):
            T = 10**power
            risk = fs.conditional_mse(T, z, mu, target)
            simulation = fs.simulate(T, z, mu, target, E, 20000, rng)
            simulation['mse_agreement_standard_errors'] = abs(simulation['conditional_mse_empirical']-risk)/simulation['conditional_mse_mc_se']
            rows.append({'attempts': T, 'conditional_mse': risk,
                         'energy_rmse': scale*math.sqrt(risk),
                         'abstention_probability': (1-z)**T,
                         'simulation': simulation})
        curves.append({'id': name, 'degree': candidate['degree'], 'success': z,
                       'energy_bias_floor': scale*(mu-target), 'rows': rows})
    out = {'metadata': {'seed': 20261101, 'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                         'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                         'replicates_per_setting': 20000, 'ideal_circuits': True},
           'spins': n, 'interaction_norm': str(v), 'energy_tolerance': physical['audit']['energy_tolerance'],
           'curves': curves}
    (ROOT/'results/finite_precision.json').write_text(json.dumps(out, indent=2, allow_nan=False)+'\n')
    print('PASS 39 ideal-filter finite-attempt settings, 780000 sampling replicates.')


if __name__ == '__main__':
    main()
