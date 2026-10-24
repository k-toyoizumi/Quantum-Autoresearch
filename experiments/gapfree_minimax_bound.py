"""Scalar minimax retention for gap-free filtered-mean bias; stdlib only.

Run:
  python experiments/gapfree_minimax_bound.py > results/gapfree_minimax_bound.json
  python -m py_compile experiments/gapfree_minimax_bound.py

The analytic inequalities are hand-derived in the companion memo. Grids here
are numerical consistency checks, not proof of continuous feasibility.
"""
from fractions import Fraction
import json, math, platform

ETA=Fraction("0.1")
L=Fraction("-0.05")
U=Fraction("0.05")
EMAX=Fraction("1.0")
BIAS_TARGETS=(Fraction("0.02"),Fraction("0.01"),Fraction("0.005"))
E0_GRID_N=101
D_GRID_N=1001
KAPPA=float((1-ETA)/ETA)


def scalar_F(x: float, b: float, eta: float) -> float:
    """F(x)=max_n n log(((x/n)-b)/A), restricted to positive rewards."""
    if x <= 0: return 0.0
    A=b*eta/(1-eta)
    delta0=b/(1-eta)
    best=0.0
    n=1
    while x/n > delta0:
        reward=n*math.log((x/n-b)/A)
        if reward>best: best=reward
        n+=1
    return best


def exact_chain(W: Fraction, b: Fraction, eta: Fraction):
    """Best equal-step chain. For fixed n, concavity makes equal steps best."""
    A=b*eta/(1-eta)
    delta0=b/(1-eta)
    best=Fraction(1)
    best_n=0
    n=1
    while W/n > delta0:
        ratio=(W/n-b)/A
        attempts=ratio**n
        if attempts>best:
            best,best_n=attempts,n
        n+=1
    step=W/best_n if best_n else None
    ratio=(step-b)/A if best_n else None
    return dict(steps=best_n,step=float(step) if step else None,
                per_step_relative_attenuation=float(1/ratio) if ratio else None,
                max_weight_upper_bound=float(1/best),
                pure_ground_expected_attempts_lower_numerator=best.numerator,
                pure_ground_expected_attempts_lower_denominator=best.denominator,
                log_attempt_lower=math.log(float(best)))


def lambert_rate(eta: float) -> float:
    """Solve r exp(r)=(1-eta)/(e eta) with bisection."""
    k=(1-eta)/eta
    target=k/math.e
    lo,hi=0.0,max(1.0,k)
    for _ in range(200):
        mid=(lo+hi)/2
        if mid*math.exp(mid)<target: lo=mid
        else: hi=mid
    return (lo+hi)/2


def additive_floor_counterexample(bias: float):
    eta=float(ETA); lo,hi=float(L),float(U); d=2*bias
    A=bias*eta/(1-eta)
    w0=math.exp(-scalar_F(hi-lo,bias,eta))
    w1=math.exp(-scalar_F(hi+d-lo,bias,eta))
    rows=[]
    for delta in (0.0,1e-8,1e-7,1e-6,1e-5,1e-4):
        v0=min(1.0,w0+delta); v1=min(1.0,w1+delta)
        ratio=v1/v0
        mean_bias=(1-eta)*v1*d/(eta*v0+(1-eta)*v1)
        rows.append(dict(absolute_weight_floor=delta,relative_weight_ratio=ratio,
          necessary_ratio_bound=A/(d-bias),filtered_mean_bias=mean_bias,
          certificate_passes=mean_bias<=bias+1e-14))
    return dict(target_ground_energy=hi,excited_distance=d,
      ground_weight_exact=w0,excited_weight_exact=w1,
      active_ratio_bound=A/(d-bias),rows=rows,
      caveat="additive weight floor is a stylized absolute-error perturbation, not a compiled QSP filter")


def grid_check(bias: float, rate: float):
    Lf,Uf,Ef=float(L),float(U),float(EMAX)
    eta=float(ETA); A=bias*eta/(1-eta)
    max_f_violation=-math.inf; max_exp_violation=-math.inf
    for i in range(E0_GRID_N):
        e0=Lf+(Uf-Lf)*i/(E0_GRID_N-1)
        dmax=Ef-e0
        for j in range(1,D_GRID_N+1):
            d=bias+(dmax-bias)*j/D_GRID_N
            if d<=bias: continue
            x=e0-Lf
            f_log_ratio=-scalar_F(x+d,bias,eta)+scalar_F(x,bias,eta)
            log_rhs=math.log(A/(d-bias))
            max_f_violation=max(max_f_violation,f_log_ratio-log_rhs)
            exp_log_ratio=-(rate/bias)*d
            max_exp_violation=max(max_exp_violation,exp_log_ratio-log_rhs)
    return dict(E0_points=E0_GRID_N,distance_points_per_E0=D_GRID_N,
       largest_log_constraint_violation_F_profile=max_f_violation,
       largest_log_constraint_violation_exponential=max_exp_violation)


def main():
    eta=float(ETA); W=float(U-L); r=lambert_rate(eta)
    chain=[]; profiles=[]
    for bq in BIAS_TARGETS:
        b=float(bq)
        cb=exact_chain(U-L,bq,ETA)
        cb.update(dict(bias_target=b,step_choice_for_previous_example=2*b/(1-eta),
                       previous_step_attempt_bound=(1/ (b*eta/((1-eta)*(2*b/(1-eta)-b))) )
                         ** math.floor(W/(2*b/(1-eta)) + 1e-12)))
        chain.append(cb)
        fw=scalar_F(W,b,eta)
        profiles.append(dict(bias_target=b,F_of_width=fw,
          F_profile_worst_bracket_transmission=math.exp(-fw),
          F_profile_attempt_proxy=math.exp(fw),
          lambert_r=r,exponential_slope_per_energy=r/b,
          exponential_worst_bracket_transmission=math.exp(-r*W/b),
          exponential_attempt_proxy=math.exp(r*W/b),
          log_gap_exponential_minus_F=r*W/b-fw,
          pairwise_grid_check=grid_check(b,r)))
    # A concrete near-tight pairwise-constraint check for b=0.01.
    perturb=additive_floor_counterexample(float(BIAS_TARGETS[1]))
    out=dict(metadata=dict(python=platform.python_version(),seed=None,deterministic=True,
      model=dict(eta_lower=float(ETA),ground_bracket=[float(L),float(U)],
        support_upper=float(EMAX),gap="unknown",filter_weight_bound="0 <= w <= 1",
        fixed_filter_independent_of_true_E0=True,loss="worst-case filtered spectral-mean bias"),
      warning="exact scalar-weight theorem ignores degree/query/depth/LCU costs; grid checks do not prove continuous feasibility"),
      finite_bracket_chain=chain,profile_and_exponential_comparison=profiles,
      additive_approximation_counterexample=perturb)
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
