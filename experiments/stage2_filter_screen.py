"""Deterministic coarse filter screening; standard library only. Run from repo root."""
import itertools, json, math, platform

CENTER, W, GAP, ETA, EMAX = 0.0, 0.05, 0.50, 0.10, 1.0
TAU, D, EPS, DELTA, PREP = math.pi, 20.0, 0.30, 0.05, 1.0
E0_GRID = [-W, -W/2, 0.0, W/2, W]
TAIL_N = 51
H_GRID = [0.1, 0.3, 0.5, 0.8, 1.0]
STEP_UNITS, MAX_K = 4, 2  # coefficient step 1/4; includes cos^2 baseline

# c=(c0,c1,...,cK), symmetric Fourier coefficients c_{-k}=c_k; response is real.
def response(c, x): return c[0] + 2*sum(c[k]*math.cos(k*TAU*x) for k in range(1,len(c)))
def wgt(c,x): return response(c,x)**2
def candidates():
    out=[]; U=STEP_UNITS
    for K in range(MAX_K+1):
        for rest in itertools.product(range(U+1),repeat=K):
            if 2*sum(rest)>U: continue
            out.append(tuple([float(U-2*sum(rest))/U]+[v/U for v in rest]))
    return out

def prior(c, tail_n):
    # Exact two-point extremal expression, but only gridded in E0 and excited E.
    worst=0.; zlo=math.inf; arg=None
    for e0 in E0_GRID:
        wg=wgt(c,e0); zlo=min(zlo,ETA*wg)
        lo=e0+GAP
        for j in range(tail_n):
            e=lo+(EMAX-lo)*j/(tail_n-1); we=wgt(c,e)
            den=ETA*wg+(1-ETA)*we
            b=(1-ETA)*we*(e-e0)/den if den else 0.
            if b>worst: worst,arg=b,(e0,e)
    return worst,zlo,arg

def ac(c):
    a={}
    for j,cj in enumerate(c):
        for k,ck in enumerate(c):
            d=j-k; a[d]=a.get(d,0.)+cj*ck
            if j: 
                d=-j-k; a[d]=a.get(d,0.)+cj*ck
            if k:
                d=j+k; a[d]=a.get(d,0.)+cj*ck
            if j and k:
                d=-j+k; a[d]=a.get(d,0.)+cj*ck
    return a

def evalc(c,h,tail_n=TAIL_N):
    K=len(c)-1; b,z,arg=prior(c,tail_n); fd=h*h*EMAX**3/6; es=EPS-b-fd
    if es<=0 or z<=0: return None
    l1=c[0]+2*sum(abs(x) for x in c[1:]); ph=z/(l1*l1)
    n=math.ceil(2*math.log(2/DELTA)/(h*h*es*es))
    dphys=K*TAU+h
    cphys=(n/ph)*(PREP+K*TAU)+n*h
    a=ac(c); B=sum(abs(x) for x in a.values())
    err=es*h*z/(2+es*h); nv=math.ceil(2*B*B/(err*err)*math.log(4/DELTA))
    tnum=sum(abs(v)*abs(h+d*TAU) for d,v in a.items())/B
    tden=sum(abs(v)*abs(d*TAU) for d,v in a.items())/B
    dvirt=h+2*K*TAU; cvirt=nv*(2*PREP+tnum+tden)
    if max(dphys,dvirt)>D:return None
    return dict(K=K,h=h,bias_proxy=b,fd_bias_bound=fd,eps_stat=es,z_lower=z,
      herald_lower=ph,L1=l1,B=B,physical_accepted_shots=n,physical_attempt_proxy=n/ph,
      physical_depth_proxy=dphys,physical_cost_proxy=cphys,virtual_shots_each=nv,
      virtual_depth_proxy=dvirt,virtual_cost_proxy=cvirt,bias_arg=arg)

def main():
    cs=candidates()
    for m in range(4):
        cs.append(tuple(math.comb(2*m,m+k)/(4**m) for k in range(m+1)))
    # Deduplicate coefficient vectors while preserving deterministic order.
    cs=list(dict.fromkeys(cs)); outcomes=[]
    for c in cs:
        for h in H_GRID:
            r=evalc(c,h)
            if r: outcomes.append((r['physical_cost_proxy'],c,r))
    best=min(outcomes,key=lambda x:x[0]) if outcomes else None
    # Fixed baselines and validation only; no validation spectrum enters selection.
    val={"left":((-0.04,.46,.72,1.),(.10,.45,.25,.20)),
         "right":((.04,.54,.82,1.),(.10,.30,.30,.30)),
         "two_level":((-.05,.45),(.10,.90)),
         "symmetric_gap_counterexample":((-.05,.05),(.10,.90))}
    rows=[]
    choices=[('nofilter',(1.,),0.5)]
    if best: choices.append(('screen_best',best[1],best[2]['h']))
    for name,c,h in choices:
        r=evalc(c,h,201) or {}
        r.update(name=name,coefficients=list(c))
        for case,(es,ps) in val.items():
            ws=[wgt(c,e) for e in es]; z=sum(p*v for p,v in zip(ps,ws))
            mean=sum(p*v*e for p,v,e in zip(ps,ws,es))/z
            r[case+'_filtered_mean_bias']=mean-min(es); r[case+'_z']=z
        rows.append(r)
    result=dict(metadata=dict(python=platform.python_version(),seed=None,deterministic=True,
      coefficient_grid_step=1/STEP_UNITS,candidate_count=len(cs),h_grid=H_GRID,
      design_grid=dict(e0_points=len(E0_GRID),tail_points=TAIL_N),validation_bias_grid=dict(e0_points=len(E0_GRID),tail_points=201),
      prior=dict(center=CENTER,bracket_half_width=W,gap_lower=GAP,eta_lower=ETA,Emax=EMAX,tau=TAU),
      objective=dict(epsilon=EPS,delta=DELTA,depth_cap_query_time_proxy=D,state_prep_cost_proxy=PREP),
      limitations=['gridded supremum is a screening proxy, not a certified interval bound',
       'depth is ideal controlled-evolution-time proxy, not physical gate depth',
       'finite-difference estimator estimates filtered mean, not a standalone ground-energy estimator',
       'true validation spectra are post-hoc only; coefficients use priors only',
       'C_prior and concrete Hamiltonian simulation costs are omitted']),
      best_physical_cost=(dict(coefficients=list(best[1]),**best[2]) if best else None),results=rows)
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__': main()
