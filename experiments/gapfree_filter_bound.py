"""Gap-free, bracket-uncertain single-filter bias/success tradeoff toy.
Standard library only; run: python experiments/gapfree_filter_bound.py > results/gapfree_filter_bound.json
The grid is diagnostic only, not a continuous certificate.
"""
import json, math, platform
from fractions import Fraction

ETA=0.1; L=-0.05; U=0.05; EMAX=1.0
BIAS_TARGETS=(0.02,0.01,0.005)
E0_N=201; TAIL_N=1001

# Analytic chain from two-level adversarial instances.
def chain(b):
    Delta=2*b/(1-ETA)
    eta_q=Fraction(str(ETA)); rho_q=eta_q/(1+eta_q)
    rho=float(rho_q)
    m=math.floor((U-L)/Delta+1e-12)
    attempts=(1/rho_q)**m
    return dict(bias_target=b,step_Delta=Delta,relative_weight_ratio=rho,
               chain_steps=m,normalized_filter_weight_at_chain_endpoint_upper=float(rho_q**m),
               pure_ground_expected_herald_attempts_lower=attempts.numerator)

def cos_power(m,x): return math.cos(math.pi*x/2)**(2*m)
def w(m,x): return cos_power(m,x)**2

def grid_bias(m):
    best=(0.0,None)
    for i in range(E0_N):
        e0=L+(U-L)*i/(E0_N-1); wg=w(m,e0)
        for j in range(TAIL_N):
            e=e0+(EMAX-e0)*j/(TAIL_N-1); we=w(m,e)
            den=ETA*wg+(1-ETA)*we
            b=(1-ETA)*we*(e-e0)/den if den else 0.0
            if b>best[0]: best=(b,(e0,e))
    return best

def main():
    powers=[]
    for m in range(13):
        bias,arg=grid_bias(m)
        min_w=min(w(m,L+(U-L)*i/(E0_N-1)) for i in range(E0_N))
        wsym0=w(m,L); wsym1=w(m,U)
        sym_bias=((1-ETA)*wsym1*(U-L)/(ETA*wsym0+(1-ETA)*wsym1)
                  if ETA*wsym0+(1-ETA)*wsym1 else None)
        powers.append(dict(m=m,f_degree=m,ideal_max_evolution_time=m*math.pi,
           gridded_worst_mean_bias=bias,bias_arg=arg,
           endpoint_symmetric_two_level_bias=sym_bias,
           min_ground_filter_weight_on_bracket=min_w,
           pure_ground_worstcase_attempts_proxy=(1/min_w if min_w else None)))
    out=dict(metadata=dict(python=platform.python_version(),seed=None,deterministic=True,
       assumptions=dict(eta_lower=ETA,ground_bracket=[L,U],support=[L,EMAX],gap="unknown",
          all_E0_in_bracket_are_admissible=True,filter_bounded_by_one=True,
          each_E0_may_have_its_own_adversarial_two_level_instance=True),
       grids=dict(E0_points=E0_N,excited_energy_points_per_E0=TAIL_N),
       warning="gridded bias values are diagnostic, not continuous guarantees; time degree is not compiled depth"),
       chain_bounds=[chain(b) for b in BIAS_TARGETS],cosine_power_screen=powers)
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
