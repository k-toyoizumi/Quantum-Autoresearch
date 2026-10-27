#!/usr/bin/env python3
"""Independent exact sums for binomial laws and outward arithmetic controls."""
from fractions import Fraction as F
import math
import numpy as np
import finite_sampling as fs


def main():
    checks = 0
    for T in [1, 2, 3, 8, 17, 40, 80]:
        for z in [F(1, 10000), F(1, 20), F(1, 3), F(4, 5), F(1)]:
            q = 1-z
            lo, hi = fs.power_enclosure(q, T)
            assert lo <= q**T <= hi
            C = 1-q**T
            H = sum((F(math.comb(T, m))*z**m*q**(T-m)/m for m in range(1, T+1)), F(0))
            exact = H/C
            upper, zero = fs.certified_inverse_bound(T, z)
            assert exact <= upper and q**T <= zero
            numeric = fs.inverse_positive_binomial(T, float(z))
            assert abs(numeric-float(exact)) < 2e-12
            for mu, e in [(F(1, 5), F(1, 10)), (F(2, 3), F(1, 4))]:
                direct = F(0)
                for m in range(1, T+1):
                    mass = F(math.comb(T, m))*z**m*q**(T-m)
                    direct += mass*((mu-e)**2+mu*(1-mu)/m)
                assert direct/C == (mu-e)**2+mu*(1-mu)*exact
                checks += 1
            checks += 3
    # Exact enumeration of every accepted-one count, with rational thresholds.
    for T in [2, 5, 11]:
        z, mu, e, tolerance = F(1, 3), F(2, 5), F(1, 4), F(1, 8)
        failure = (1-z)**T
        for m in range(1, T+1):
            pm = F(math.comb(T, m))*z**m*(1-z)**(T-m)
            failure += pm*sum((F(math.comb(m, k))*mu**k*(1-mu)**(m-k)
                                for k in range(m+1) if abs(F(k, m)-e)>tolerance), F(0))
        numerical = fs.failure_probability(T, float(z), float(mu), float(e), float(tolerance))
        assert abs(numerical['failure_probability_lower_numeric']-float(failure)) < 2e-12
        checks += 1
    # h_T(z) decreases with acceptance; its replacement by 1/E[M] is not exact.
    for T in [2, 8, 100, 10000]:
        values = fs.inverse_positive_binomial(T, np.linspace(.0001, .999, 100))
        assert np.all(np.diff(values) <= 1e-12)
        checks += 1
    assert abs(fs.inverse_positive_binomial(8, .1)-1/(8*.1)) > .1
    print(f'PASS {checks+1} finite-sampling checks: exact sums, rational bounds, law enumeration, monotonicity.')


if __name__ == '__main__':
    main()
