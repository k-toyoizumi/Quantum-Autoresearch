"""Exact rational / outward integer certificates for real spectral polynomials.

The arithmetic primitives adapt the project's earlier Bernstein verifier
(Quantum-Autoresearch, local commit 4c8fb96, certify_gapfree_candidate.py).
All decisions in this module use integers or Fraction; grids do not certify.
"""
from fractions import Fraction as F
from math import comb, isqrt

BITS = 220
S = 1 << BITS


def add(a, b):
    p = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a): p[i] += x
    for i, x in enumerate(b): p[i] += x
    return p


def mul(a, b):
    p = [F(0)] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): p[i+j] += x*y
    return p


def cheb_power(c):
    """c_k T_k(2 lambda - 1), exact power-basis coefficients."""
    t0, t1 = [F(1)], [F(-1), F(2)]
    p = [c[0]]
    if len(c)>1: p=add(p,[x*c[1] for x in t1])
    for ck in c[2:]:
        t2=add([2*x for x in mul(t1,[-F(1),F(2)])],[-x for x in t0])
        p=add(p,[ck*x for x in t2]); t0,t1=t1,t2
    return p


def bernstein(p, length=F(1), degree=None):
    n=len(p)-1 if degree is None else degree
    return [sum((p[k]*length**k*F(comb(i,k),comb(n,k))
                 for k in range(min(i,len(p)-1)+1)),F(0)) for i in range(n+1)]


