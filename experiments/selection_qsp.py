#!/usr/bin/env python3
"""Synthesize whole even polynomials, then certify saved decimal phases.

Symmetric-QSP Im(U_00) convention and extraction adapt the earlier project
audit at local commit 4c8fb96. This verifier additionally encloses all sin/cos
evaluations and polynomial recurrences by exact rational / integer intervals.
"""
import contextlib
import hashlib
import importlib.metadata
import io
import json
import math
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from pyqsp.sym_qsp_opt import newton_solver
import selection_certificates as cert

ROOT=Path(__file__).resolve().parents[1]
S=cert.S
ZERO=(0,0)


def ip(x):return ((x*S).__floor__(),cert.ceil(x*S))
def ia(x,y):return x[0]+y[0],x[1]+y[1]
def ine(x):return -x[1],-x[0]
def im(x,y):
    p=[a*b for a in x for b in y]
    return min(p)//S,-((-max(p))//S)
def ca(x,y):return ia(x[0],y[0]),ia(x[1],y[1])
def cn(x):return ine(x[0]),ine(x[1])
def cm(x,y):return ia(im(x[0],y[0]),ine(im(x[1],y[1]))),ia(im(x[0],y[1]),im(x[1],y[0]))
CZ=(ZERO,ZERO)


def trigonometric(phi):
    m=8
    while abs(phi)**(2*m+2)/math.factorial(2*m+2)>F(1,2**280):m+=4
    co=sum(((-1)**k*phi**(2*k)/math.factorial(2*k) for k in range(m+1)),F(0))
    si=sum(((-1)**k*phi**(2*k+1)/math.factorial(2*k+1) for k in range(m+1)),F(0))
    ec=abs(phi)**(2*m+2)/math.factorial(2*m+2)
    es=abs(phi)**(2*m+3)/math.factorial(2*m+3)
    return ((ip(co-ec)[0],ip(co+ec)[1]),(ip(si-es)[0],ip(si+es)[1]))


def qsp_coefficients(phases):
    P=[trigonometric(phases[0])];Q=[CZ]
    for phi in phases[1:]:
        rotation=trigonometric(phi);conjugate=(rotation[0],ine(rotation[1]))
        size=max(len(P)+1,len(Q)+2)
        newP=[CZ]*size;newQ=[CZ]*size
        for j,v in enumerate(P):
            newP[j+1]=ca(newP[j+1],v);newQ[j]=ca(newQ[j],v)
        for j,v in enumerate(Q):
            newP[j]=ca(newP[j],cn(v));newP[j+2]=ca(newP[j+2],v)
            newQ[j+1]=ca(newQ[j+1],v)
        P=[cm(v,rotation) for v in newP];Q=[cm(v,conjugate) for v in newQ]
        while len(P)>1 and P[-1]==CZ:P.pop()
        while len(Q)>1 and Q[-1]==CZ:Q.pop()
    return P


def phase_error(phases,target_power):
    coefficients=qsp_coefficients(phases)
    # Even diagonal parity must hold exactly, including the interval zeros.
    assert all(v==CZ for v in coefficients[1::2])
    coeff=coefficients[::2]
    n=max(len(coeff),len(target_power))
    lo=[];hi=[]
    for j in range(n):
        interval=coeff[j][1] if j<len(coeff) else ZERO
        target=target_power[j] if j<len(target_power) else F(0)
        lo.append(F(interval[0],S)-target);hi.append(F(interval[1],S)-target)
    bl=cert.bernstein(lo);bh=cert.bernstein(hi)
    bounds=(tuple((v*S).__floor__() for v in bl),tuple(cert.ceil(v*S) for v in bh))
    low,high=cert.range_bound(bounds,8)
    eta=max(abs(low),abs(high))
    return {'uniform_amplitude_error_upper_exact':str(eta),'uniform_amplitude_error_upper':float(eta),
            'arithmetic_bits':cert.BITS,'scope':'whole lambda interval [0,1], exact saved decimal phase angles',
            'method':'Taylor enclosures for sin/cos, complex interval recurrence, Bernstein subdivision'},eta


