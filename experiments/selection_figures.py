#!/usr/bin/env python3
"""Generate the article's tables, figures and numerical summary from JSON."""
import json
import math
from fractions import Fraction as F
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from filter_selection import scalar_limit

ROOT=Path(__file__).resolve().parents[1]


def fracval(v):return float(F(v))


def main():
    data=json.loads((ROOT/'results/filter_selection.json').read_text())
    phase=json.loads((ROOT/'results/filter_selection_qsp.json').read_text())
    matrix=json.loads((ROOT/'results/filter_selection_matrix.json').read_text())
    cases=data['cases']; figdir=ROOT/'figures'
    paper=ROOT if (ROOT/'main.tex').exists() else ROOT/'paper/filter-selection'
    figdir.mkdir(exist_ok=True);paper.mkdir(parents=True,exist_ok=True)
    lines=[r'\begin{tabular}{rrrrrlrrr}',r'\toprule',
           r'$a$ & $u$ & $E$ & $c_\psi$ & $n$ & Response & $b$ & $J^{\rm up}$ & Gap \\',r'\midrule']
    for case in cases:
        p=case['prior'];s=case['selected'];family='LP' if s['family']=='optimized' else 'Cheb.'
        lines.append(f"{fracval(p['a']):.2f} & {fracval(p['u']):.3f} & {fracval(p['mean_error']):.3f} & {p['prep_cost']} & {s['degree_lambda']} & {family} & {fracval(s['bias']):.3f} & {s['cost_upper']:.3g} & {100*(case['selected_to_optimum_upper_ratio']-1):.1f}" + chr(92) + "% " + chr(92)*2)
    lines.extend([r'\bottomrule',r'\end{tabular}'])
    (paper/'generated-table.tex').write_text('\n'.join(lines)+'\n')

    fig,axes=plt.subplots(1,2,figsize=(10,3.7))
    for a in [F(3,10),F(3,5)]:
        for prep,style in [(1,'-o'),(32,'--s')]:
            group=[c for c in cases if F(c['prior']['a'])==a and c['prior']['prep_cost']==prep and F(c['prior']['mean_error'])==F(1,40)]
            axes[0].semilogy([fracval(c['prior']['u']) for c in group],
                             [c['selected']['cost_upper'] for c in group],style,label=f'a={float(a):g}, prep={prep}')
    axes[0].set(xlabel='Prior upper endpoint u',ylabel='Guaranteed expected query cost')
    axes[0].legend(fontsize=7)
    axes[1].bar(np.arange(len(cases)),[100*(c['selected_to_optimum_upper_ratio']-1) for c in cases],color='#2b758e')
    axes[1].set(xlabel='Table row',ylabel='Gap to certified optimum lower bound (%)',xticks=np.arange(len(cases)),xticklabels=np.arange(1,len(cases)+1))
    for ax in axes:ax.grid(alpha=.25,axis='y')
    fig.tight_layout();fig.savefig(figdir/'selection_costs.png',dpi=180);plt.close(fig)

    representative=[c for c in cases if c['prior']['a']=='3/5' and c['prior']['u']=='1/5']
    c1,c2=representative
    s1,s2=c1['selected'],c2['selected']
    fig,axes=plt.subplots(1,2,figsize=(10,3.7));x=np.linspace(0,1,1001)
    for c,style in [(c1,'-'),(c2,'--')]:
        s=c['selected'];raw=np.array([fracval(v) for v in s['chebyshev_coefficients']])
        response=np.polynomial.chebyshev.chebval(2*x-1,raw)/s['certificate']['global_normalization']
        axes[0].plot(x,response**2,style,label=f"selected n={s['degree_lambda']}")
    axes[0].axvspan(0,.2,alpha=.12,color='gray');axes[0].set(xlabel='Gram eigenvalue',ylabel='Unscaled transmission P(lambda)^2')
    axes[0].legend(fontsize=8)
    costs=np.linspace(0,64,257)
    for s in [s1,s2]:
        M=s['samples'];lo=fracval(s['certificate']['success_lower_exact']);hi=fracval(s['certificate']['success_upper_exact'])
        upper=M*((costs+4*s['degree_lambda'])/lo+1)
        lower=M*((costs+4*s['degree_lambda'])/hi+1)
        axes[1].plot(costs,upper,label=f"n={s['degree_lambda']}")
        axes[1].fill_between(costs,lower,upper,alpha=.15)
    axes[1].set(xlabel='Preparation cost',ylabel='Expected queries, certified intervals');axes[1].legend(fontsize=8)
    for ax in axes:ax.grid(alpha=.25)
    fig.tight_layout();fig.savefig(figdir/'selection_crossover.png',dpi=180);plt.close(fig)

    fig,ax=plt.subplots(figsize=(6.4,3.8))
    for a in [F(3,10),F(3,5)]:
        ratios=np.linspace(.01,15,301)
        bound=[scalar_limit(a,F(str(float(r))),F(1))['optimal_target_weight_upper'] for r in ratios]
        ax.semilogy(ratios,bound,label=f'unrestricted scalar, a={float(a):g}')
        group=[c for c in cases if F(c['prior']['a'])==a]
        xs=[fracval(c['prior']['u'])/fracval(c['selected']['bias']) for c in group]
        ys=[fracval(c['selected']['certificate']['target_amplitude_lower_exact'])**2 for c in group]
        for xx,yy,c in zip(xs,ys,group):
            bound=scalar_limit(a,F(c['prior']['u']),F(c['selected']['bias']))['optimal_target_weight_upper']
            assert yy<=bound*(1+1e-10)
        ax.scatter(xs,ys,s=24,marker='x')
    ax.set(xlabel='Prior width / bias allowance',ylabel='Worst target transmission (without kappa)')
    ax.grid(alpha=.25);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(figdir/'selection_prior_limit.png',dpi=180);plt.close(fig)

    # Two distinct certified polynomials, same sampling/bias allocation.
    assert s1['samples']==s2['samples'] and s1['bias']==s2['bias']
    p1=fracval(s1['certificate']['success_lower_exact']);p2=fracval(s2['certificate']['success_lower_exact'])
    cross=4*(s2['degree_lambda']*p1-s1['degree_lambda']*p2)/(p2-p1)
    l1=F(s1['certificate']['success_lower_exact']);h1=F(s1['certificate']['success_upper_exact'])
    l2=F(s2['certificate']['success_lower_exact']);h2=F(s2['certificate']['success_upper_exact'])
    left=4*(s2['degree_lambda']*l1-s1['degree_lambda']*h2)/(h2-l1)
    right=4*(s2['degree_lambda']*h1-s1['degree_lambda']*l2)/(l2-h1)
    assert l2>h1 and left<=right
    summary={'number_of_cases':len(cases),'nontrivial_prior_baseline':all(F(c['prior']['u'])>4*F(c['prior']['mean_error']) for c in cases),
             'maximum_optimality_factor':max(c['selected_to_optimum_upper_ratio'] for c in cases),
             'minimum_optimality_factor':min(c['selected_to_optimum_upper_ratio'] for c in cases),
             'selected_families':sorted(set(c['selected']['family'] for c in cases)),
             'phase_error_upper_max':max(c['phase_realization']['certificate']['uniform_amplitude_error_upper'] for c in phase['cases']),
             'phase_cost_inflation_max':max(c['phase_realization']['relative_cost_inflation_upper'] for c in phase['cases']),
             'matrix_response_error_max':max(c['matrix_response_error'] for c in matrix['cases']),
             'matrix_unitarity_error_max':max(c['unitarity_error'] for c in matrix['cases']),
             'scalar_heldout_instances':sum(c['held_out']['instances'] for c in cases),
             'scalar_confidence_failures':sum(c['held_out']['confidence_failures'] for c in cases),
             'matrix_sampling_replicates':sum(c['replicates'] for c in matrix['cases']),
             'matrix_confidence_failures':sum(c['confidence_failures'] for c in matrix['cases']),
             'crossover_example':{'a':.6,'u':.2,'E':.025,'bias':fracval(s1['bias']),
                                  'degree_low_prep':s1['degree_lambda'],'degree_high_prep':s2['degree_lambda'],
                                  'guaranteed_cost_crossover':cross,
                                  'true_candidate_crossover_enclosure':[float(left),float(right)],
                                  'true_candidate_crossover_enclosure_exact':[str(left),str(right)]}}
    (ROOT/'results/filter_selection_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
