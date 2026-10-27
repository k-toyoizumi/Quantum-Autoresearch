#!/usr/bin/env python3
"""Publication figures and a machine-readable finite-sampling audit summary."""
import json
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def main():
    budget = json.loads((ROOT/'results/finite_budget.json').read_text())
    precision = json.loads((ROOT/'results/finite_precision.json').read_text())
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    all_se = []; all_simulations = []
    for curve in precision['curves']:
        rows = curve['rows']; T = np.array([r['attempts'] for r in rows])
        rmse = np.array([r['energy_rmse'] for r in rows])
        label = f"degree {curve['degree']}"
        line, = axes[0].loglog(T, rmse, label=label)
        empirical = [r['energy_rmse']*math.sqrt(r['simulation']['conditional_mse_empirical']/r['conditional_mse']) for r in rows]
        axes[0].scatter(T, empirical, s=13, marker='x', color=line.get_color())
        axes[0].axhline(curve['energy_bias_floor'], color=line.get_color(), ls=':', lw=1)
        axes[1].semilogx(T, [r['abstention_probability'] for r in rows], label=label)
        for r in rows:
            all_simulations.append(r['simulation'])
            all_se.append(r['simulation']['mse_agreement_standard_errors'])
    axes[0].axhline(precision['energy_tolerance'], color='black', ls='--', lw=1, label='target tolerance')
    axes[0].set(xlabel='Whole-filter attempts T', ylabel='Energy RMSE, conditional on an output')
    axes[1].set(xlabel='Whole-filter attempts T', ylabel='Probability of no output', xlim=(1, 1e4))
    for ax in axes:
        ax.legend(fontsize=8); ax.grid(alpha=.2)
    fig.suptitle('Ideal circuits, finite samples: four-spin TFIM, v=0.8')
    fig.tight_layout(); fig.savefig(ROOT/'figures/finite_precision.png', dpi=180); plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.1))
    representative = budget['cases'][1]
    curves = representative['curves']; B = [r['budget'] for r in curves]
    scale = representative['energy_scale']
    axes[0].loglog(B, [scale*math.sqrt(r['selection']['conditional_mse_upper']) for r in curves], 'k--', label='Selected uniform RMSE bound')
    axes[0].loglog(B, [r['selected_audit']['ideal_energy_rmse'] for r in curves], 'o-', label='Selected: actual TFIM law')
    axes[0].loglog(B, [r['original_fixed_design_audit']['ideal_energy_rmse'] for r in curves], 's-', label='Original fixed degree: actual law')
    axes[0].axhline(representative['energy_tolerance'], color='grey', ls=':', label='Target tolerance')
    axes[0].set(xlabel='Reserved total query budget B', ylabel='Energy RMSE, conditional on an output')
    axes[0].legend(fontsize=7); axes[0].grid(alpha=.2)
    degrees = np.array([[r['selection']['degree'] for r in c['curves']] for c in budget['cases']])
    axes[1].imshow(degrees, aspect='auto', cmap='Blues', vmin=0, vmax=max(10, degrees.max()))
    axes[1].set_xticks(range(len(B)), [f'$10^{int(math.log10(b))}$' for b in B])
    axes[1].set_yticks(range(6), [f"N={c['parameters']['spins']}, v={c['parameters']['interaction_norm']}" for c in budget['cases']], fontsize=8)
    for i in range(6):
        for j in range(len(B)):
            axes[1].text(j, i, 'prior' if degrees[i, j] == 0 else str(degrees[i, j]),
                         ha='center', va='center', fontsize=8,
                         color='white' if degrees[i, j] >= 7 else 'black')
    axes[1].set(xlabel='Reserved total query budget B', title='Selected degree; prior means no quantum work')
    fig.tight_layout(); fig.savefig(ROOT/'figures/finite_budget.png', dpi=180); plt.close(fig)
    selections = []
    for case in budget['cases']:
        for row in case['curves']:
            selections.append(row['selection'])
            for name in ['selected_audit', 'original_fixed_design_audit']:
                a = row[name]
                if 'simulation' in a:
                    all_simulations.append(a['simulation'])
                    all_se.append(a['simulation']['mse_agreement_standard_errors'])
    support = budget['support_reduction_controls']
    summary = {'physical_cases': 6, 'budget_conditions': len(selections),
        'candidate_counts': [len(c['catalog']) for c in budget['cases']],
        'precision_sweep_conditions': sum(len(c['rows']) for c in precision['curves']),
        'sampling_settings': len(all_simulations),
        'sampling_replicates': sum(r['replicates'] for r in all_simulations),
        'maximum_mse_discrepancy_in_mc_standard_errors': max(all_se),
        'prior_only_selections': sum(r['id'] == 'prior-midpoint' for r in selections),
        'support_reduction_controls': len(support),
        'maximum_reduced_support': max(r['support_count'] for r in support),
        'maximum_support_risk_inflation': max(r['conditional_mse_after']/r['conditional_mse_before'] for r in support),
        'precision_bias_floors': {str(c['degree']): c['energy_bias_floor'] for c in precision['curves']},
        'representative_original_degree': 7,
        'representative_rows': [{'budget': r['budget'], 'selected_id': r['selection']['id'],
            'selected_degree': r['selection']['degree'],
            'original_energy_rmse': r['original_fixed_design_audit']['ideal_energy_rmse'],
            'original_abstention': r['original_fixed_design_audit']['abstention_probability'],
            'original_tolerance_failure_lower_numeric': r['original_fixed_design_audit']['failure_law']['failure_probability_lower_numeric'],
            'selected_energy_rmse': r['selected_audit']['ideal_energy_rmse']} for r in curves]}
    (ROOT/'results/finite_sampling_summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