def signal_response(xs,phases):
    xs=np.asarray(xs);w=np.zeros((len(xs),2,2),complex)
    w[:,0,0]=w[:,1,1]=xs;w[:,0,1]=w[:,1,0]=1j*np.sqrt(np.maximum(0,1-xs*xs))
    def r(p):return np.diag([np.exp(1j*p),np.exp(-1j*p)])
    U=np.broadcast_to(r(phases[0]),w.shape).copy()
    for phi in phases[1:]:U=U@w@r(phi)
    return U


def synthesize(record):
    c=list(map(F,record['chebyshev_coefficients']))
    certificate=record['certificate'];norm=F(certificate['global_normalization_exact'])
    kappa=F(certificate['kappa_exact']);p=[v*kappa/norm for v in cert.cheb_power(c)]
    # Exact monomial-to-even-Chebyshev conversion, avoiding float cancellation.
    ch=[F(0)]*(2*len(p)-1)
    for k,v in enumerate(p):
        ch[0]+=v*F(math.comb(2*k,k),4**k)
        for j in range(1,k+1):ch[2*j]+=v*F(2*math.comb(2*k,k-j),4**k)
    with contextlib.redirect_stdout(io.StringIO()):
        _,error,iterations,protocol=newton_solver(np.array(list(map(float,ch[::2]))),0,crit=1e-14,maxiter=100)
    if not math.isfinite(error) or error>1e-11:raise RuntimeError('QSP solver failed')
    phases=[F(str(float(x))) for x in protocol.full_phases]
    bound,eta=phase_error(phases,p)
    prior_success=F(certificate['success_lower_exact'])
    reserve=F(record['implementation_bias_reserve'])
    assert 4*eta**2<=reserve**2*prior_success
    sqrt_floor=F(math.isqrt(prior_success.numerator*S*S//prior_success.denominator),S)
    assert eta<sqrt_floor
    success=(sqrt_floor-eta)**2
    grid=np.linspace(-1,1,2049);U=signal_response(grid,list(map(float,phases)))
    target=np.polynomial.polynomial.polyval(grid*grid,list(map(float,p)))
    grid_error=float(np.max(np.abs(U[:,0,0].imag-target)))
    # Explicit 4x4 LCU unitary: H ( -i U direct-sum i U† ) H.
    h=np.kron(np.array([[1,1],[1,-1]])/math.sqrt(2),np.eye(2))
    select=np.zeros((len(grid),4,4),complex)
    select[:,:2,:2]=-1j*U;select[:,2:,2:]=1j*np.swapaxes(U.conj(),1,2)
    full=h@select@h
    matrix_error=float(np.max(np.abs(full[:,0,0]-U[:,0,0].imag)))
    unitary=float(np.max(np.abs(np.swapaxes(full.conj(),1,2)@full-np.eye(4))))
    assert grid_error<1e-9 and matrix_error<1e-12 and unitary<1e-12
    return {'phases_exact_decimal_radians':list(map(str,phases)),
            'solver_error':float(error),'solver_iterations':int(iterations),'certificate':bound,
            'meets_implementation_bias_reserve':True,
            'implemented_success_lower_exact':str(success),'implemented_success_lower':float(success),
            'relative_cost_inflation_upper':float(prior_success/success),
            'numerical_grid_amplitude_error':grid_error,'lcu_extraction_error':matrix_error,
            'lcu_unitarity_error':unitary,'signal_degree':len(phases)-1,
            'serial_extraction_signal_calls':2*(len(phases)-1)}


def main():
    source=ROOT/'results/filter_selection.json';data=json.loads(source.read_text());rows=[]
    for case in data['cases']:
        if 'selected' not in case:continue
        row={'prior':case['prior'],'phase_realization':synthesize(case['selected'])};rows.append(row)
        print(case['prior']['a'],case['prior']['u'],case['prior']['prep_cost'],
              row['phase_realization']['certificate']['uniform_amplitude_error_upper'],flush=True)
    out={'metadata':{'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                     'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     'pyqsp':importlib.metadata.version('pyqsp'),
                     'oracle':'ideal singular-value Wx signal; no hardware compilation',
                     'normalization':'kappa applied once to the whole polynomial, not once per scalar step'},
         'cases':rows}
    (ROOT/'results/filter_selection_qsp.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':main()
