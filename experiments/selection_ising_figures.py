#!/usr/bin/env python3
"""Plot and summarize the TFIM application without changing the main paper data."""
import json
from fractions import Fraction as F
import math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def main():
    data = json.loads((ROOT/'results/selection_ising_application.json').read_text())
    rows = data['cases']
    assert len(rows) == 6 and all('audit' in row for row in rows)
    labels = [f"N={row['audit']['spins']}\nv={row['parameters']['interaction_norm']}" for row in rows]
    x = np.arange(len(rows))
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    no_filter = [r['audit']['unfiltered_energy_bias']/r['audit']['energy_tolerance'] for r in rows]
    filtered = [r['audit']['selected_qsp_energy_bias']/r['audit']['energy_tolerance'] for r in rows]
    axes[0].bar(x-.18, no_filter, .36, label='Unfiltered product state')
    axes[0].bar(x+.18, filtered, .36, label='Selected QSP response')
    axes[0].axhline(1, color='black', ls='--', lw=1, label='Requested tolerance')
    axes[0].set_yscale('log'); axes[0].set_ylabel('Energy bias / tolerance')
    for k, family in enumerate(['optimized', 'power', 'chebyshev']):
        costs = [next((f['guaranteed_cost_upper'] for f in r['audit']['certified_family_audits']
                       if f['family'] == family), np.nan) for r in rows]
        axes[1].bar(x+(k-1)*.25, costs, .25, label=family)
    axes[1].set_yscale('log'); axes[1].set_ylabel('Guaranteed expected model cost')
    axes[2].bar(x, [100*(r['design']['selected_to_optimum_upper_ratio']-1) for r in rows])
    axes[2].set_ylabel('Gap to restricted lower bound (%)')
    for ax in axes:
        ax.set_xticks(x, labels, fontsize=8); ax.grid(axis='y', alpha=.2)
    axes[0].legend(fontsize=7); axes[1].legend(fontsize=8)
    fig.suptitle('Open transverse-field Ising chains; analytic priors; ideal normalized Hamiltonian signal')
    fig.tight_layout()
    fig.savefig(ROOT/'figures/selection_ising_application.png', dpi=170)
    summary = []
    for row in rows:
        audit, result = row['audit'], row['design']
        selected = result['selected']
        costs = {f['family']: f['guaranteed_cost_upper'] for f in audit['certified_family_audits']}
        success = F(selected['certificate']['success_lower_exact'])
        phase_error = F(audit['selected_qsp']['uniform_amplitude_error_upper_exact'])
        precision = 2**220
        sqrt_floor = F(math.isqrt(success.numerator*precision**2//success.denominator), precision)
        implemented_success = (sqrt_floor-phase_error)**2
        implemented_cost = selected['samples']*((audit['spins']+4*selected['degree_lambda'])/implemented_success+1)
        summary.append({'spins': audit['spins'], 'v': row['parameters']['interaction_norm'],
            'tolerance': audit['energy_tolerance'], 'initial_bias': audit['unfiltered_energy_bias'],
            'filtered_bias': audit['selected_qsp_energy_bias'],
            'family': selected['family'], 'degree': selected['degree_lambda'],
            'cost_upper': selected['cost_upper'],
            'power_cost_ratio': costs['power']/selected['cost_upper'] if 'power' in costs else None,
            'chebyshev_cost_ratio': costs['chebyshev']/selected['cost_upper'] if 'chebyshev' in costs else None,
            'restricted_optimality_factor': result['selected_to_optimum_upper_ratio'],
            'phase_realized_cost_upper_exact': str(implemented_cost),
            'phase_realized_cost_upper': float(implemented_cost),
            'phase_realized_cost_inflation_upper': float(implemented_cost/F(selected['cost_upper_exact'])),
            'phase_error_upper': audit['selected_qsp']['uniform_amplitude_error_upper'],
            'confidence_failures': audit['sampling_confidence_failures']})
    (ROOT/'results/selection_ising_summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False)+'\n')
    for r in summary:
        power_ratio = f"{r['power_cost_ratio']:.3f}" if r['power_cost_ratio'] is not None else 'uncertified'
        print(f"{r['spins']} | {r['v']} | {r['tolerance']:.6g} | {r['initial_bias']:.6g} | "
              f"{r['filtered_bias']:.6g} | {r['degree']} | {r['cost_upper']:.5g} | "
              f"{power_ratio} | {r['chebyshev_cost_ratio']:.3f} | "
              f"{r['restricted_optimality_factor']:.6f}")


if __name__ == '__main__':
    main()
