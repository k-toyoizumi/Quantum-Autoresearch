"""Small deterministic screens linking the scalar gap-free envelope to finite degree.
Stdlib only; run: python this_file.py > output.json
"""
from fractions import Fraction as Q
import json, math, platform

ETA=Q('0.1'); L=Q('-0.05'); U=Q('0.05'); EMAX=Q('1.0'); B=Q('0.01')
W=U-L; R=EMAX-L
A=B*ETA/(1-ETA); delta0=B/(1-ETA)

def F(x):
    xf=float(x); best=0.0; n=1
    while xf/n>float(delta0):
        best=max(best,n*math.log((xf/n-float(B))/float(A))); n+=1
    return best

def finite_difference_gate(degree):
    N=2*degree+1
    Delta=W/N
    if Delta<=B: return {'degree':degree,'N':N,'delta':float(Delta),'rho':None,'odd_sum':None,'impossible_by_gate':False,'reason':'delta <= b'}
    rho=A/(Delta-B)
    # O_N(rho)=sum odd binomial(N,k) rho^k, exact rational.
    O=sum(Q(math.comb(N,k))*rho**k for k in range(1,N+1,2))
    return {'degree':degree,'N':N,'delta':float(Delta),'rho':float(rho),'odd_sum_exact':str(O),'odd_sum':float(O),'impossible_by_gate':O<1,
      'meaning':'O_N(rho)<1 contradicts finite-difference identity, so no feasible polynomial of this degree'}

def shifted_power(n):
    S=R # global support endpoint; p(E)=(1-(E-L)/S)^n is bounded in [0,1]
    r=1.1010029972769728 # numeric bisection for W_0((1-eta)/(e eta))
    r_upper=1.102
    rhs=(1-float(ETA))/float(ETA)/math.e
    assert r_upper*math.exp(r_upper)>rhs # monotonicity certifies the root is below this safe bound
    required=math.ceil(float(S)*r_upper/(2*float(B)))
    return {'degree':n,'S':float(S),'amplitude':'p(x)=(1-x/S)^n, x=E-L','global_bound_on_support':'0<=p<=1',
      'lambert_root_numeric':r,'lambert_root_upper_bound_verified':r_upper,'upper_bound_equation_rhs':rhs,
      'sufficient_degree_for_continuous_bias_certificate':required,'passes_analytic_sufficient_condition':n>=required,
      'bracket_min_ground_transmission':float((1-float(W/S))**(2*n)),
      'max_time_oracle_cost':'not comparable: polynomial/block-encoding oracle; physical depth uncompiled'}

def bias(p, e0, e):
    w0=p(e0)**2; w1=p(e)**2; d=e-e0
    den=float(ETA)*w0+float(1-ETA)*w1
    return 0.0 if den==0 else float(1-ETA)*w1*d/den

def grid_profile(name,p,degree,l1):
    gcount=101; ecount=501
    maxbias=-1.; arg=None
    mintrans=float('inf')
    for i in range(gcount):
        e0=float(L)+(float(U-L))*i/(gcount-1)
        mintrans=min(mintrans,(p(e0)/l1)**2)
        for j in range(ecount):
            e=e0+(float(EMAX)-e0)*j/(ecount-1)
            val=bias(p,e0,e)
            if val>maxbias: maxbias=val;arg=(e0,e)
    return {'name':name,'degree':degree,'amplitude_scale':l1,'grid_max_bias_proxy':maxbias,'grid_argmax_E0_E':arg,
      'grid_min_bracket_transmission_after_amplitude_scale':mintrans,'grid_points':[gcount,ecount],
      'guarantee':'grid only; no continuous certificate'}

def main():
    # Use x=(E-L)/R, full physical support [0,1]. CTE cosine basis is a separate input oracle.
    Rf=float(R)
    cands=[]
    # Cosine-power amplitude cos^(2m)(pi*x/2) has Fourier degree m and nonnegative L1=1.
    for m in (2,4,6):
        def pfun(e,m=m): return math.cos(math.pi*(e-float(L))/(2*Rf))**(2*m)
        cands.append(grid_profile(f'cosine-power-amplitude-m{m}',pfun,m,1.0))
    # Coefficient-truncated prior-only Gaussian and exact scalar-envelope amplitude, cosine series via trapezoid.
    for label, fn in [('gaussian-endpoint-matched',lambda x: math.exp(-0.5*F(float(W))*(x/float(W))**2)),
                      ('scalar-envelope-amplitude',lambda x: math.exp(-0.5*F(x)) )]:
        M=6000; dx=Rf/M
        vals=[fn(Rf*i/M) for i in range(M+1)]
        for K in (2,4,6):
            coeff=[sum((0.5 if i in (0,M) else 1.0)*vals[i]*math.cos(k*math.pi*i/M) for i in range(M+1))*dx/Rf*(1 if k==0 else 2) for k in range(K+1)]
            def pfun(e,coeff=coeff):
                x=(e-float(L))/Rf
                return sum(a*math.cos(k*math.pi*x) for k,a in enumerate(coeff))
            cands.append(grid_profile(f'{label}-K{K}',pfun,K,sum(abs(v) for v in coeff)))
    # Polynomial impossibility lower bound and shifted-power analytic sufficient upper bound.
    gates=[finite_difference_gate(n) for n in (0,1,2,3,4,5,6)]
    powers=[shifted_power(n) for n in (2,4,6,57,58)]
    power_grids=[]
    for n in (2,4,6,57,58):
        def ppower(e,n=n): return max(0.0,1.0-(e-float(L))/float(R))**n
        power_grids.append(grid_profile(f'shifted-power-polynomial-n{n}',ppower,n,1.0))
    print(json.dumps({'metadata':{'python':platform.python_version(),'seed':None,'standard_library_only':True,
      'model':{'eta':float(ETA),'ground_bracket':[float(L),float(U)],'support':[float(L),float(EMAX)],'gap':'unknown','bias_target':float(B),
      'filter_weight':'w=|p|^2; candidate amplitude normalized by coefficient l1 for LCU success proxy',
      'finite_difference_gate_applies':'algebraic polynomial amplitudes only, not trigonometric polynomials'},
      'warning':'candidate grids are screening proxies, not continuous feasibility certificates; oracle depths across CTE/Fourier and polynomial block-encoding are not equated'},
      'scalar_unconstrained_optimum':{'F_W':F(W),'transmission':math.exp(-F(W))},
      'polynomial_finite_difference_gate':gates,'finite_degree_candidate_screens':cands,'shifted_power_analytic_baseline':powers,'shifted_power_grid_checks':power_grids},indent=2,sort_keys=True))
if __name__=='__main__':main()
