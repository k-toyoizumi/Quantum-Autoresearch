"""Independent exact controls for the interval and dual certificate path."""
from fractions import Fraction as F
from math import comb
import selection_certificates as c
from filter_selection import solve, samples, LN40_UPPER
from selection_qsp import im, cm, S


def bernstein_value(b,t):
    n=len(b)-1
    return sum(comb(n,k)*v*t**k*(1-t)**(n-k) for k,v in enumerate(b))


def main():
    checks=0
    for polynomial in [[F(1,7),F(-3,5),F(7,3)], [F(-2),F(5),F(-7),F(3)]]:
        for length in [F(1),F(1,5)]:
            b=c.bernstein(polynomial,length);lohi=c.enclose(b)
            children=c.split(lohi)
            for j in range(33):
                t=F(j,32)
                direct=sum(v*(length*t)**k for k,v in enumerate(polynomial))
                assert direct==bernstein_value(b,t)
                for child,z in zip(children,[t/2,(1+t)/2]):
                    exact=bernstein_value(b,z)
                    assert bernstein_value(child[0],t)<=exact*S<=bernstein_value(child[1],t)
                    checks+=1
    # A known degree-one admissible polynomial has exact optimum tau=1-u.
    a,u,b=F(4,5),F(1,10),F(1,10)
    polynomial=[F(1,2),F(-1,2)]
    record=c.certify(polynomial,a,u,b)
    assert record['certified'] and record['endpoint_zero_exact']
    coefficients,lp=solve(a,u,b,1)
    assert F(lp['dual']['upper_exact'])>=1-u
    assert float(F(lp['dual']['upper_exact'])-(1-u))<1e-10
    # Deliberately invalid filters must not acquire certificates.
    assert not c.pair_certificate([F(1)],a,u,F(1,100),max_nodes=200,max_depth=12)['certified']
    assert not c.certify([F(-1)],a,u,b)['certified']
    # Directed multiplication and complex multiplication at exact corners.
    for lo in [-17,-2,0,5]:
        for high in [lo,lo+3]:
            x=(lo,high);y=(-9,13);z=im(x,y)
            for xx in x:
                for yy in y:
                    assert F(z[0],S)<=F(xx*yy,S*S)<=F(z[1],S)
                    checks+=1
    for X,Y in [(((1,5),(-7,2)),((-4,9),(0,3))), (((-5,-1),(1,1)),((3,3),(-7,-2)))]:
        Z=cm(X,Y)
        for xr in X[0]:
            for xi in X[1]:
                for yr in Y[0]:
                    for yi in Y[1]:
                        rr=F(xr*yr-xi*yi,S*S);ii=F(xr*yi+xi*yr,S*S)
                        assert F(Z[0][0],S)<=rr<=F(Z[0][1],S)
                        assert F(Z[1][0],S)<=ii<=F(Z[1][1],S)
                        checks+=1
    assert F(3688879454113936,10**15)<LN40_UPPER<F(3688879454113937,10**15)
    print('PASS',checks,'exact arithmetic checks; feasible/infeasible controls; analytic degree-one dual bound')


if __name__=='__main__':main()
