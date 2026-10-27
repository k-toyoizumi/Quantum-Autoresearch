#!/usr/bin/env python3
"""Prior-only, depth-limited filter selection with rational certificates.

No true minimum, gap, or held-out spectral weights enter the design.
Oracle accounting: even polynomial P(s^2), degree 2n in singular value s;
serial controlled U/U† extraction costs 4n signal calls, readout costs 1.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import platform
import subprocess
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import scipy
from numpy.polynomial import Chebyshev as Ch, Polynomial as Po
from numpy.polynomial.chebyshev import chebvander, chebval
from scipy.optimize import linprog
from scipy.special import lambertw

import selection_certificates as cert

ROOT=Path(__file__).resolve().parents[1]
KAPPA=F(19,20)
DELTA=.05


def log_upper(x, terms=100):
    z=(x-1)/(x+1)
    return 2*sum((z**(2*k+1)/(2*k+1) for k in range(terms)),F(0))+2*z**(2*terms+1)/((2*terms+1)*(1-z*z))


LN40_UPPER=log_upper(F(5))+3*log_upper(F(2))


def base_revision():
    try:
        return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
    except (OSError,subprocess.CalledProcessError):
        return None  # Source archives have no .git; source hashes still identify code.


def basis(x,n):return chebvander(2*np.asarray(x)-1,n)


def solve(a,u,bias,n,rounds=3):
    # Dyadic/rational nodes permit exact reconstruction of active dual rows.
    es=[u*F(i,16) for i in range(17)] if u else [F(0)]
    xs=[F(i,64) for i in range(65)]
    ss=[F(i,128) for i in range(129)]
    ve=basis(list(map(float,es)),n);vx=basis(list(map(float,xs)),n)
    rows=[];rhs=[];meta=[]
    for x,v in zip(ss,basis(list(map(float,ss)),n)):
        for sign in [1,-1]:rows.append(np.r_[sign*v,0]);rhs.append(1);meta.append(('support',x,sign))
    for e,v in zip(es,ve):rows.append(np.r_[-v,1]);rhs.append(0);meta.append(('target',e))
    for sign in [1,-1]:rows.append(np.r_[np.full(n+1,sign),0]);rhs.append(0);meta.append(('endpoint',sign))
    for i,e in enumerate(es):
        for j,x in enumerate(xs):
            if x-e<=bias:continue
            q=float(cert.sqrt_upper(a*bias/((1-a)*(x-e-bias))))
            for sign in [1,-1]:
                rows.append(np.r_[sign*vx[j]-q*ve[i],0]);rhs.append(0);meta.append(('pair',e,x,sign))
    objective=np.r_[np.zeros(n+1),-1]
    history=[]
    for iteration in range(rounds+1):
        result=linprog(objective,A_ub=np.asarray(rows),b_ub=np.asarray(rhs),
                       bounds=[(-1,1)]+[(-2,2)]*n+[(0,1)],method='highs',
                       options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
        if not result.success:raise RuntimeError(result.message)
        history.append(float(result.x[-1]))
        if iteration==rounds:break
        ed=[u*F(i,64) for i in range(65)] if u else [F(0)]
        xd=[F(i,512) for i in range(513)]
        ved=basis(list(map(float,ed)),n);vxd=basis(list(map(float,xd)),n)
        pe=ved@result.x[:-1];px=vxd@result.x[:-1]
        distance=np.array(list(map(float,xd)))[:,None]-np.array(list(map(float,ed)))[None,:]-float(bias)
        q=np.sqrt(float(a*bias/(1-a))/np.maximum(distance,1e-100))
        score=np.abs(px[:,None])-q*pe[None,:]
        score[distance<=0]=-np.inf
        indices=np.argpartition(score.ravel(),-6)[-6:]
        added=0
        for flat in indices:
            j,i=np.unravel_index(flat,score.shape)
            if score[j,i]<=1e-10:continue
            e,x=ed[i],xd[j];sign=1 if px[j]>=0 else -1
            qq=float(cert.sqrt_upper(a*bias/((1-a)*(x-e-bias))))
            rows.append(np.r_[sign*vxd[j]-qq*ved[i],0]);rhs.append(0);meta.append(('pair',e,x,sign));added+=1
        for j in np.argsort(np.abs(px))[-3:]:
            if abs(px[j])<=1+1e-10:continue
            sign=1 if px[j]>=0 else -1
            rows.append(np.r_[sign*vxd[j],0]);rhs.append(1);meta.append(('support',xd[j],sign));added+=1
        for i in np.argsort(pe-result.x[-1])[:2]:
            if pe[i]>=result.x[-1]-1e-10:continue
            rows.append(np.r_[-ved[i],1]);rhs.append(0);meta.append(('target',ed[i]));added+=1
        if not added:break
    c=[F(str(float(x))) for x in result.x[:-1]]
    # Enforce P(1)=0 exactly in the saved-decimal interpretation.
    c[0]=-sum(c[1:])
    dual=cert.grid_dual_upper(result,meta,a,u,bias,n)
    return c,{'grid_objective':float(result.x[-1]),'rows':len(rows),'dual':dual,'exchange_objectives':history}


def samples(total_error,bias):
    if float(bias)>=float(total_error):return None
    return cert.ceil(LN40_UPPER/(2*(total_error-bias)**2))


def cost(n,success,M,prep):return M*((prep+4*n)/success+1)


def float_screen(c,a,u,bias):
    """Discard obviously infeasible baselines; never used as a certificate."""
    e=np.linspace(0,float(u),41)
    x=np.linspace(0,1,1201)
    pe=chebval(2*e-1,np.array(c,float));px=chebval(2*x-1,np.array(c,float))
    denom=float(a)*pe[None,:]**2+(1-float(a))*px[:,None]**2
    vals=np.divide((1-float(a))*(x[:,None]-e[None,:])*px[:,None]**2,
                   denom,out=np.zeros_like(denom),where=denom>1e-250)
    return float(vals.max())<=float(bias)*.999999, float(np.min(pe)**2)


def baseline_coefficients(n):
    """All candidates have P(1)=0; degree refers to lambda, not s."""
    out=[]
    power=Po([1,-1])**n
    out.append(('power',None,power.convert(kind=Ch,domain=[0,1],window=[-1,1]).coef))
    if n%2==0:
        quartic=Po([1,0,-1])**(n//2)
        out.append(('quartic_power',None,quartic.convert(kind=Ch,domain=[0,1],window=[-1,1]).coef))
    if n>=2:
        # Classical endpoint Chebyshev low-pass, followed by 1-lambda nulling.
        for cutoff in [.04,.08,.16,.28,.42,.60,.78]:
            arg=Po([-(1+cutoff)/(1-cutoff),2/(1-cutoff)])
            C=Ch.basis(n-1).convert(kind=Po)(arg)/float(Ch.basis(n-1)(arg(0)))
            p=C*Po([1,-1])
            out.append(('chebyshev',cutoff,p.convert(kind=Ch,domain=[0,1],window=[-1,1]).coef))
        # Degree-two cosine Taylor step, composed once before QSP synthesis.
        if n%2==1:
            p=(Po([1,0,-.72])**((n-1)//2))*Po([1,-1])
            c=p.convert(kind=Ch,domain=[0,1],window=[-1,1]).coef
            out.append(('cosine_taylor',1.2,np.pad(c,(0,n+1-len(c)))))
    return out


def rational_coeff(c):
    c=[F(str(float(v))) for v in c]
    c[0]=-sum(c[1:])
    return c


def scalar_limit(a,u,b):
    A=a*b/(1-a);best=F(1);winner=0
    for n in range(1,int(u/(b+A))+1):
        step=u/n
        if step>b+A:
            candidate=((step-b)/A)**n
            if candidate>best:best=candidate;winner=n
    return {'optimal_target_weight_upper_exact':str(1/best),
            'optimal_target_weight_upper':float(1/best),'restart_lower':float(best),
            'chain_length':winner,
            'asymptotic_rate':float(lambertw(float((1-a)/a)/math.e).real)}


def run_case(a,u,E,N,prep,allocations=(F(2,5),F(3,5),F(4,5))):
    started=time.monotonic(); designs=[];baselines=[];relaxations=[]
    for fraction in allocations:
        b=E*fraction;M=samples(E,b)
        # The design bias has slack; the exact dual solves the evaluation bias.
        for n in range(1,N+1):
            for family,param,raw in baseline_coefficients(n):
                cb=rational_coeff(raw)
                ok,tau2b=float_screen(cb,a,u,b*F(99,100))
                if ok and tau2b>1e-12:
                    baselines.append({'family':family,'parameter':param,'degree_lambda':n,
                                      'bias':str(b),'samples':M,
                                      'chebyshev_coefficients':list(map(str,cb)),
                                      'screen_cost':cost(n,float(a)*float(KAPPA)**2*tau2b,M,prep)})
            _,relax=solve(a,u,b,n)
            upper=float(min(F(1),F(relax['dual']['upper_exact'])))
            if upper>0:
                lower_exact=M*((prep+4*n)/(a*KAPPA**2*min(F(1),F(relax['dual']['upper_exact']))**2)+1)
                lower=float(lower_exact)
                relaxations.append({'degree_lambda':n,'bias':str(b),'certificate_cost_lower':lower,
                                    'certificate_cost_lower_exact':str(lower_exact),
                                    'grid_dual':relax['dual']})
            c,info=solve(a,u,b*F(49,50),n)
            if info['grid_objective']<1e-5:continue
            passed,tau2=float_screen(c,a,u,b)
            if not passed:continue
            optimistic=cost(n,float(a)*float(KAPPA)**2*tau2,M,prep)
            designs.append({'family':'optimized','degree_lambda':n,'bias':str(b),'samples':M,
                            'chebyshev_coefficients':list(map(str,c)),
                            'screen_cost':optimistic,'design_lp':info})
    # Candidates are ranked with prior-only grids, but reported choices must
    # pass exact continuous certification. Retain the best in each family.
    certified=[]
    for family in ['optimized','power','quartic_power','chebyshev','cosine_taylor']:
        pool=sorted([r for r in designs+baselines if r['family']==family],key=lambda r:r['screen_cost'])
        best=None
        for candidate in pool[:12]:
            c=list(map(F,candidate['chebyshev_coefficients']));b=F(candidate['bias'])
            certificate=cert.certify(c,a,u,b*F(99,100),KAPPA)
            if not certificate['certified']:continue
            upper=cost(candidate['degree_lambda'],certificate['success_lower'],candidate['samples'],prep)
            upper_exact=candidate['samples']*((prep+4*candidate['degree_lambda'])/F(certificate['success_lower_exact'])+1)
            record={**candidate,'certificate':certificate,'cost_upper':float(upper_exact),'cost_upper_exact':str(upper_exact),
                    'polynomial_bias_certificate':str(b*F(99,100)),
                    'implementation_bias_reserve':str(b*F(1,100)),
                    'oracle_queries_per_attempt':4*candidate['degree_lambda'],
                    'maximum_filter_and_readout_queries':4*candidate['degree_lambda']+1}
            if best is None or upper<best['cost_upper']:best=record
            # A slightly looser interval enclosure is permitted; the first
            # certified choice is used rather than claiming a catalogue optimum.
            if upper<=candidate['screen_cost']*1.03:break
        if best:certified.append(best)
    if not certified:
        return {'prior':{'a':str(a),'u':str(u),'mean_error':str(E),'maximum_degree_lambda':N,'prep_cost':prep},
                'status':'no certified feasible candidate','elapsed_seconds':time.monotonic()-started}
    best=min(certified,key=lambda r:r['cost_upper'])
    lower=min(r['certificate_cost_lower'] for r in relaxations)
    return {'prior':{'a':str(a),'u':str(u),'mean_error':str(E),'maximum_degree_lambda':N,
                     'maximum_filter_readout_queries':4*N+1,'maximum_total_serial_queries':prep+4*N+1,
                     'prep_cost':prep,'kappa':str(KAPPA)},
            'allocation_grid':list(map(str,allocations)),
            'selected':best,'certified_families':certified,
            'grid_allocation_optimum_cost_lower':lower,
            'selected_to_optimum_upper_ratio':best['cost_upper']/lower,
            'degree_allocation_dual_bounds':relaxations,
            'scalar_limit_at_selected_bias':scalar_limit(a,u,F(best['bias'])),
            'elapsed_seconds':time.monotonic()-started}


def held_out(case,seed=20261027):
    """Selection is already fixed. Validate on new minima and many-level inputs."""
    rng=np.random.default_rng(seed);s=case['selected'];a=F(case['prior']['a']);u=F(case['prior']['u'])
    c=np.array([float(F(v)) for v in s['chebyshev_coefficients']])
    c*=float(KAPPA)/s['certificate']['global_normalization']
    b=float(F(s['bias']));E=float(F(case['prior']['mean_error']));M=s['samples']
    failures=0;max_bias=0.;worst_success=1.;sample_rows=[]
    for trial in range(100):
        target=float(u)*rng.random();mass=float(a)+(1-float(a))*rng.random()
        lam=np.r_[target,target+(1-target)*rng.uniform(.000001,1,15)]
        p=np.r_[mass,(1-mass)*rng.dirichlet(np.ones(15))]
        response=chebval(2*lam-1,c);z=float(p@response**2)
        mu=float((p*response**2)@lam/z);bias=mu-target
        assert bias<=b+1e-10 and z>=s['certificate']['success_lower']-1e-12
        readout=rng.binomial(M,mu)/M
        failures+=abs(readout-target)>E
        max_bias=max(max_bias,bias);worst_success=min(worst_success,z)
        if trial<4:sample_rows.append({'target':target,'a_actual':mass,'mu':mu,'readout':readout,
                                       'success':z,'expected_attempts':M/z})
    return {'seed':seed,'instances':100,'confidence_failures':int(failures),
            'maximum_bias':max_bias,'minimum_success':worst_success,'examples':sample_rows,
            'draw_model':'aggregate independent accepted Bernoulli draws; no quantum hardware'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pilot',action='store_true')
    parser.add_argument('--output',default='results/filter_selection.json')
    args=parser.parse_args()
    if args.pilot:
        parameters=[(F(3,5),F(1,4),F(1,20),12,1),(F(3,5),F(1,4),F(1,20),12,32)]
    else:
        parameters=[(a,u,F(1,40),20,prep) for a in [F(3,10),F(3,5)]
                    for u in [F(1,8),F(1,5)] for prep in [1,32]]
        parameters += [(F(3,5),u,F(1,20),12,1) for u in [F(1,4),F(2,5)]]
    results=[]
    for a,u,E,N,prep in parameters:
        # Neither the Gram midpoint nor the singular-value midpoint already
        # meets the requested accuracy; otherwise no quantum work is needed.
        assert u>4*E
        case=run_case(a,u,E,N,prep)
        if 'selected' in case:case['held_out']=held_out(case)
        results.append(case)
        # Incremental results survive interruption.
        out={'metadata':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
                         'base_commit':base_revision(),
                         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                         'verifier_sha256':hashlib.sha256(Path(cert.__file__).read_bytes()).hexdigest(),
                         'oracle_model':'P(s^2); degree 2n in s; serial Hermitian extraction 4n signal calls; readout 1',
                         'error_metric':'normalized Gram minimum additive error; singular error at most sqrt(error)',
                         'confidence_delta':DELTA,'pilot':args.pilot,
                         'optimality_scope':'real endpoint-nulling polynomial class; finite bias-allocation grid; exact dual bounds'},
             'cases':results}
        Path(args.output).parent.mkdir(parents=True,exist_ok=True)
        Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
        print(json.dumps({'prior':case['prior'],'status':case.get('status','certified'),
                          'winner':case.get('selected',{}).get('family'),
                          'cost':case.get('selected',{}).get('cost_upper'),
                          'optimality_ratio':case.get('selected_to_optimum_upper_ratio'),
                          'seconds':case['elapsed_seconds']}),flush=True)


if __name__=='__main__':main()