def ceil(x): return -((-x.numerator)//x.denominator)


def enclose(values):
    return (tuple((v*S).__floor__() for v in values),tuple(ceil(v*S) for v in values))


def split(bounds):
    lo,hi=list(bounds[0]),list(bounds[1])
    ll,lh,rl,rh=[lo[0]],[hi[0]],[lo[-1]],[hi[-1]]
    while len(lo)>1:
        lo=[(a+b)//2 for a,b in zip(lo,lo[1:])]
        hi=[(a+b+1)//2 for a,b in zip(hi,hi[1:])]
        ll.append(lo[0]);lh.append(hi[0]);rl.append(lo[-1]);rh.append(hi[-1])
    return (tuple(ll),tuple(lh)),(tuple(reversed(rl)),tuple(reversed(rh)))


def range_bound(bounds, depth=7):
    leaves=[bounds]
    for _ in range(depth): leaves=[v for b in leaves for v in split(b)]
    return F(min(min(b[0]) for b in leaves),S),F(max(max(b[1]) for b in leaves),S)


def pair_certificate(p, a, u, bias, max_nodes=100000, max_depth=42):
    """Certify (y-x-b) p(y)^2 <= (a*b/(1-a)) p(x)^2.

    Covers the full x in [0,u], y in [0,1] rectangle; y<=x+b is harmless.
    Bounds y*w(y)-(x0+b)*w(y) in a common elevated Bernstein basis.
    """
    w=mul(p,p); n=len(w)
    wx=enclose(bernstein(w,u))
    wy=enclose(bernstein(w,F(1),n))
    yw=enclose(bernstein([F(0)]+w,F(1),n))
    ratio=a*bias/(1-a)
    stack=[(F(0),u,wx,F(0),F(1),wy,yw,0,0)]
    nodes=leaves=0; deepest=0
    while stack:
        x0,x1,vx,y0,y1,vy,yt,dx,dy=stack.pop();nodes+=1
        deepest=max(deepest,dx+dy)
        if y1<=x0+bias: leaves+=1;continue
        upper=max(ceil(F(t)-(x0+bias)*v) for t,v in zip(yt[1],vy[0]))-(ratio*min(vx[0])).__floor__()
        if upper<=0: leaves+=1;continue
        if nodes>=max_nodes or dx+dy>=max_depth:
            return {'certified':False,'nodes':nodes,'leaves':leaves,
                    'unresolved_rectangle':list(map(str,[x0,x1,y0,y1])),
                    'residual_upper':str(F(upper,S))}
        if dx<=dy and u>0:
            vl,vr=split(vx);mid=(x0+x1)/2
            stack.extend([(x0,mid,vl,y0,y1,vy,yt,dx+1,dy),
                          (mid,x1,vr,y0,y1,vy,yt,dx+1,dy)])
        else:
            vl,vr=split(vy);tl,tr=split(yt);mid=(y0+y1)/2
            stack.extend([(x0,x1,vx,y0,mid,vl,tl,dx,dy+1),
                          (x0,x1,vx,mid,y1,vr,tr,dx,dy+1)])
    return {'certified':True,'nodes':nodes,'leaves':leaves,'max_total_depth':deepest,
            'residual_upper':'0','arithmetic_bits':BITS}


def certify(c, a, u, bias, kappa=F(19,20)):
    p=cheb_power(c)
    global_lo,global_hi=range_bound(enclose(bernstein(p)),8)
    normalization=max(F(1),abs(global_lo),abs(global_hi))
    target_lo,target_hi=range_bound(enclose(bernstein(p,u)),8)
    if target_lo<=0:
        return {'certified':False,'reason':'target positivity not certified'}
    pair=pair_certificate(p,a,u,bias)
    tau=target_lo/normalization
    target_endpoint_upper=min(p[0],sum(v*u**i for i,v in enumerate(p)))/normalization
    return {'certified':pair['certified'],'pair':pair,
            'target_amplitude_lower_exact':str(tau),
            'target_amplitude_upper_exact':str(target_endpoint_upper),
            'global_normalization_exact':str(normalization),
            'kappa_exact':str(kappa),
            'success_lower_exact':str(a*(kappa*tau)**2),
            'success_upper_exact':str(a*(kappa*target_endpoint_upper)**2),
            'endpoint_zero_exact':sum(p)==0,
            'target_amplitude_lower':float(tau),
            'global_normalization':float(normalization),
            'success_lower':float(a*(kappa*tau)**2)}


def sqrt_upper(q, scale=10**12):
    n=isqrt(q.numerator*scale*scale//q.denominator)
    return F(n+1,scale)


def cheb_values(x,n):
    z=2*x-1;v=[F(1)]
    if n:v.append(z)
    for _ in range(2,n+1):v.append(2*z*v[-1]-v[-2])
    return v


def grid_dual_upper(result, metadata, a, u, bias, degree):
    """Exact weak-duality bound including an exact stationarity correction.

    Finite-grid sqrt coefficients are rounded UP, weakening pair constraints.
    True |P|<=1 implies |c0|<=1, |ck|<=2; also 0<=tau<=1.
    Thus arbitrary nonnegative rational dual weights give a rigorous upper
    objective bound even when floating-point stationarity is imperfect.
    """
    dual=[F(0)]*(degree+2); objective=F(0);active=0
    for y_float,info in zip(-result.ineqlin.marginals,metadata):
        if y_float<=1e-14:continue
        y=F(str(float(y_float)));active+=1
        kind=info[0]
        if kind=='support':
            _,x,sign=info;row=[sign*v for v in cheb_values(x,degree)]+[F(0)];rhs=F(1)
        elif kind=='target':
            row=[-v for v in cheb_values(info[1],degree)]+[F(1)];rhs=F(0)
        elif kind=='endpoint':
            row=[F(info[1])]*(degree+1)+[F(0)];rhs=F(0)
        else:
            _,e,x,sign=info;q=sqrt_upper(a*bias/((1-a)*(x-e-bias)))
            row=[sign*vx-q*ve for vx,ve in zip(cheb_values(x,degree),cheb_values(e,degree))]+[F(0)];rhs=F(0)
        objective+=y*rhs
        dual=[v+y*r for v,r in zip(dual,row)]
    residual=[-v for v in dual];residual[-1]+=1
    correction=sum(abs(v)*bound for v,bound in zip(residual,[1]+[2]*degree+[1]))
    upper=objective+correction
    return {'upper_exact':str(upper),'upper':float(upper),'active_dual_rows':active,
            'stationarity_correction_exact':str(correction),
            'stationarity_correction':float(correction),
            'arithmetic':'exact Fraction weak duality with Chebyshev coefficient bounds'}
